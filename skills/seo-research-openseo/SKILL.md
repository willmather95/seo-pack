---
name: seo-research-openseo
description: Use when an SEO seat needs real market data beyond Search Console (keyword volume and difficulty, competitor keyword gaps, live SERPs, backlinks, rank tracking, AI-answer citations) from the self-hosted OpenSEO MCP, or when running the full weekly research loop per site (GSC + OpenSEO + PostHog -> code builds candidates -> Jev scores -> Opus writes -> owner approves -> rank tracking measures). Holds the exact OpenSEO tool names, DataForSEO cost per step, the per-site dollar cap script, the named Cody Schneider and Neil Patel plays, and a client-ready site config for MMS.
---
# SEO research with OpenSEO

One job: feed `seo-loop` real market data every week, inside a hard dollar cap, so each pick is backed by demand, a beatable SERP and a conversion path.
Search Console shows what we already rank for. OpenSEO shows what we don't: volume, difficulty, who ranks, why, and who AI answers cite. PostHog shows what makes money.

## 0. Setup (once per site or client)
- Server: `https://<your-openseo-host>/mcp` (your own self-hosted OpenSEO, behind an access gate with an owner login). Grok Bot seats call it as the `user-openseo` connector. Claude Code and Codex add the same URL and sign in through localhost OAuth. Access setup (per @rrmdp, x.com/rrmdp/status/2112874674300289351): Cloudflare > Zero Trust > Access controls > Applications > Edit the OpenSEO app > Additional settings > OAuth, then turn on 1) Managed OAuth, 2) Allow localhost clients, 3) Allow loopback clients.
- Data: DataForSEO, pay per call, one shared account for every site. Key `DATAFORSEO_API_KEY` lives in the env only. Never print it.
- Fill `references/site-config-template.md` as `logs/<site>/openseo/CONFIG.md`. One file per site or client. Without it, stop.
- In OpenSEO: `list_projects` -> `create_project` (name, domain, locationCode 2840 US, en). Then `update_project_context` with the offer, conversion, competitors and key pages from the site file. Both are free.
- Connect Search Console in OpenSEO when the owner can sign in. Until then, use our own GSC export scripts. Same data.

## 1. Rules (on top of seo-loop's hard rules)
1. **Four roles.** Real data finds (GSC, OpenSEO, PostHog). Code counts and joins. Jev judges one narrow question per row (`jev-seo-campaign`, 50-row hand check before anything acts). Opus writes. The writer never grades itself.
2. **Cap in code.** Before any paid call: `scripts/openseo_budget.py start` with the plan. Exit 3 = over cap, do not call. After: `end`, which logs the real spend from the balance change. Run one site at a time.
3. **Free first.** Read saved data before paying: `list_saved_keywords`, `get_rank_tracker`, `get_audit_issues`, `list_reports`. OpenSEO caches domain calls for 12 hours. Reuse them.
4. **No schedules without the owner's yes.** Rank tracker and AI visibility schedules spend every run. Default: rank tracker weekly at most, AI visibility schedule OFF. Always call `estimate_rank_tracker_cost` or `estimate_ai_visibility_cost` first and show the number.
5. **Owner approves anything public.** OpenSEO's internal state (projects, saved keywords, private reports) is fine to write. Pages, outreach, listing edits, `submit_indexnow_urls` (only after a shipped, approved page) and `set_report_sharing` wait for a yes.
6. **Code veto stays.** Never remove, merge or noindex a page of 600+ words. 90-day WAIT on changed pages.
7. **Receipts.** Save each OpenSEO result as dated JSON or CSV in `logs/<site>/openseo/YYYY-MM-DD/`. Every number in a brief points to one.

## 2. Tool map and cost (raw DataForSEO, self-hosted, checked 2026-10-21)
| Need | OpenSEO tool | Cost per call |
|---|---|---|
| What we rank for | `get_search_console_performance`, `inspect_urls` | free |
| GSC 4-20 joined to GA4 outcomes | `get_search_opportunities` (needs GSC + GA4 in OpenSEO) | free |
| Volume, KD, intent, CPC for known terms | `get_keyword_metrics` (up to 700 terms) | $0.012 + $0.00012/term (300 terms = $0.05) |
| New ideas from seeds | `research_keywords` (1-5 seeds) | ~$0.04/seed, up to $0.10 with fallback, +$0.09 local volume |
| A domain's footprint | `get_domain_overview` | ~$0.08-0.25 |
| Keywords a domain ranks for | `get_ranked_keywords`, `get_domain_keyword_suggestions` | $0.012 + $0.00012/row (200 rows = $0.036) |
| Who really competes | `find_serp_competitors` | $0.012 + $0.00012/row |
| Live top 10-20 | `get_serp_results` (1-10 terms) | ~$0.002/term |
| Backlinks summary / rows | `get_backlinks_overview`, `get_backlinks_profile` | $0.024 + $0.000036/row |
| Site crawl and issues | `run_site_audit` then `get_audit_issues`, `get_audit_pages` | crawl free, Lighthouse ~$0.005/page |
| Rank tracking | `create_rank_tracker`, `add_rank_tracking_keywords`, `estimate_rank_tracker_cost`, `run_rank_tracker`, `get_rank_tracker` | $0.0006/term queued, $0.002 live, up to 3x with retries |
| Local pack | `get_local_rank_grid`, `get_local_serp_results`, `search_local_businesses`, `get_business_profile`, `get_business_reviews` | grid $0.002/point (5x5 = $0.05), profile $0.005, reviews ~$0.004-0.01 |
| AI answers | `research_ai_visibility_prompts`, `explore_prompt`, `save_ai_visibility_tracker`, `estimate_ai_visibility_cost`, `run_ai_visibility_check`, `get_ai_visibility_results`, `get_ai_visibility_sources`, `get_ai_visibility_trend` | prompt research ~$0.10/request; explore ~$0.04-0.18/answer; tracked answer $0.0012 queued, $0.004 live |
| Keep findings | `save_keywords`, `save_report`, `update_project_context` | free |

## 3. The weekly loop (per site, Monday)
1. **Gather, free.** GSC 28 days query x page. PostHog: conversions by landing page (Lively clicks, booked calls, signups). Saved OpenSEO keywords and the rank tracker. Code joins them into `pages.csv` (page, queries, clicks, position, conversions, last changed).
2. **Hydrate, cheap.** Send every GSC query with 20+ impressions plus last week's gap terms to `get_keyword_metrics` in one call. About $0.05.
3. **Build candidates, code only.** Each row gets a play tag (section 4), volume, KD, current position, conversions on the page, last-changed date. Code drops WAIT pages, terms with no volume and no impressions, and KD far above our authority band (DR under 20: KD up to ~20; 20-40: up to ~40).
4. **Check the SERP.** For the top 10 candidates only, `get_serp_results`. Code counts page types and exact-keyword titles. Jev prompt 7 labels each result type. About $0.02.
5. **Jev scores.** Buyer noul (prompt 4), category choice (prompt 5), page-fit score (prompt 6). For gap terms add the noul "someone typing this could become a customer of ours" with the site file's buyer words. Calibrate each new question on 50 hand-labeled rows first.
6. **Pick one.** Code ranks by value: conversions on the page or the buyer probability, times reachable position gain, minus effort. The seat writes one paragraph: the pick, the play and the receipts. One change per site per week. Defects are uncapped.
7. **Opus writes.** A brief or draft through `seo-page`, with the SERP read and the one angle the top 3 miss. Draft gate (prompt 11) before the owner sees it.
8. **Owner approves.** Exact version, yes or no. A no becomes a line in the site's rules file.
9. **Measure.** Add the target term and 3-5 close variants to the rank tracker. Recheck at day 7 and day 28. Log rank, clicks, conversions and spend in the site log.
10. **Links lane.** Move one link prospect forward one step (play 6). Not the week's change.
Typical weekly spend: $0.20-0.40 per site.

## 4. Named plays (pick the one that fits the candidate)
1. **Striking distance (Neil Patel).** Terms in positions 4-20 with real volume. Position drop = better page. CTR drop at the same position = better title. Tools: GSC, `get_keyword_metrics`, `get_serp_results`.
2. **Competitor keyword gap (Neil Patel).** `find_serp_competitors` on 20 money terms names who really competes. `get_ranked_keywords` on the top 3 (maxRank 20, excludeBrandTerms). Code keeps terms they rank for and we don't. Jev buyer noul. Easiest first: terms where we sit on page 2-3. About $0.15 a month per site.
3. **Alternatives and comparison pages (Cody Schneider).** Bottom-funnel terms: "x vs y", "x alternative", "x review", "x pricing", "best x for y". Pull volume, read every page-1 result in full, then write a fair, dated page. A two-sentence verdict up top. A real table of named options with prices, limits and who each is best for. Say when the other option wins. Buyer FAQs. The slug is the exact term; the term goes in the H1, first paragraph, title and meta. Get it indexed the same day. Check AI citations at 2 weeks and rewrite what isn't showing. Add the owner's own take (a 20-minute interview transcript) so the page has something no one can copy. Our pace rule wins over his "1 a day, then 10".
4. **Content refresh and decay (Neil Patel).** Code flags pages with clicks down 30%+ over 28 vs 28 days or 90 vs 90, not changed in 90 days. Refresh with current facts, better structure, missing subtopics from the SERP read, and FAQs. Consolidate only below 600 words, with the owner's yes. A refresh of a proven page usually beats a new page.
5. **Topic clusters (Neil Patel).** 3-5 pillars per site, 4-8 cluster pages each, mapped with `seo-keyword-map` and OpenSEO's `keyword-clustering` skill. Link cluster pages to the pillar with clear 2-5 word anchors. Do the links after the pages exist. Local businesses: the service x town grid is the cluster.
6. **Link prospecting (Neil Patel).** Three lanes, monthly. (a) Broken competitor links: `get_backlinks_profile` on a competitor, filter lost or broken targets, check the old page in the Wayback Machine, offer our matching page. (b) Unlinked mentions: search the brand name, find pages that name us with no link, ask for one. (c) Resource and list pages: `get_serp_results` on "<topic> resources", "best <category>", "<competitor> alternatives". Jev prompt 13 scores fit. OpenSEO's `link-prospecting` skill has the query patterns. Never invent an email. Every send waits for the owner.
7. **AI answer visibility (Cody Schneider).** Citations, not dashboards, move AI answers. Monthly: pick 5-10 real buyer prompts. Proxy: GSC queries of 50+ characters with high impressions and few clicks often come from AI fan-out. Run one manual check (`estimate_ai_visibility_cost` -> owner sees the price -> `run_ai_visibility_check`, queued). Then `get_ai_visibility_sources`: the 1-3 pages the answers lean on are the targets. Get onto those lists and reviews (play 6) and make our own comparison page (play 3). Schedule stays off until a monthly check shows movement worth tracking.
8. **Programmatic pages (Cody Schneider), gated.** Only when each page carries its own real data (HSA provider fees by provider, service x town with real local facts, event weekends by town). Build 3 by hand, pass the draft gate, ship them, wait for indexing and clicks, then template. No swapped-name pages. Hubs must be indexed first.
9. **Reddit and forums (Neil Patel's crawl, walk, run).** Listen first: `get_serp_results` shows which threads rank for our terms. Note the questions for pages and FAQs. No posting or commenting without the owner's yes on each one. Third-party lists beat Reddit for AI citations.

## 5. Monthly add-ons (first Monday)
`run_site_audit` (Lighthouse on 10 pages, about $0.05) -> `get_audit_issues` -> defects into the loop. `get_domain_overview` for us and 3 competitors (about $1). `get_backlinks_overview` for us and the top competitor. Play 2, play 6 and play 7. Jev calibration (prompt 18). Save one report with `save_report` (private) and put the top 3 wins in the site log.

## 6. Caps (proposed, owner sets the real numbers in CONFIG.md)
- Default **$10 per site per month**, **$3 per run**. Typical use is $2-4 per site per month. Four owned sites: $40 a month ceiling, about $12-16 typical.
- AI visibility schedules **OFF**. Rank tracker: up to 25 terms, weekly, queued (about $0.06 a month at queued price, $0.20 worst case).
- Local client add-on: 5x5 grid on 5 terms monthly (about $0.25), reviews for the client and 3 rivals (about $0.05).
- Balance under $5: seats stop paid calls and tell the lead seat, who tells the owner.

## 7. Client mode (agencies)
One OpenSEO project per client, one CONFIG.md per client in `logs/clients/<client>/openseo/`. Client caps are separate and billed into the retainer. Proof is the client's own numbers only. Never mix data between projects. Add the client's login to the access gate only with the owner's yes. Sales copy: never say "AI".

## 8. Hand-offs
`seo-loop` runs the week. `seo-keyword-map` turns gap terms into a page plan. `seo-page` writes. `seo-local` handles the map pack. `seo-authority` runs links and AI citations. `jev-seo-campaign` scores rows. OpenSEO's own skills (in its repo `.agents/skills`: keyword-research, competitor-analysis, keyword-clustering, link-prospecting, ai-visibility-audit, competitive-landscape, ai-prompt-research) are good call orders. Our caps and gates win where they differ.

Sources: Cody Schneider on comparison pages AI cites (https://www.linkedin.com/posts/codyxschneider_a-page-called-x-vs-y-gets-quoted-in-ai-activity-7512466582313431040-sM7n) and SaaS SEO playbook (https://www.linkedin.com/posts/codyxschneider_saas-seo-playbook-in-the-age-of-ai-use-perplexity-activity-7350926635040198657-HqK_); In the Pit, citations episode with Shawn Schneider (https://podbay.fm/p/in-the-pit-with-cody-schneider-or-marketing-or-growth-or-startups/e/1766428200); Neil Patel on content gaps (https://neilpatel.com/blog/content-gaps/), content decay (https://neilpatel.com/blog/content-decay/), advanced SEO incl. striking distance and unlinked mentions (https://neilpatel.com/blog/10-advanced-seo-techniques-thatll-double-your-search-traffic/), broken link building (https://neilpatel.com/blog/ecommerce-link-building/), topic clusters (https://neilpatel.com/blog/topic-clusters/), Reddit SEO (https://neilpatel.com/blog/reddit-seo/). OpenSEO: github.com/every-app/open-seo, prices from src/server/lib/dataforseo/pricing.ts and the DataForSEO price table.
