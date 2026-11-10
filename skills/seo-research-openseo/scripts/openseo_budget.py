#!/usr/bin/env python3
"""Dollar cap and cost log for OpenSEO / DataForSEO research runs.

OpenSEO self-hosted has no spend cap of its own, and every site shares one
DataForSEO account. So this script is the cap:

  estimate  price a planned list of OpenSEO tool calls (no network)
  start     check month-to-date spend + the estimate against the site cap,
            read the live DataForSEO balance (free call), save a run file.
            Exit 3 = over cap: do not make the calls.
  end       read the balance again, log the real spend (balance delta).
  month     show month-to-date spend per site from the cost log.

Run one site at a time so the balance delta belongs to that run.
Key: DATAFORSEO_API_KEY (base64 login:password) from the environment only.
Never print it. No key = estimate-only, and the log line says so.

Example:
  python3 openseo_budget.py estimate plan.json
  python3 openseo_budget.py start --site hsatrackr --plan plan.json --cap-usd 10 \
      --log logs/hsatrackr/openseo/COST-LOG.md
  ...make the OpenSEO MCP calls...
  python3 openseo_budget.py end --site hsatrackr --log logs/hsatrackr/openseo/COST-LOG.md

plan.json: [{"tool": "get_keyword_metrics", "n": 1, "rows": 300}, {"tool": "get_serp_results", "n": 10}]
"""
import argparse, base64, datetime as dt, json, os, re, sys, urllib.request
from pathlib import Path

# Raw DataForSEO USD per call (self-hosted pays raw, no OpenSEO markup).
# From open-seo src/server/lib/dataforseo/pricing.ts (read Sep 2026) and the
# free /v3/appendix/user_data price table (checked 2026-10-21). Upper bounds.
LABS_TASK, LABS_ROW = 0.012, 0.00012
BL_TASK, BL_ROW = 0.024, 0.000036
PRICES = {
    # tool: (base per call, per row)  rows = expected result rows
    "research_keywords":        (0.012 + 0.09, 0.00012),  # per seed; worst case w/ fallback
    "get_keyword_metrics":      (LABS_TASK, LABS_ROW),    # rows = keywords sent (<=700)
    "get_ranked_keywords":      (LABS_TASK, LABS_ROW),
    "get_domain_keyword_suggestions": (LABS_TASK, LABS_ROW),
    "get_domain_overview":      (0.25, 0.0),              # tool says ~100-300 credits hosted; padded
    "find_serp_competitors":    (LABS_TASK, LABS_ROW),
    "get_serp_results":         (0.002, 0.0),             # per keyword at depth 10-20 (live)
    "get_backlinks_overview":   (BL_TASK, BL_ROW),
    "get_backlinks_profile":    (BL_TASK, BL_ROW),
    "get_local_serp_results":   (0.002, 0.0),
    "get_local_rank_grid":      (0.002, 0.0),             # n = grid points (3x3 = 9)
    "search_local_businesses":  (0.012, 0.00036),
    "get_business_profile":     (0.0054, 0.0),
    "get_business_reviews":     (0.01, 0.0),              # per 20 reviews, padded
    "get_google_business_questions": (0.0054, 0.0),
    "run_site_audit":           (0.0, 0.0),               # crawl is free; Lighthouse sample adds ~$0.005/page
    "lighthouse_page":          (0.005, 0.0),
    "run_rank_tracker":         (0.002, 0.0),             # n = keywords x devices (live); queued ~$0.0006
    "run_ai_visibility_check":  (0.004, 0.0),             # n = prompts x engines (live); queued $0.0012
    "research_ai_visibility_prompts": (0.101, 0.0),       # LLM mentions endpoints bill ~$0.10/request
    "explore_prompt":           (0.09, 0.0),              # ChatGPT with web search; Claude ~$0.18
}
FREE = {"get_search_console_performance", "inspect_urls", "get_search_opportunities",
        "list_projects", "get_project_context", "list_saved_keywords", "save_keywords",
        "get_rank_tracker", "estimate_rank_tracker_cost", "estimate_ai_visibility_cost",
        "get_audit_status", "get_audit_issues", "get_audit_pages", "whoami",
        "save_report", "list_reports", "get_report", "list_business_categories"}


def price(plan):
    total, lines = 0.0, []
    for c in plan:
        tool, n, rows = c["tool"], int(c.get("n", 1)), int(c.get("rows", 0))
        if tool in FREE or tool.startswith("get_google_analytics_"):
            usd = 0.0
        elif tool in PRICES:
            base, per = PRICES[tool]
            usd = n * (base + rows * per)
        else:
            sys.exit(f"unknown tool {tool}: add it to PRICES before spending")
        total += usd
        lines.append(f"  {tool} x{n} rows {rows}: ${usd:.4f}")
    return round(total, 4), lines


def balance():
    key = os.environ.get("DATAFORSEO_API_KEY", "").strip()
    if not key:
        return None
    req = urllib.request.Request("https://api.dataforseo.com/v3/appendix/user_data",
                                 headers={"Authorization": "Basic " + key})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
    return float(d["tasks"][0]["result"][0]["money"]["balance"])


def month_spend(log, site):
    if not log.exists():
        return 0.0
    ym = dt.date.today().strftime("%Y-%m")
    s = 0.0
    for line in log.read_text().splitlines():
        p = [x.strip() for x in line.split("|")]
        if len(p) >= 5 and p[0].startswith(ym) and p[2] == site:
            m = re.search(r"\$([0-9.]+)", p[4])
            if m:
                s += float(m.group(1))
    return round(s, 4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["estimate", "start", "end", "month"])
    ap.add_argument("plan", nargs="?")
    ap.add_argument("--plan", dest="plan_opt")
    ap.add_argument("--site", default="")
    ap.add_argument("--workflow", default="openseo-weekly")
    ap.add_argument("--cap-usd", type=float, default=10.0, help="monthly cap for this site")
    ap.add_argument("--run-cap-usd", type=float, default=3.0, help="cap for one run")
    ap.add_argument("--log", default="COST-LOG.md")
    a = ap.parse_args()
    log = Path(a.log)
    runf = log.with_name(f".openseo-run-{a.site or 'site'}.json")
    planf = a.plan or a.plan_opt

    if a.cmd == "estimate":
        est, lines = price(json.load(open(planf)))
        print("\n".join(lines)); print(f"estimate ${est:.4f}"); return

    if a.cmd == "month":
        print(f"{a.site}: ${month_spend(log, a.site):.4f} this month (cap ${a.cap_usd:.2f})"); return

    if a.cmd == "start":
        est, lines = price(json.load(open(planf))) if planf else (0.0, [])
        mtd = month_spend(log, a.site)
        print("\n".join(lines)); print(f"estimate ${est:.4f} | month so far ${mtd:.4f} | cap ${a.cap_usd:.2f}/mo, ${a.run_cap_usd:.2f}/run")
        if est > a.run_cap_usd or mtd + est > a.cap_usd:
            print("OVER CAP: do not make these calls. Shrink the plan or ask the owner to raise the cap.")
            sys.exit(3)
        b = balance()
        if b is not None and b < est:
            print(f"DataForSEO balance ${b:.2f} is below the estimate. Stop and tell the owner."); sys.exit(3)
        runf.parent.mkdir(parents=True, exist_ok=True)
        json.dump({"site": a.site, "est": est, "bal": b, "t": dt.datetime.now().isoformat()}, open(runf, "w"))
        print("OK to run." + ("" if b is not None else " (no key: spend will be logged as an estimate)"))
        return

    if a.cmd == "end":
        r = json.load(open(runf))
        b = balance()
        if r["bal"] is not None and b is not None:
            spent, how = round(max(r["bal"] - b, 0.0), 5), "measured"
        else:
            spent, how = r["est"], "estimate"
        log.parent.mkdir(parents=True, exist_ok=True)
        if not log.exists():
            log.write_text("# OpenSEO / DataForSEO cost log\n\ndate | workflow | site | est | spent | how | balance after\n")
        now = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
        bal = f"${b:.2f}" if b is not None else "n/a"
        with log.open("a") as f:
            f.write(f"{now} | {a.workflow} | {a.site} | est ${r['est']:.4f} | ${spent:.4f} | {how} | {bal}\n")
        runf.unlink()
        print(f"logged ${spent:.4f} ({how}); month so far ${month_spend(log, a.site):.4f}")


if __name__ == "__main__":
    main()
