# SEO case study: baselines, receipts and the write-up

One job: make every ship provable, so a "how we grew X" post is a copy job, not a memory test.

Rules: real numbers only, each with a file or URL behind it. No invented or rounded-up numbers. Client sites stay anonymous unless the client says yes in writing. Grade 8-9, short sentences, no em dashes.

## 1. Baseline before the first change
Save one dated folder per site, for example `<site logs>/baseline-YYYY-MM-DD/`. Put in it:
- **Search Console export:** 28 days and 90 days, query x page (clicks, impressions, CTR, position). Note the window, the property (domain or URL prefix) and the method (UI, API, or a loader that drops anonymized queries). Numbers from two methods are never compared.
- **Index count:** indexed URLs out of sitemap URLs, with the source (URL Inspection API or the Pages report) and its "last updated" date.
- **Conversions:** the named conversion (signup, lead, call, booking, subscriber) by landing page, from the tool that counts it. Write down whether tracking was verified and any consent or gap that undercounts.
- **Local only:** map grid rank, reviews total and new per month, NAP audit sheet.
- **Links:** referring domains to the money pages, with the tool and date.
- **Live state:** titles, H1s and status codes of the pages you plan to touch.
If a number can't be pulled, write "no baseline" and why. A missing before number is a gap, not a guess.

## 2. Receipts at every ship
Keep these next to the ship log entry:
1. The change: PR or doc link, merge commit, deploy id, time with zone.
2. The before snapshot: the section 1 numbers for the pages touched, taken the day of the ship.
3. The live check: URL returns 200, in sitemap, canonical, title and H1 as shipped.
4. The ask: indexing request and its result.
5. Day 7 and day 28: the same numbers, same method, same pages.
6. Anything else that changed in the window (other ships, outages, tracking fixes, season). It stops a post from crediting the wrong change.

## 3. Reading the result
- Compare like with like: same method, same window length, same pages.
- Say what changed and what didn't. Flat or down is still a result.
- One change and one result is a link, not proof. Write "after" or "since," not "because," unless only one thing changed.
- A conversion claim needs verified tracking for the whole window.

## 4. Article template: "How we grew [metric] for [site type]"
Use only the receipts above. Anonymize: "a national HSA review site," "a local events newsletter."
```
Title: How we [took X from A to B] in [N weeks] for [site type]
Hook (2-3 lines): the problem in plain words and the one number that moved.
Where it started: the baseline table, dated, with sources.
What we found: 2-4 causes, each with its evidence.
What we changed: one short section per change, in date order, with the ship date.
What happened: the before and after table, same method. Day 7 and day 28 if you have them.
What didn't work: honest misses and what we learned.
What we'd do next: the next change and why.
How to copy it: 3-5 steps the reader can run on their own site.
Receipts note: "Numbers from [tool], [method], [window]. No numbers rounded up."
```
Gate before anyone posts: every number traced to a file, no client name or detail without written consent, no promises ("results vary"), human-copy pass, owner's yes.
