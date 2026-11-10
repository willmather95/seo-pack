#!/usr/bin/env python3
"""Judge every row with Jev, under a hard dollar cap, and sort rows into act / review / drop.

Code counts and holds the veto. Jev only answers typed questions. Nothing here edits a site,
publishes or sends: the script writes files.

Usage:
  jev_rows.py QUESTIONS.json ROWS.jsonl --out DIR                      dry run: one sample request + cost estimate
  jev_rows.py QUESTIONS.json ROWS.jsonl --out DIR --live [--limit 50]  call Jev, write DIR/results.jsonl + act/review/drop.jsonl
      [--cap-usd 1.00] [--workflow NAME] [--site SLUG] [--cost-log PATH] [--veto-words 600]
  jev_rows.py calibrate RESULTS.jsonl LABELS.csv                       compare with hand labels (csv: id,question,label)

QUESTIONS.json: {"workflow": str, "questions": {id: {type, instructions, criteria}},
                 "bands": {id: {"act": 0.8, "drop": 0.2}},           optional, defaults below
                 "veto_values": {id: [values that may never act alone]}, optional
                 "gate": {"pass_if": {id: [op_or_choice, number]}}}      optional, all must hold to act
ROWS.jsonl: {"id": ..., "state": {...sent to Jev...}, "meta": {...kept by code, never sent...}}
Model: JEV_MODEL env, default jev-1.13.0 (aliases refused). Key: TYPESAFE_API_KEY env, never printed.
"""
import csv, datetime, json, os, sys, time, urllib.error, urllib.request

ENDPOINT = "https://api.typesafe.ai/v1/systemone"
USD_PER_MTOK = 0.042          # docs.typesafe.ai, checked 2026-10-18; recheck on the day you build
DEFAULT_ACT, DEFAULT_DROP = 0.8, 0.2
VETO_ALWAYS = {"merge", "merge_or_remove", "remove", "delete", "redirect", "noindex", "noindex_or_remove"}


def arg(name, default=None, cast=str):
    if name in sys.argv:
        return cast(sys.argv[sys.argv.index(name) + 1])
    return default


def est_tokens(body: bytes) -> int:
    return len(body) // 3 + 1      # conservative, so the cap is never beaten by an estimate


def band(q, a, b):
    """Return (value, band) for one typed answer. Bands: act, review, drop."""
    t = q["type"]
    act, drop = b.get("act", DEFAULT_ACT), b.get("drop", DEFAULT_DROP)
    if t == "noul":
        v = float(a["noul"])
        return v, "act" if v >= act else "drop" if v <= drop else "review"
    conf = float(a.get("confidence", 0) or 0)
    if t == "choice":
        if a.get("choice") not in q["criteria"]:
            raise ValueError("choice outside the allowed options")
        return a["choice"], "act" if conf >= act else "review"
    top = len(q["criteria"]) - 1
    s = float(a["score"])
    probs = a.get("probabilities") or {}
    upper = sum(float(p) for k, p in probs.items() if int(k) / top >= 0.5)
    side = max(upper, 1 - upper) if probs else conf
    return s, "act" if side >= act else "review"


def gate_ok(gate, answers):
    for qid, (op, x) in gate.items():
        v = answers.get(qid, {}).get("value")
        if v is None:
            return False
        if op == ">=" and not float(v) >= x: return False
        if op == "<=" and not float(v) <= x: return False
        if op not in (">=", "<="):          # choice: [wanted value, min confidence]
            if v != op or float(answers[qid].get("confidence", 0)) < x: return False
    return True


def decide(spec, row, answers, veto_words):
    notes = []
    bands = [a["band"] for a in answers.values()]
    decision = "review" if "review" in bands else ("drop" if bands and all(b == "drop" for b in bands) else "act")
    gate = (spec.get("gate") or {}).get("pass_if")
    if gate:
        decision = "act" if gate_ok(gate, answers) else "review"
        if decision == "review":
            notes.append("gate failed: " + ", ".join(k for k in gate if not gate_ok({k: gate[k]}, answers)))
    vetoes = {k: set(v) for k, v in (spec.get("veto_values") or {}).items()}
    words = (row.get("meta") or {}).get("word_count")
    for qid, a in answers.items():
        v = a.get("value")
        if isinstance(v, str) and (v in VETO_ALWAYS or v in vetoes.get(qid, ())):
            if decision == "act":
                decision = "review"
            notes.append(f"veto: {qid}={v} never acts alone")
            if words is not None and veto_words and words >= veto_words:
                notes.append(f"veto: {words} words >= {veto_words}, removal blocked by code")
    return decision, notes


def cost_line(path, workflow, site, rows, calls, skipped, tokens, cap, model):
    usd = tokens * USD_PER_MTOK / 1e6
    now = datetime.datetime.now().astimezone()
    line = (f"{now:%Y-%m-%d %H:%M} {now.tzname()} | {workflow} | {site} | rows {rows} | calls {calls} | "
            f"skipped {skipped} | tokens {tokens} | ${usd:.6f} | cap ${cap:g} | {model}")
    print(line)
    if path:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "a") as f:
            f.write(line + "\n")


def run():
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags_with_values = {arg(n) for n in ("--out", "--limit", "--cap-usd", "--workflow", "--site", "--cost-log", "--veto-words") if n in sys.argv}
    pos = [a for a in pos if a not in flags_with_values]
    if len(pos) != 2 or "--out" not in sys.argv:
        sys.exit(__doc__)
    spec = json.load(open(pos[0]))
    rows = [json.loads(l) for l in open(pos[1]) if l.strip()]
    limit = arg("--limit", None, int)
    rows = rows[:limit] if limit else rows
    out = arg("--out")
    cap = arg("--cap-usd", 1.00, float)
    workflow = arg("--workflow", spec.get("workflow", "jev-rows"))
    site = arg("--site", "-")
    cost_log = arg("--cost-log")
    veto_words = arg("--veto-words", 600, int)
    model = os.environ.get("JEV_MODEL", "jev-1.13.0")
    if model.endswith(("latest", "preview")):
        sys.exit("Pin a version (e.g. jev-1.13.0). Aliases move on their own.")
    qs, bands = spec["questions"], spec.get("bands", {})
    bodies = [json.dumps({"model": model, "state": r.get("state", {}), "questions": qs}).encode() for r in rows]
    est_total = sum(est_tokens(b) for b in bodies)
    est_usd = est_total * USD_PER_MTOK / 1e6
    if "--live" not in sys.argv:
        print(json.dumps(json.loads(bodies[0]), indent=2) if bodies else "no rows")
        print(f"\nDry run: {len(rows)} rows, {len(qs)} questions each, 1 call per row. "
              f"Estimated {est_total} tokens, about ${est_usd:.5f} (cap ${cap:g}). Add --live to call Jev.")
        return
    key = os.environ.get("TYPESAFE_API_KEY") or sys.exit("TYPESAFE_API_KEY is not set. Dry run only.")
    os.makedirs(out, exist_ok=True)
    files = {k: open(os.path.join(out, f"{k}.jsonl"), "w") for k in ("results", "act", "review", "drop")}
    tokens = calls = skipped = failed = 0
    returned_model = model
    for r, body in zip(rows, bodies):
        est = est_tokens(body)
        if (tokens + est) * USD_PER_MTOK / 1e6 > cap:      # hard cap, checked before every call
            skipped += 1
            continue
        req = urllib.request.Request(ENDPOINT, data=body, headers={"authorization": "Bearer " + key, "content-type": "application/json"})
        t0 = time.time()
        for attempt in range(3):
            try:
                resp = json.load(urllib.request.urlopen(req, timeout=30))
                break
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503) and attempt < 2:
                    time.sleep(2 ** attempt); continue
                resp = {"error": f"HTTP {e.code}"}; break
            except Exception as e:
                resp = {"error": type(e).__name__}; break
        calls += 1
        usage = resp.get("usage") or {}
        tokens += usage["input_tokens"] if isinstance(usage.get("input_tokens"), int) else est
        returned_model = resp.get("model") or returned_model
        rec = {"id": r.get("id"), "meta": r.get("meta"), "ms": int((time.time() - t0) * 1000), "model": resp.get("model"), "usage": usage}
        try:
            if "error" in resp:
                raise ValueError(resp["error"])
            ans = {}
            for qid, q in qs.items():
                a = resp["answers"][qid]
                v, bnd = band(q, a, bands.get(qid, {}))
                ans[qid] = {"value": v, "band": bnd, "confidence": a.get("confidence"), "probabilities": a.get("probabilities")}
            rec["answers"] = ans
            rec["decision"], rec["notes"] = decide(spec, r, ans, veto_words)
        except Exception as e:
            failed += 1
            rec["decision"], rec["notes"] = "review", [f"error: {e}"]
        line = json.dumps(rec) + "\n"
        files["results"].write(line)
        files[rec["decision"]].write(line)
    for f in files.values():
        f.close()
    counts = {k: sum(1 for _ in open(os.path.join(out, f"{k}.jsonl"))) for k in ("act", "review", "drop")}
    print(f"Wrote {out}: act {counts['act']}, review {counts['review']}, drop {counts['drop']}, failed {failed}, skipped by cap {skipped}.")
    if rows and counts["review"] / max(1, calls) > 0.05:
        print(f"Review pile is {counts['review'] / max(1, calls):.0%} of calls (target under 5%). Check the question before the threshold.")
    cost_line(cost_log, workflow, site, len(rows), calls, skipped, tokens, cap, returned_model)


def calibrate():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    res = {}
    for l in open(sys.argv[2]):
        if l.strip():
            r = json.loads(l); res[str(r["id"])] = r.get("answers") or {}
    per = {}
    with open(sys.argv[3]) as f:
        for row in csv.DictReader(f):
            q, want = row["question"], row["label"].strip().lower()
            a = res.get(str(row["id"]), {}).get(q)
            if a is None:
                continue
            got = a["value"]
            if isinstance(got, float) and want in ("yes", "no", "true", "false", "1", "0"):
                got_s = "yes" if got >= 0.5 else "no"
                want = "yes" if want in ("yes", "true", "1") else "no"
            else:
                got_s = str(int(got)) if isinstance(got, float) and got.is_integer() else str(got).lower()
            d = per.setdefault(q, {"n": 0, "miss": []})
            d["n"] += 1
            if got_s != want:
                d["miss"].append((row["id"], want, got_s, a["band"]))
    for q, d in per.items():
        m = len(d["miss"])
        verdict = "trust the high band" if m < 5 else "rewrite the question, not the threshold" if m > 10 else "read each miss, tighten the criteria, rerun"
        print(f"{q}: {m} disagreements in {d['n']} labels -> {verdict}")
        for i, want, got, b in d["miss"]:
            print(f"   {i}: you said {want}, Jev said {got} ({b})")


if __name__ == "__main__":
    calibrate() if len(sys.argv) > 1 and sys.argv[1] == "calibrate" else run()
