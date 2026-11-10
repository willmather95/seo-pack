---
name: seo-keyword-map
description: Use when building or cleaning up a keyword list and page plan for a site. Builds the list from real searches in five buckets, sorts by intent, maps one intent to one page, and flags pages that compete with each other. Never invents search volumes.
---
# Keyword map

One job: turn real searches into a page plan where every page owns one intent.

## 1. Build the raw list (real data only)
Start from what the business actually sells or covers. Read the site file (see seo-loop) for offers, places and conversion.
Cover five buckets:
1. **Service + place:** "[service] [city]", "[service] near me". The money searches. They go first.
2. **Brand or product names:** each brand, provider or product people search by name. "[Brand A] [city]" is a different search from "[Brand B] [city]".
3. **Problem:** what is wrong before they know the fix ("dark spots on face", "lost HSA receipts").
4. **Price:** "[service] cost", "how much is [service]". Close to buying.
5. **Comparison:** "[A] vs [B]", "best [category]". Still deciding.

Add the city and 3 to 5 nearby areas only if the business serves them. Then collect:
- Buyer words from sales calls, demos, support tickets and the inbox. Use their phrasing, not ours.
- Search Console queries filtered in code for buying modifiers (best, vs, alternative, price, cost, pricing, review, for [role or use]). This is demand we already reach.
- Search Console queries for the site (28 or 90 days).
- Google autocomplete and "People also ask" for each seed.
- A keyword tool export (volume, difficulty). Default: OpenSEO `get_keyword_metrics` for known terms and `research_keywords` for new seeds, inside the cap (`seo-research-openseo`). Record the tool and date.

Never let a model guess volumes. If you have no volume data, say so and rank by Search Console impressions or by business value.

## 2. Sort by intent
For a full Search Console export (hundreds or thousands of rows), don't paste it into a writing model: it reads the first few hundred rows and guesses the rest. Judge every row with a Jev "buyer" noul and a category choice (jev-seo-campaign, prompts 4-5), after the 50-row hand-label check. The prompt below is for short lists.
Prompt pattern (paste the real export):
```
Here is a keyword export for [business] serving [market], with volume and difficulty from [source, date].
Sort every term into:
A) Ready to act now (buy, book, sign up, subscribe)
B) Researching (comparing, pricing, learning before acting)
C) DIY or no buying intent
Keep the original numbers. Sort each group by volume. Don't add, rename or estimate any terms or numbers. Flag terms that fit more than one group.
```
Routing: A goes to money pages (service, location, product). B goes to guides, comparisons, price pages and free tools. C goes to the bottom of the backlog or nowhere.

## 3. Map to pages
- **Check the live SERP first.** The top results show the format buyers expect (list, tool, product page, guide, video). Match it or pick another term.
- **Group by shared results.** Terms whose top 10 share most URLs need one answer: put them on one page. Grouping is done in code on SERP exports, not by the model's guess.
- **Narrow to win.** When the head term is out of reach, target one buyer and one use case ("[category] for [role]").
- **Plan clusters from a money page.** Pick the commercial page first, then the buyer questions around it: one broad guide, detail pages for questions that need a full answer, all linked both ways. Expand to the same buyer's next problem only after the cluster ranks.
- **One intent per page.** Don't mix "buy" and "how to" in one title.
- **One service, one page. One brand, one page.** A single page listing 20 services gives search engines little to rank.
- Location pages only for places the business really serves, and only if each can carry its own local facts (see seo-page swap test).
- **Service x town grid.** For a local business, plan one page per service and one page per service and town it really serves. Link it like a tree: home links to the main service pages, each service page links to its town pages, and each town page links back to its service page and to nearby towns. Build the grid a few pages at a time, best towns first.
- Tool-intent terms ("calculator", "checker", "estimator", "how much") are free-tool candidates.
Prompt pattern:
```
Using groups A and B, propose a page map. For each page: URL, one primary term, 3-5 supporting terms from the list only, page type (money, location, guide, comparison, tool), and the bucket it serves.
Mark any term that would compete with these existing URLs: [list].
```

## 4. Check for conflicts
- Two pages showing for the same query is usually fine (that's topical depth). It is a real conflict only when the two pages have the same intent AND the same angle: same reader, same question, same answer. Test every pair with two Jev nouls and flag only when both are 0.9+ (jev-seo-campaign, cannibalization). Expect a handful of pairs, not hundreds. The owner decides any merge, redirect or re-aim; a redirect is hard to undo.
- Pages whose queries are all group C with tiny impressions are merge or noindex candidates. The owner decides.

## 5. Output
A table: URL | primary term | supporting terms | bucket | intent | page type | data source | status (exists, rewrite, new). Save it with a date next to the site log. New pages still need the owner's yes before they are built.
