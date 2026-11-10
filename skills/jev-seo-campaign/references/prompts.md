# Campaign prompts (adapted)

Adapted from Paul Vengeons' 18 prompts (2026-10-19). "Using ChatSEO" became "from real data": our GSC API scripts, a live SERP read, a crawl, or free backlink sources. Paid tools only with the owner's yes. `<site>` is the site file in `seo-loop/sites/`.
Every Jev call: model `jev-1.13.0`, all questions for a row in one request, run through `scripts/jev_rows.py` with a cap and a cost log line.

Question file shape for `jev_rows.py`:
```json
{"workflow": "gsc-triage",
 "questions": {"<id>": {"type": "noul|choice|score", "instructions": "...", "criteria": {...} }},
 "bands": {"<id>": {"act": 0.8, "drop": 0.2}},
 "veto_values": {"<id>": ["merge_or_remove"]}}
```
Rows file: one JSON object per line: `{"id": "...", "state": {...}, "meta": {...numbers code keeps, never sent...}}`.
Noul criteria are `{"true": "...", "false": "..."}`. Choice criteria are `{"option": "what it means"}`. Score criteria are a list of levels, low to high.

## Prompt 0: write a Jev question (before any workflow over 50 rows)
1. Ask the owner: what is the decision, what happens for each answer, what would a human expert look at to decide.
2. Pick the type: noul for yes/no, choice for 3-10 named outcomes, score for a level on a scale.
3. Write a POSITIVE statement: a high probability must mean yes to something good. Never a negation.
4. Criteria for true and false (or one line per option or level) in the site file's own words.
5. Choice: always add "other".
6. State fields: the minimum a human would read. No page bodies unless the decision is about the body.
7. Threshold plan: act above X, review between Y and X, drop below Y. Start at 0.9 / 0.5 and calibrate on 50 rows.
8. Never a question that needs counting, arithmetic, or comparing numbers or dates. The script computes it and passes the result as text.

## Prompts 1-2: context and rules (once per site)
Our versions already exist: the site file (`seo-loop/sites/<site>.md`) and the team rules or MISTAKES file. Make sure the site file has: what we sell, to whom, at what price; the 3 pages that make money; who ranks next to us; DR and referring domains from real data (never estimated); target markets; and two sentences about the business for Jev state.
Add this rules block if missing:
- ALLOW: read GSC, analytics, crawls; call Jev on read-only judgments; write drafts, scripts, reports.
- REQUIRE OWNER YES: publish or edit a live page; change a title that already gets clicks; redirect, merge, noindex or delete; send any email.
- BLOCK: act on a Jev answer below the calibrated threshold; let Jev decide a delete, redirect or merge alone; ask Jev to count or compare numbers or dates.
- Every rejection: write the reason at the bottom and read it before the next task.

## Prompt 3: which battles are open (code only)
From real data, get our DR and referring domains and the same for the 3 sites on our top business queries. In a script: DR under 20 = long tail only; 20-40 = mid tail; over 40 = head terms in reach. Under 50 referring domains: say so in the first line and list 5 free on-topic links to start this week (niche directories, partners, communities, resource pages).

## Prompt 4: full Search Console triage
Script: export every query for 16 months (query, clicks, impressions, position). One noul per query. State = the site's two sentences + the query. Nothing else. Keep 0.8+, drop 0.2-, tag the rest "review". Write keep.csv, drop.csv, review.csv with the probability next to the GSC numbers. Print the 40 review rows with most impressions for a human. Never ask Jev about clicks or positions. Run 50 rows first and stop for labels.
```json
{"workflow": "gsc-triage",
 "questions": {"buyer": {"type": "noul",
   "instructions": "Someone typing `query` into Google could buy what the business in `site` sells.",
   "criteria": {"true": "They want a product, a provider, a price, a comparison or an alternative in our category.",
                "false": "Unrelated topic, academic, a job search, or another brand's login page."}}},
 "bands": {"buyer": {"act": 0.8, "drop": 0.2}}}
```
Rewrite "true" in the site's words (see SKILL.md sec. 8). If the keep pile is huge or full of how-to queries, the true criteria are too loose. Check: sort keep by impressions, read the top 30; you should want 27 of them.

## Prompt 5: sort keepers into categories
```json
{"workflow": "categories",
 "questions": {"category": {"type": "choice", "instructions": "Which kind of search is `query`?",
   "criteria": {"alternative": "\"<competitor> alternative\", \"free <competitor>\"",
                "comparison": "\"<a> vs <b>\", \"<a> or <b>\"",
                "provider_city": "a service plus a place",
                "best_list": "\"best <offer>\", \"top <offer>\", with or without a year",
                "price_review": "price, cost, fees, review, \"is it worth it\"",
                "how_to": "someone learning to do it themselves",
                "other": "none of these fits"}}},
 "bands": {"category": {"act": 0.8}}}
```
Code: group by category, sum impressions, count queries, write categories.md (one table per category, by impressions), mark queries where we already have a page. Priority = business potential x volume x accessibility, reasoned by the writer, not Jev.

## Prompt 6: quick wins, and protect what ranks
Code: from keep.csv, query + page pairs at position 5-20 with 100+ impressions over 90 days. Exact page AND exact query, never the site average.
```json
{"workflow": "quick-wins",
 "questions": {"answers": {"type": "score", "instructions": "How well does the page in `page` answer the query in `query`?",
   "criteria": ["It doesn't answer it", "It partly answers it", "It answers it directly"]}},
 "bands": {"answers": {"act": 0.8}}}
```
State = query + the page's title, H1 and first 150 words. Score 2: page is right, fix the title (prompt 9). Score 1: brief the missing part. Score 0: ranks by accident; plan a NEW page and leave the old one alone. Before touching any page, list the queries it already gets clicks for.

## Cannibalization: page pairs
Code: from the query + page export, every pair of OUR pages sharing at least one query with impressions.
```json
{"workflow": "cannibal",
 "questions": {
  "same_intent": {"type": "noul", "instructions": "Page `a` and page `b` answer the same need for the same reader.",
    "criteria": {"true": "A searcher would be happy with either page for the shared queries.", "false": "They serve different needs or readers."}},
  "same_angle": {"type": "noul", "instructions": "Page `a` and page `b` take the same angle: same format, same audience, same promise.",
    "criteria": {"true": "Same format, audience and promise.", "false": "Different format, audience or promise."}}},
 "bands": {"same_intent": {"act": 0.9, "drop": 0.2}, "same_angle": {"act": 0.9, "drop": 0.2}}}
```
State per page: title, H1, meta description, the 5 shared queries. Not bodies. Flag only when BOTH are 0.9+. Do not merge anything. Write cannibal.md with the pairs, their clicks, which gets more. The owner decides.

## Prompt 7: read the SERP first
Live top 10 for the keyword. One choice per result: service_page, product_page, category_page, comparison, ranking_list, article, forum, video, other. State = title, URL, snippet. Code counts the types and how many top-3 titles contain the keyword word for word. None = say it first: that's the opening.

## Prompt 8: the brief (writer)
Secondary keywords: other queries the #1 page ranks top 5 for, plus our queries on the topic with impressions but few clicks. brief.md: create or optimize and which URL (check we don't already have it), primary and secondary keywords, the searcher's questions in SERP order, ONE thing the top 3 don't have (our own number, a real screenshot, a calculator, a video, a first-person verdict), title and H1. No "one thing" = stop and ask the owner.

## Prompt 9: the title
Writer: 5 options, keyword first word for word, a colon, one promise matched to intent (a count, a proof or a scope), the current year on rankings, comparisons, reviews and "best". Code: pixel width under 600 px with the SERP font, not a character count. Jev, one score per option: "How likely is a searcher who typed `keyword` to click `option` among the 10 titles in `serp`?" Levels 0-3. Return the top 2 with score and width. The owner picks. GSC says the truth in 90 days.

## Prompt 10: first page by hand, then the template
The first page of a category is built by hand (up to an hour). Then template.html (same design, title pattern, H1, original element, FAQ, CTA) and process.md: build on the template; structured data that matches the page; 3-5 internal links (prompt 12); sitemap and hreflang; run prompt 11 before anything goes live. Read process.md before every page. One page a day is the ceiling.

## Prompt 11: the pre-publish gate
```json
{"workflow": "draft-gate",
 "questions": {
  "intent": {"type": "noul", "instructions": "The draft answers the need of someone typing `keyword`, in the format the SERP shows.",
    "criteria": {"true": "Format and content match what the top results show the searcher wants.", "false": "Wrong format or off the need."}},
  "original": {"type": "noul", "instructions": "The draft contains something the 3 summaries in `top3` don't have: our own data, a real screenshot, a tool, a first-person verdict.",
    "criteria": {"true": "At least one element the top 3 lack.", "false": "Nothing the top 3 don't already have."}},
  "unsupported": {"type": "noul", "instructions": "The draft states a figure or a fact with no source and no first-hand origin.",
    "criteria": {"true": "At least one figure or fact has no source.", "false": "Every figure and fact has a source or first-hand origin."}},
  "title_h1": {"type": "noul", "instructions": "The title and the H1 of the draft promise the same thing.",
    "criteria": {"true": "Same promise.", "false": "Different promises."}},
  "verdict": {"type": "choice", "instructions": "What should happen to the draft before it goes live?",
    "criteria": {"publish": "Ready as is", "revise": "Small fixes needed", "rewrite": "Wrong approach", "other": "None of these"}}},
 "gate": {"pass_if": {"verdict": ["publish", 0.9], "intent": [">=", 0.9], "original": [">=", 0.9], "unsupported": ["<=", 0.1]}}}
```
State = the draft, the brief, a 3-line summary of each top-3 result. Anything that fails goes to the owner with the failing question named. Counting words, H2s or keyword mentions is done in code. Passing the gate is not publishing: the owner still says yes.
Health sites add: noul "no_promise": "The draft makes no promise of a medical outcome or result." Pass only at 0.9+.

## Prompt 12: internal links
Script `link_plan.py` for a target URL and keyword: crawl our site (or load the last crawl): URL, title, H1, folder, existing internal links. Code pre-filter: same folder or category, not already linking to the target, max 100. One score per candidate: "How closely does the page in `candidate` cover the same topic as `target`?" Levels: 0 unrelated, 1 adjacent, 2 same topic. State = both titles, both H1s, the candidate's first 150 words. Keep score-2 pages, highest probability first, top 8. Writer: find the paragraph where the link reads naturally and write ONE sentence with the exact anchor; show before and after. Never the same anchor for two different pages. Nothing changes on the live site until the owner says yes.

## Prompt 12b: sitewide links from best-ranking queries (added 2026-10-26)
Use for a sitewide internal-link pass on any site with published articles. Input: Search Console for the last 3 months (GSC connector, the box DuckDB load, or an export), plus the site's repo or CMS connector.
1. For each article, find the queries where it ranks best (position 1-10, decent impressions). Those are its target anchors.
2. Go through every published post. Wherever the text naturally mentions another article's top query (or a close variant), turn that phrase into a link to that article.
3. Rules:
   - Max 3-5 new internal links per post, spread through the body (not in headings, the intro sentence, or existing links).
   - Never link a post to itself, and link each target only once per post.
   - Anchor text must read naturally. Don't rewrite sentences just to force a keyword in.
   - Prioritize sending links to pages ranking 4-15 (they gain the most).
   - Never use the same anchor for two different targets (same rule as Prompt 12).
4. Before changing anything, show a table: source post, anchor text, target URL, target's query and position. Wait for the owner's OK.
5. After approval, make the edits (a draft PR on the site repo, or through the CMS connector), then give a changelog so every link can be reverted. The merge still needs the owner's yes at the exact SHA.
Prompt 12 picks links for one target by topic. 12b runs sitewide by ranking query. Run 12b monthly, or after a GSC triage (Prompt 4).

## Prompt 13: filter link prospects
Sites linking to the 3 pages ranking on the keyword, with their organic traffic and top pages (free sources first). Code: drop every site with no real organic traffic on its own topic. Jev, one score: "How relevant is the site in `site` as a source of a link to the page in `our_page`?" Levels: 0 off topic, 1 related, 2 same topic and same audience. State = site title, its 3 top pages, 2 sentences about our page. prospects.csv by P(level 2). Never invent an email; blank if none was found.

## Prompt 14: size the links (code)
Referring domains to each top-3 PAGE (not domain) and their anchor mix (brand, URL, exact, other). Give the range and the number of links that puts our page inside it, not above it. Free placements first (resource pages, communities, dead-link replacement), paid last and only with the owner's yes. A page with 12 RDs is catchable even when its domain has thousands.

## Prompt 15: GEO, who is in the evaluation lists
From best_list, price_review and alternative: top 10 queries each, plus a "best <offer> <year>" version. Live top 10 for each. Two nouls per result: third_party_list ("This page ranks or lists several providers, and it is not written by one of them about itself.") and lists_us ("Our brand appears in this page's list."). State = title, URL, snippet, brand names found on the page. Write geo.md.

## Prompt 16: get into other people's lists (writer, drafts only)
For each list we're missing from: author and contact from the page; page updated in the last 12 months and already lists a competitor. Short honest email: what the list covers well, what we do that listed options don't, a free way to judge, and "if it doesn't belong in the piece, ignore this". Our rule: no swaps or barter placements (seo-loop rule 5). Nothing sends without the owner's yes. Never rank ourselves first in our own lists.

## Prompt 17: Monday review
1. Last 28 days vs the previous 28 (GSC is 2-3 days late): pages that gained impressions, pages that lost clicks, queries new to the top 10.
2. Code: any page edited in the last 90 days is WAIT. Not touched.
3. Code, for pages that lost clicks: lost position (needs a better page) or lost CTR at the same position (needs a better title)? Never the same fix.
4. Prompt 4 on NEW queries only, then prompt 5 on the keepers.
5. review-<date>.md: 5 actions ranked by business value, not traffic.

## Prompt 18: monthly calibration
Take 30 random rows each Jev workflow auto-approved this month and 20 it sent to review. Show them to the owner without Jev's answer. The owner labels. Compare (`jev_rows.py calibrate`), report disagreements per workflow and whether a threshold should move. Write the result in the rules file.

## Local: reviews (map-pack businesses)
Export our Google reviews (text, stars, date) and those of the 3 local-pack businesses on "<service> <city>".
```json
{"workflow": "reviews",
 "questions": {"describes": {"type": "choice", "instructions": "What does the review in `review` describe?",
   "criteria": {"names_service_and_place": "Names the service and the town or area", "names_service": "Names the service only",
                "generic_praise": "Praise with no service named", "complaint": "A complaint", "other": "None of these"}}},
 "bands": {"describes": {"act": 0.8}}}
```
State = the review text only. Code: share of each option for us and each rival, and services named most in THEIR reviews that never appear in ours. Writer: a better review request asking patients to say what was done and where (never scripted words, never paid or gated reviews). Never keywords in our replies; health replies never confirm someone is a patient (seo-local).
