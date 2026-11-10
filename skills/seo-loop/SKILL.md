---
name: seo-loop
description: The one front door for SEO and AI-answer (AEO) work on a site you own or serve. Weekly mode reads the site file, pulls real search and conversion data, picks one change, audits in four passes, drafts behind an approval gate, and logs results. Build mode (new site or product, keyword-first, full overhaul, "seo god") runs the keyword gate, revenue spine and build phases. Fires on "seo loop", "seo god", "god mode SEO", "full SEO program", "SEO from scratch", "keyword-first", "build a product around a keyword", "what should we do for SEO this week". The hub that calls seo-keyword-map, seo-page, seo-local, seo-authority and seo-research-openseo. For a one-page diagnostic audit, use seo-audit.
---
# SEO loop

One job: move one site toward more conversions from search, one change at a time, with receipts.

## Pick the mode
- **Weekly mode** (default): the site exists and has a site file. Follow the steps below.
- **Build mode:** no site or product yet, a keyword-first idea, a full overhaul, or the owner asks for a build sprint ("seo god"). Follow `references/build-mode.md`, then switch to weekly mode once the revenue spine ships.
- Both modes use the same hard rules, the owner gate and the effort order in `references/tactic-ladder.md`.

## Before you start
1. Find the site file. Look in this order: `SEO-SITE.md` in the site's repo root, then `sites/<site>.md` inside this skill's folder. If none exists, copy `sites/_template.md` and fill it in with the owner. Never guess the conversion. Folder paths in site files are relative to the shared workspace root (the folder that holds the site logs).
2. Read the site's mistakes file and last log entry if they exist (the site file says where).
3. No conversion named = stop. Define it first. Rankings are a means; bookings, signups or leads are the score.
4. **Tracking before judging.** Check that calls, form fills, signups or bookings are really counted (test event seen in the tool, consent gaps noted). If tracking is missing or undercounts, fixing it is a defect for this week. Until it works, report rank and clicks only, and never call a change a win or a loss on conversions.
5. **PostHog on every site.** The growth plan is to learn how people really use the site and change it from that data, before they complain or rankings slip. Every site in this loop runs PostHog: pageviews, autocapture, session replay and the conversion as a named event. No PostHog project in the site file = installing it is this week's defect (owner says yes to the deploy). Read it through the PostHog MCP; recipe in `references/posthog-behavior.md`.

## Hard rules
1. **Receipts or it didn't happen.** Every number comes from a real source: Search Console, analytics, a keyword tool export, a crawl, a live page. Keep the file or URL. Never invent volumes, rankings, traffic, DR or results.
2. **One change per site per week.** One killer page or one main change. Build mode works in owner-approved batches instead. Defects are not capped: a wrong fact, a broken page or a bad redirect gets its own fix now.
3. **The owner approves anything public.** Drafts, audits and draft PRs are fine. Merge, deploy, publish, new pages, listing edits, outreach sends, purchases and form submits all wait for the owner's yes on the exact item. No reply means hold.
4. **Winnable top 3**, not "somewhere on page one". Pick queries where the top results are beatable.
5. **No spam.** No bought links, link swaps, PBNs, keyword-stuffed anchors, thin scaled pages, or swapped-name location pages. No thin parasite posts for owned brands.
6. **Human copy.** Plain, short, true. Grade 8-9. No em dashes, no AI tells, no invented quotes, reviews or stats.
7. **Four roles.** Real data finds, code counts, Jev judges, the writing model writes. The writer never grades its own work. For any decision over about 50 rows, use `jev-seo-campaign`.
8. **90-day wait.** After a real change, leave the page alone about 90 days. Code marks any page changed in the last 90 days WAIT, whatever the numbers say. The next move after a publish is another keyword.
9. **Model limits.** The model sorts and drafts. It cannot see rankings, local results or dashboards unless you hand it exports. A person decides strategy, link targets and anything sensitive.

## Weekly steps
1. **Gather.** Pull 28 days of Search Console (query x page: clicks, impressions, CTR, position) and conversions by landing page. Note index coverage and sitemap status. Save the export with a date. Then add market data from OpenSEO (volume, difficulty, competitor gap, SERP, rank tracker) inside the site's dollar cap, per `seo-research-openseo`. Search Console alone only shows what we already rank for. Then pull the same 28 days from PostHog for search visitors (referrer is a search engine or AI answer): by landing page, the conversion rate, where they drop off, scroll depth, rage and dead clicks, and the top exit pages. Search Console shows how people find the site; PostHog shows what they do once they land.
2. **Pick one change.** Work the ladder in `references/tactic-ladder.md`: buyer pages, topical depth, new information, refreshes and internal links come before outreach and polish. For pages that lost clicks, compare the same weeks last year first (seasonal dips are not defects). code checks first: did the position drop (needs a better page) or the CTR drop at the same position (needs a better title)? Skip WAIT pages. A page that already ranks and gets search visits but converts badly in PostHog (big drop-off, rage clicks, short scroll, visitors leave before the CTA) is a strong pick: fixing the page is often worth more than winning a new keyword. Score candidates on: conversion value, winnable position (often 4-15 already), effort, risk. Write the pick and the evidence in one paragraph. Use a decision model or rubric if the site file names one.
3. **Four-pass check** on the chosen page:
   - **Access and index:** status code, canonical, robots, in sitemap, indexed, server-rendered text, mobile speed. Rank crawl issues by impact on rankings and leads, with a one-line fix each.
   - **Competitors:** read the top 3 results in full. Note length, headings, shared subtopics, tables, FAQs. Find the one angle none of them cover.
   - **AI answers:** if an AI Overview or chatbot answer exists for the query, note who is cited and the named slots ("best for X"). For a serious AEO push, track it 7 days first (see seo-authority).
   - **Conversion path:** one clear next step, tracked. Check it on a phone. Watch 3-5 PostHog replays of search visitors on this page and write down where they stall, what they click that isn't a link, and where they leave.
4. **Recommend one change** with evidence. Use the right skill to build it:
   - Market data, competitor gap, comparison pages, refresh, link prospects, AI citations: `seo-research-openseo`
   - New keyword list or page plan: `seo-keyword-map`
   - Page write, rewrite, title/meta, schema, free tool: `seo-page`
   - Map pack, reviews, citations (real-location businesses): `seo-local`
   - Links, mentions, AI-answer citations: `seo-authority`
   - Judging many rows (full GSC export, page pairs, link candidates, prospects, draft gate): `jev-seo-campaign`
5. **Links lane.** Every week, move at least one link target forward one step (`seo-authority`). It does not count as the week's change. Plays: `seo-authority/references/link-plays.md`. UTM-tag every link we place off-site.
6. **Draft and gate.** Open a draft PR or draft doc. Run the pre-ship checklist below. Ask the owner for a yes on that exact version.
7. **Log.** Append to the site log: date, change, evidence, links lane step, what to recheck. After ship: request indexing, then recheck at day 7 and day 28 (rank, clicks, conversions, and the PostHog conversion rate and drop-off for search visitors on that page, against the baseline).
8. **Snapshot a baseline at every ship.** Save the dated before numbers (GSC export, indexed count, conversions, PostHog funnel for the page) next to the ship receipt, per `references/seo-case-study.md`, so case studies write themselves.

## Pre-ship checklist
- Facts match sources, with an "as of" date where numbers can change.
- One H1. Title and meta written. Canonical to itself. In sitemap.
- Schema validates and matches visible text word for word.
- Links return 200. Internal links in from 3-5 strong pages, placed beside the question they answer, with anchors that name what opens next. The page links to its money page.
- Phone check at 390px: no sideways scroll, CTA visible.
- Human-copy pass done. No em dashes.
- Tracking fires for the conversion, in PostHog as well as the site's main analytics (event seen in PostHog Activity).
- Draft gate passed (jev-seo-campaign prompt 11): intent, original, no unsupported claims, title and H1 match. The gate never publishes; the owner does.
- After ship, a script checks it, not the agent's word: URL returns 200, page is in the live sitemap, its internal links are live, the deploy is on the right branch.

## Adding a new SEO lesson later
Save the source note. Patch the one skill it belongs in with only what transfers. Do not make a new skill per post.
