---
name: seo-page
description: Use when writing, rewriting or auditing one page for search and AI answers. Covers fact-locked drafting, service and treatment pages, "best X" pages, location pages, free-tool pages, titles and meta, schema, and the human-copy gate. One page at a time, drafts only until the owner approves.
---
# SEO page

One job: make one page the best answer for its query, using only true facts.

## 1. Inputs before writing
- The page row from the keyword map (primary term, supporting terms, page type).
- The top 3 results, read in full: headings, length, tables, FAQs, what they miss.
- A **facts sheet**: verified facts with sources and "as of" dates, approved claims, prices, who does the work and their credentials. Regulated topics (health, tax, money, legal) need a primary source (for example the IRS publication, the label, the license).
- Real questions: "People also ask", Search Console queries, support inbox, front-desk questions.

## 1b. Information gain (before drafting)
The page must add something the top 10 lack. Find the gap in this order:
1. Read the top 10 and list what they already answer.
2. Read YouTube transcripts and forum, Reddit and review complaints for questions none of them answer.
3. Fill it with something only we have: our own data, a side-by-side test of the same task across products, or a firsthand example from an interview with the owner or a customer (the model asks, the person answers).
Save the raw notes and calculations. Put the evidence next to each finding on the page so it can be checked. No gap found = no new page; improve an existing one instead.

## 2. The fact lock (use in every drafting prompt)
```
Facts (the only facts you may use): [facts sheet].
Leave out anything you can't confirm from the facts above. If a question can't be answered from them, list it in a note to me instead of answering.
```

## 3. Pick the page type
**Service, treatment or product page** (one per service, one per brand):
- What it treats or solves
- How it works and how long it takes
- Downtime, aftercare or what happens next
- Who it suits, and who should skip it
- Price or starting price (if the owner shares one)
- Who does it, with title and credentials, linked to a bio page
- Real FAQs (4-8)
- One clear next step (book, sign up, start)

**"Best [category] in [year]" page** (comparison and AI-answer pages):
- Named human author with bio and profile link; published and updated dates; refresh every 30-90 days.
- Title = H1. Short intro (under ~95 words) that names the top pick and why.
- 5 key takeaways. A short "what [category] is and is not" section.
- "How we ranked" with 4+ countable criteria.
- One H3 per option: "[Name], best for [use case]", with real numbers (price, fees, ratings with counts). End each with "best suited for".
- An HTML comparison table (never an image) and a "which fits your use case" table.
- FAQ, then one closing CTA.
- Only name yourself the pick where it is true for a stated use case. Disclose affiliate links.

**Buyer pages** (pricing, alternatives, migration, features):
- **Pricing:** every plan, price, limit and trial term on one page, with what happens when the trial ends and what discounts really cost. Trial or demo button beside the terms.
- **Alternatives and switching ("[competitor] alternative"):** the honest reasons people switch, who should stay, and a same-criteria comparison. Never invent a competitor fact; source and date each one.
- **Migration guide ("switch from [competitor]"):** the real steps, what moves and what does not, how long it takes.
- **Feature and integration pages:** show the feature doing the job (screenshot or short video) and answer the objection it removes.

**Location page** (only for places really served):
- Write each one from scratch with local facts: parking, landmarks, drive times, local rules, local examples.
- **Swap test:** if replacing the town name would make the page fit another town, it fails. Rewrite or don't publish.
- Link up to the main service page and across to 2-3 nearby town pages (see seo-keyword-map grid).

**Free-tool page** (calculator, checker, planner):
- No signup or email gate before the result. Few inputs, sensible defaults, instant result.
- Numbers come from cited sources shown next to the result with an "as of" date.
- Works one-handed at 390px. One CTA right after the result.
- Indexable text below the tool: how it works, method, sources, worked example, limits.
- Schema: WebApplication (free, price 0) + FAQPage + BreadcrumbList. Track tool use and CTA clicks.

## 4. Trust on health, money and legal pages
These pages are held to a higher bar. Name the person behind the content and their credentials. Give each expert a bio page (training, licenses, years). Before-and-after photos need written consent, same angle and light, and no promises ("results vary", never "guaranteed").

## 5. On-page basics
- One H1 with the primary term. Primary term in the first ~100 words.
- 3-5 internal links out, and 3-5 strong pages linking in with natural anchors. For a sitewide pass driven by each page's best-ranking GSC queries, use jev-seo-campaign Prompt 12b. 2-3 external links to primary sources.
- Server-rendered or static HTML for all indexable text.
- Mobile first: fast, CTA visible without scrolling.
- If a video answers the query, embed it beside the written steps it shows.
- Check the rendered page (not just source) shows the answer to readers and crawlers.

## 6. Title, meta and H1
Give 3 options each, built from the page's real Search Console queries:
- Title under 60 characters, primary term first, brand suffix per the site file.
- Meta description under 155 characters, says what the reader gets.
- H1 that matches the intent. The owner picks.
- Width: measure the title in pixels in code (under about 600 px with the SERP font), not by counting characters.
- To sort many options, Jev scores each against the current top 10 titles (jev-seo-campaign prompt 9). It sorts; it doesn't know CTR. Search Console tells the truth in 90 days.
- Never change a title that already gets clicks without the owner's yes.

## 7. Schema
Generate JSON-LD only from the facts sheet: Organization or LocalBusiness, Service or Product, Person for authors, Article with dateModified, FAQPage, BreadcrumbList. No ratings or reviews unless they are real and shown on the page. Validate before the PR.

## 8. Gates
1. Human-copy pass: grade 8-9, short sentences, no em dashes, nothing salesy, no invented stats, quotes or reviews.
2. Fact check every claim against the facts sheet.
3. Run the Jev draft gate (jev-seo-campaign prompt 11). Auto-pass only at verdict publish 0.9+, intent 0.9+, original 0.9+ and unsupported 0.1 or below; health pages also need no_promise 0.9+. Word and heading counts happen in code.
4. Run the seo-loop pre-ship checklist.
5. Draft PR or draft doc only. Publishing waits for the owner's yes.

First page of a new category: build it by hand, then save a template and a process file (schema, internal links, sitemap, gate) for the rest. One page a day is a ceiling; two good ones a week is plenty.
