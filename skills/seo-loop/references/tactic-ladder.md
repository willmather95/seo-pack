# Tactic ladder: where effort goes first

Source note: borja (@borjafat), 232-tactic ladder, 2026-10-27 (one founder's ranked list; the order transfers, the claims are unverified). Use this when picking the week's change. Higher rungs beat lower rungs unless a defect is open.

## The order
1. **Buyer-intent pages.** Pricing, comparisons, alternatives, migration guides, feature and integration pages, trial and discount terms. Built from real buyer words (`seo-keyword-map` section 1, `seo-page` section 3).
2. **Topical depth from a commercial page.** Pick the money page first, then plan the guide and detail pages that feed it (`seo-keyword-map` section 3).
3. **Information gain.** Something the top 10 results do not have: our data, a test, a firsthand example (`seo-page` section 1b).
4. **Refresh what already ranks.** Usually the cheapest win (lane below).
5. **Internal links people click.** (lane below)
6. **Earned links and citations.** Roundups, reclamation, replacement, original stats, journalist requests (`seo-authority`, `references/link-plays.md`).
7. **Distribution on platforms that rank.** YouTube answers, LinkedIn articles, honest Reddit and Quora answers (`seo-authority` section 5).
8. **Local profile work** for real locations (`seo-local`).
9. **Polish last.** Meta descriptions, share previews, schema, image and script weight, llms.txt. Fix these when broken; don't make them the week's change while rungs 1-5 have open work.

## Refresh lane (rung 4)
Run in code on the 28-day and year-over-year GSC exports:
- **Lost clicks:** compare the same weeks last year before calling a drop. A dip that repeats every year is seasonal, not a defect.
- **Near page one:** queries at position 4-15 with real impressions on a money page are the first refresh pool.
- **Unanswered queries:** a query with impressions that the page never answers gets a short section, not a new page. In bulk, judge each query and page pair with a Jev yes/no "answered on page" choice, using the jev-seo-campaign run pattern (50-row hand check first).
- **Stale facts:** old prices, plan limits, screenshots, years in titles. Refresh with an "as of" date.
- **Duplicates:** two pages giving the same answer to the same reader merge into one URL with a 301. The owner approves every redirect.
- **Titles:** if the position held but CTR fell, rewrite the title to say why to click (`seo-page` section 6).
The 90-day wait still applies after a real change.

## Internal-link lane (rung 5)
- Every article links to the product or money page it supports, placed beside the question that page answers.
- Find orphans (pages with zero internal links in) from the crawl. Each gets 3-5 links in from related pages, or a merge or noindex call by the owner.
- Push near-page-one pages: link to them from the site's strongest pages (most clicks or referring domains).
- Anchor text names what opens next, in the words of the sentence. Vary it. No exact-match anchor schemes.
- Keep the main guides and money pages in the nav or footer.
- If the analytics setup allows, track internal-link clicks; rewrite or drop links nobody clicks after 90 days.

## Tracking that ties it to money
- Conversions and revenue by landing page (seo-loop Weekly step 1).
- UTM-tag every link we place off-site (platform posts, listings, guest pieces) so we can see which places send buyers.
- Save the before numbers and the edit at every ship (seo-loop step 8).
