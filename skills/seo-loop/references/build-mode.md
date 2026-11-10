# Build mode (was seo-god)

Use when there is no site or product yet, or the owner asks for a full SEO overhaul or a build sprint. Weekly mode (SKILL.md) takes over once the spine ships. Merged from the old `seo-god` skill on 2026-10-27. Its traffic figures (4.96M, 215K/mo, 54K, 32K/mo) are source claims, not ours.

Where seo-god and the pack disagreed, the pack wins:
- **Free tools:** the result is free and ungated (seo-page). An email can unlock extras after the result (saved report, PDF), never the answer.
- **Counts are ceilings, not quotas.** No "every site gets 20+ comparisons, 3-10 tools, a 45K-page matrix". Build only what keyword data supports. The owner approves each batch.
- **Winners:** name a pick per use case, only where true, with sources (seo-page best-of rules).
- **Receipts, fact lock, owner gate, human copy and the 90-day wait** all still apply.

## Phase -1: Keyword gate (greenfield only)
The keyword picks the product. No build starts until one head keyword clears this gate. Pull numbers from OpenSEO (`seo-research-openseo`); never guess.

| Check | Pass | Why |
|---|---|---|
| Difficulty | KD under 20 | Rankable with launch-level links |
| Volume | Over 500/mo on the head term | Enough demand |
| Long-tail family | 20+ real variants | Each can become a subpage |
| SERP fit | Top 10 shows tools or products, not only articles | Google already rewards the thing we build |
| Zero-click risk | No AI Overview, or one that cites tools | An answer that fully satisfies the query eats the click |
| Money path | Clear paid tier or affiliate route | Traffic with no revenue is a vanity build |

Fewer than 3 candidates pass: stop and report. Thresholds are starting points; tune per niche with data.

Build around the winner:
1. The answer on first load, above the fold. No signup wall.
2. The head term once each in slug, title, H1 and image alt. No stuffing.
3. One subpage per long-tail variant that has its own facts (Phase 3 rules).
4. Free version earns links, paid version earns revenue.

Launch links: Product Hunt and launch reposts (mostly nofollow, enough for KD under 20 only), free directories, communities we are really in, then platform listings (`seo-authority` section 4). Log the build date plus day-90 and month-9 GSC checks in MC. Don't judge the keyword before day 90. Source: Danny Postma, 2023 (his revenue claim, unverified).

## Phase 0: Revenue spine and audit
Map the money pages before tools, programmatic pages or blog posts:
1. Product, service or category pages for direct demand.
2. Comparison, alternatives, pricing and "best for" pages for deciding buyers.
3. Guides that link into the money pages.
4. Nav or hub links to the most important commercial pages.

Match the page type to what the live SERP rewards:

| SERP rewards | Build |
|---|---|
| Category pages | Category page with list, buyer guide, FAQ, internal links |
| Homepages | Homepage copy and metadata aimed at the broad term |
| Product pages | Product page with full specs, real reviews, availability, schema |
| Tools | Working tool with indexable explainer and WebApplication schema |
| Local pack or service pages | Service or area page plus profile alignment (`seo-local`) |
| Comparisons or lists | Comparison page with verdict, table and CTA |

Blog posts support money pages unless the SERP rewards articles.

PostHog ships with the spine, before the first page goes live: pageviews, autocapture, session replay and the conversion as a named event (`references/posthog-behavior.md`). From day one we want to see how search visitors use each page, not guess.

Audit in parallel (subagents where available): site and template map with monetization gaps; keyword gap vs competitors (`seo-research-openseo`); every page sorted rising, stable, declining or dead (Phase 4).

## Phase 1: Free tools
Find them from what buyers repeat: a calculation, a check, a lookup, a spreadsheet they keep. Build to seo-page's free-tool rules.
Ideas by site type:
- Agency or SaaS: schema checker, page speed grader, AI visibility checker, keyword gap finder.
- Directories: "[service] cost in [city]" calculator, "which [pro] do I need" quiz, document checklist, wait-time estimator, license lookup.
- Content or ecommerce: comparison tool, size or fit calculator, ROI or savings estimator.

Architecture: `/tools/<slug>` server page (metadata, schema, explainer, CTA) + client component + `/api/tools/<slug>`.
Non-negotiable security: block SSRF (private IPs, localhost, non-http), rate limit (about 10/IP/min on checks, 5/min on capture), validate email with zod, store leads durably (database or email notification, never the filesystem on Vercel), encode all input.
Track tool views, completed runs, optional captures and CTA clicks. Expect each tool to rank for 3-5 variants in 3-6 months (estimate, confirm in GSC).

## Phase 1.5: Platform listings
Fit gate per surface, shared API and docs spine, then Fern, Postman, npm CLI, Chrome extension, Notion, with live rel proof. Full runbook: `seo-authority/references/platform-listings.md`. Only Notion, Fern and Postman's Website field follow; CWS and npm are distribution, never backlinks. Accounts and submits are the owner's.

## Phase 2: Comparison and alternatives pages
"X vs Y" terms are lower competition and decision stage. Find them from autocomplete ("[topic] vs"), keyword exports filtered for vs, versus, alternative, competitor rankings, and Reddit. N options give up to N(N-1)/2 pairs: build only the pairs with real search demand.
Structure: H1 "[A] vs [B]: which is right for [audience]?", two-sentence verdict up top, comparison table, per-dimension breakdown, "best for" sections, real FAQ, recommendation, CTA. "Best [category]" pages follow seo-page's best-of type.

## Phase 3: Programmatic pages
Only through `~/tools/pseo-engine` and its gates (Phase 0 data gate, `pseo_slop_lint.py`, `seo_quality_gate.py`; see `~/tools/pseo-engine/AGENTS.md`).
- Find the real matrix (place x service x modifier) from data, then merge combinations that need the same answer.
- Every page carries its own facts (local rules, costs, data); the seo-page swap test applies. Store verified facts in a sheet or JSON and reuse them.
- Review a small draft batch by hand before scaling.
- Each page: 3+ internal links, real FAQs, schema that matches visible text, and a conversion path (find form, listing, tool result or CTA).
Content types that work: checklist, comparison, FAQ hub, local guide, glossary, alternatives, cost.

## Phase 4: Refresh cycle
Monthly, from GSC (last 30 days vs prior 30, and the same weeks last year):

| Group | Rule | Action |
|---|---|---|
| Rising | Clicks up over 10% | Amplify: 3-5 internal links in, deepen, refresh stats |
| Stable | Within 10% | Maintain |
| Declining | Down over 10%, not seasonal | Diagnose: better competitor, stale facts, CTR drop, cannibalization |
| Dead | Zero clicks 30+ days | Merge with 301, rewrite, or noindex (owner decides) |

Log counts and actions each month, plus the recovery rate of last month's fixes. Refresh and internal-link lanes: `references/tactic-ladder.md`. The 90-day wait applies per page.

## Phase 5: Semantic depth
Each page covers the subtopics the top results share and answers the real PAA questions, with links to deeper pages. Find terms from OpenSEO content gaps, PAA, related searches and topic clusters (`seo-keyword-map` section 3). Natural coverage, no stuffing.

## Phase 6: Review
Boris (security, edge cases, broken links), a design and UX critique, and a claims check (is every number sourced?). Fix P0s before calling it done. Then the seo-loop pre-ship checklist.

## Quality bar
- Every page: a clear path to revenue; worth sharing; data a CFO would accept; survives 1,000 users at once; has a way to stay current.
- Every claim: sourced; money math includes CTR (2-3%), conversion (3-5%) and close rate (20-30%), never raw volume x deal value; conservative defaults.
- Every authority play: no paid links that pass PageRank (paid = `rel="sponsored"`), relevant and indexed mentions only, varied anchors, nofollow listings never counted as backlinks.
- Score pages with `python ~/tools/pseo-engine/seo_quality_gate.py --url <url> --keyword "<term>" --compact`. Under 60 fails.

## Anti-patterns
- Product first, keyword later on a new domain.
- Thin programmatic pages with the place name swapped.
- Neutral comparisons that never help the reader choose.
- Publish and forget.
- Revenue math from raw search volume (overstates 100-800x).

