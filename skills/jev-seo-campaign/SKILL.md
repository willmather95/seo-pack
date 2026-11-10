---
name: jev-seo-campaign
description: Use when an SEO job has to judge many rows at once (a full Search Console export, every page pair, every internal link candidate, every link prospect, every draft before it goes live) or when running a full keyword-to-page campaign with Jev. Real data finds, code counts, Jev judges, a writing model writes. Covers the question types and thresholds, the 50-row hand-label check, the code veto, cost math with a hard dollar cap, and how it fits HSA Trackr, MMS and NTO.
---
# Jev SEO campaign

One job: let Jev judge every row, cheaply, while code and the owner keep control.
Read `jev-decisions` first for the Jev basics (pinning, split questions, shadow mode). This skill is the SEO runbook on top of it. The prompts, in campaign order, are in `references/prompts.md`.

## 1. Four roles, never mixed
| Role | Who | Does | Never |
|---|---|---|---|
| Finds | Real data: Search Console, live SERP, crawl, backlink exports | Supplies every number and fact | Comes from model memory |
| Counts | Code | Word counts, positions, clicks, dates, "did it go up", pixel widths, sums | Gets guessed by a model |
| Judges | Jev | One narrow typed question per row, a probability back | Writes, counts, compares numbers or dates |
| Writes | Opus, Claude, Codex or Grok Bot | Briefs, pages, titles, emails, reports; runs the other three | Grades its own work |

The writer is the only part that can make things up. Fence it in with the other three. When a decision is new, let the writer reason about it out loud once. When you see it make the same small call a hundred times, turn it into a Jev question. Opus explores, Jev industrializes.

## 2. Three question types and the bands
| Type | Use for | Answer | Decisive when |
|---|---|---|---|
| noul | a yes/no statement | P(yes) 0-1 | 0.8+ (yes) or 0.2- (no) |
| choice | 3-10 named outcomes, always with "other" | pick, probability per option, confidence | confidence 0.8+ |
| score | a level on a rubric (2-10 levels, low to high) | level, probabilities, confidence | 0.8+ of probability on one side of the midpoint |

Default action bands before calibration: act alone above 0.9, act carefully (or sort, never touch) 0.5 to 0.9, a person below 0.5. Your 50 rows set the real numbers. Write the bands into the site's rules file.

Writing the question (`references/prompts.md` prompt 0):
1. One decision per question. "Buyer AND already ranking?" is two questions.
2. A positive statement, so a high number means yes to something good. Never "is this NOT relevant?".
3. Describe what true and false look like in OUR business words, from the site file.
4. Choice: a few words per option, and always "other".
5. State = only what a human expert would read to decide. Two sentences about the business plus the row. No page bodies unless the call is about the body.
6. If the decision needs a number or a date, code computes it first and passes the result as text ("this page lost 40% of its clicks").

## 3. Per-row workflows (thresholds included)
| Workflow | Prompt | Jev asks | Code does | Output |
|---|---|---|---|---|
| Full GSC intent triage | 4 | noul "buyer": someone typing this could buy (or subscribe) from us | Export 16 months; keep 0.8+, drop 0.2-, rest review | keep/drop/review.csv, top 40 review rows by impressions for a human |
| Keyword categories | 5 | choice: alternative, comparison, provider_city, best_list, price_review, how_to, other | Group, sum impressions, mark queries that already have a page | categories.md |
| Quick wins | 6 | score 0/1/2: how well this page answers this query | Position 5-20 and 100+ impressions in 90 days, exact page and query | 2 = title fix, 1 = brief, 0 = new page and leave the old one alone |
| Page-pair cannibalization | C | two nouls in one call: same_intent, same_angle | Build every pair of our pages that share a query; flag only when BOTH are 0.9+ | cannibal.md. Owner decides; nothing merged |
| SERP page type | 7 | choice per result: service, product, category, comparison, ranking_list, article, forum, video, other | Count types; count top-3 titles with the exact keyword | Dominant type and "the opening" if none has the keyword |
| Title sort | 9 | score 0-3 per option: how likely a searcher clicks it among the current top 10 | Pixel width under 600 px with the SERP font | Top 2 with score and width. Owner picks |
| Pre-publish draft gate | 11 | nouls intent, original, unsupported, title_h1 and choice verdict publish/revise/rewrite | Word and heading counts, links, schema | Auto-pass only if verdict publish 0.9+, intent 0.9+, original 0.9+ AND unsupported 0.1-. Anything else goes to the owner with the failing question named |
| Internal link picks | 12 | score 0/1/2: same topic as the target page | Crawl the site (not the sitemap); pre-filter same folder or category and not already linking; max 100 | Top 8 score-2 pages; the writer drafts one sentence each with the exact anchor; before and after |
| Link prospects | 13 | score 0/1/2: same topic and same audience as our page | Drop sites with no real organic traffic on their own topic (a number, so code) | prospects.csv by P(level 2). Never invent an email |
| GEO lists | 15 | nouls third_party_list, lists_us | Add "best X year" versions of top queries | geo.md: lists we're missing from |
| Local reviews | L | choice names_service_and_place / names_service / generic_praise / complaint / other | Share per option for us and the 3 map-pack rivals; services named in theirs, not ours | reviews.md, then a better review request |

Run them with `scripts/jev_rows.py` (section 6). Never judge useless things just because they're cheap: no toxic-backlink classifier, no disavow cleanup, no keyword density, no "content score", no word-count targets.

## 4. The veto belongs to code and the owner
- A probability never makes a call you can't undo: delete, merge, redirect, noindex, publish, edit a live page, change a title that already gets clicks, send. Jev ranks; code or the owner decides.
- Remove block: code refuses any "remove", "merge" or "noindex" verdict on a page of 600 words or more, whatever the model says (Agrici). `jev_rows.py --veto-words 600` does this.
- Protect what ranks. Before touching a page, list the queries it already gets clicks for. If the change would cost them, make a new page instead.
- 90-day WAIT. Code marks any page changed in the last 90 days WAIT. It is not touched, whatever the numbers say. The next action after a publish is another keyword, not another edit.
- Check "done" with a script, never with the writer's word: the URL returns 200, it's in the sitemap, it has its internal links, the PR or deploy is on the right branch.
- Rejections compound. Every "no" from the owner becomes one line at the bottom of the site's rules file. Read it before the next run.

## 5. The 50-row rule (calibration)
Once per workflow, before anything acts on it:
1. Take 50 real rows from the site. Label them by hand without seeing Jev's answer.
2. Run the workflow on the same 50 (`jev_rows.py ... --limit 50 --live`).
3. Count the disagreements (`jev_rows.py calibrate results.jsonl labels.csv`).
4. Under 5: trust the high band. 5 to 10: read each one, tighten the criteria, rerun. Over 10: rewrite the question, not the threshold.
5. Read the disagreements before changing anything. Nine times out of ten the question was ambiguous and Jev took the other reading.
Once a month (prompt 18): 30 random auto-approved rows plus 20 sent to review, labeled blind. Move a threshold only on that evidence and write the change in the rules file. A probability you never checked is a confident guess with decimals.
Scoreboards: the GSC review pile is under 5% of the export; the cannibal list is a handful of pairs; every live page passed the gate; every new page has 3-5 in-text internal links. In the end, only clicks and conversions on business queries 90 days after each change count.

## 6. Cost math and the hard cap
- Price (check on the day you build): $0.042 per million input tokens, output free, cached input free on Cloudflare. A row is about 300 tokens; a page about 3,400.
- Math: cost = rows x tokens per row x 0.042 / 1,000,000. 18,000 GSC queries x 300 = 5.4M tokens = about $0.23. A 60-page audit is about $0.01. A 3,000-token draft gate is $0.00013.
- Every run has a hard dollar cap checked in code before each call. Default $1.00 a run, $0.25 for an audit-sized job. Calls past the cap are skipped and counted, never run.
- Every run appends one cost log line to `logs/<site>/jev/COST-LOG.md`:
  `2026-10-19 15:40 CDT | gsc-triage | hsatrackr | rows 50 | calls 50 | skipped 0 | tokens 15210 | $0.000639 | cap $1.00 | jev-1.13.0`
- Key: `TYPESAFE_API_KEY` from the environment only. Never print, paste or ask for it in chat. No key = dry run only; say so.
```bash
python3 scripts/jev_rows.py questions.json rows.jsonl --out run/            # dry run: prints one request and the estimated cost
python3 scripts/jev_rows.py questions.json rows.jsonl --out run/ --live --limit 50 --cap-usd 0.05 \
  --workflow gsc-triage --site hsatrackr --cost-log logs/<site>/jev/COST-LOG.md
python3 scripts/jev_rows.py calibrate run/results.jsonl labels.csv          # disagreements per question and the verdict
```
Question files (`questions.json`) for each workflow are in `references/prompts.md`. Model is pinned to `jev-1.13.0` (`JEV_MODEL` to change, never an alias).

## 7. The campaign, in order
Setup once: site file plus rules file (prompts 1-2, our versions are `seo-loop/sites/<site>.md` and the team's rules or MISTAKES file). Then:
1. Authority read (3): DR under 20 long tail only, 20-40 mid tail, over 40 head terms. Under 50 referring domains, start 3-5 free on-topic links this week, in parallel.
2. Full GSC triage on 50 rows, label, then the full export (4). Categories (5). Quick wins (6). Pick ONE page this week and say why.
3. Cannibal check when pages share queries (C).
4. SERP read (7), brief with the one thing the top 3 lack (8), titles (9), first page by hand then template plus process file (10), draft gate (11).
5. Internal links for the page (12). Then outside links (13-14) only on a page with proven potential, sized inside the top 3 pages' range, free placements first.
6. GEO (15-16) is about one action in ten. Never rank yourself first in your own list. Track 3-5 real buyer prompts a week in a private window (cited yes or no) and read Bing Webmaster Tools' AI Performance report.
7. Every Monday (17): 28 vs 28 days, WAIT anything changed in 90 days, lost position = better page, lost CTR at the same position = better title, new queries only through 4 and 5, five actions ranked by business value. First Monday of the month: calibration (18).
Pace: one page a day is a ceiling. Two very good pages a week is plenty. A new site, about one a week. Real data steps use our own sources (GSC API scripts, live SERP reads, free backlink sources); ChatSEO or any other paid tool only with the owner's yes. OpenSEO + DataForSEO is approved (2026-10-21) inside each site's cap: see `seo-research-openseo`.

## 8. Fit to your sites
Site details live in `seo-loop/sites/<site>.md`. Each seat runs its own site and logs cost in its own folder. Write one buyer noul per site, for example: "Someone typing this could open or switch an HSA, compare HSA providers, or track HSA receipts." For health or other regulated sites, add a noul that the draft makes no outcome promise, and gate every figure on a primary source with an as-of date. Proof stays each site's own numbers.

## 9. What this does not prove
Jev is weeks old. Speed and accuracy numbers are TypeSafe's own. Agrici's evaluation is one site judged against a second model, not humans. Your 50 labels are the only accuracy that counts. None of this promises a position or a date.

Sources: Paul Vengeons, "How to use Opus 5.5 + Jev for SEO so well it feels illegal" (https://x.com/VengeonsP/status/2112114728596070486, 2026-10-19); Daniel Agrici, jev-seo (https://github.com/AgriciDaniel/jev-seo, MIT).
