---
name: seo-authority
description: Use for the weekly links lane and for getting cited in AI answers. Finds link targets from real competitor and mention data, writes the reason each site should link, drafts short pitches for approval, tracks a 7-day AI Overview loop on one query, runs roundup, reclamation, broken-link, original-stats and journalist-request plays, spots parasite-SEO threats, and runs platform listings (Notion Marketplace, Fern Agent Score, Postman profile, Chrome Web Store extension, npm CLI) with live link-rel proof. Also fires on "get listed on Notion", "Chrome extension for SEO", "publish a CLI for backlinks", "Postman profile", "agent score", "high-DR listings". Nothing sends without the owner's yes.
---
# SEO authority

One job: earn links and citations that a real editor or an AI answer would choose to give.

## 1. Links lane (every site, every week)
Keep a living target list (the site file says where). Move at least one target forward each week: found, reason written, pitch drafted, approved, sent, won.

Plays with steps (roundups, reclamation, link context, broken-link replacement, original stats, journalist requests, asset offers, free tools, vendor and review sites, platform answers): `references/link-plays.md`.

1. **Find targets from real data.** Competitor backlinks (free first: Search Console Links, Bing Webmaster, free checkers; a paid export only with the owner's yes), unlinked brand mentions, resource and roundup pages, partner pages, relevant directories, expert-quote and podcast requests. Never guess DR, traffic or linking pages.
2. **Filter.** Keep editorial, in-content, on-topic links from real sites. Drop spam, forum profiles, paid placements. For a big list: code drops sites with no real organic traffic on their own topic, then Jev scores relevance 0/1/2 (jev-seo-campaign prompt 13). Link metrics are easy to fake; a site that ranks on its own topic is the link worth having.
   **Size it.** Count referring domains to each top-3 PAGE, not domain. Aim to get inside that range, not above it. Free placements first. Under 50 referring domains, start free on-topic links now, next to the page work.
3. **Write the reason.** Read each page live. One line: the exact section, the gap or stale fact, and the specific URL of ours that fills it (fresher data, a free tool, a better comparison, local detail). No reason, no pitch. Aim for 10-20 strong rows, not hundreds.
4. **Draft the pitch.** Short, personal, one ask, names their article and the exact spot. Real contact from their site. No invented stats or relationships. No em dashes.
```
Linking page: [URL, title, exact section]. Our page: [URL]. Reason they'd cite it: [one line].
Draft a short, personal pitch with one ask, naming their article and the exact spot. No invented stats or relationships. No em dashes.
```
5. **Owner approves** each row (page, data, contact, reason, our URL, pitch). Sends go out only after that, as drafts the owner sends unless they gave a standing send permission for that batch. One follow-up max after about 7 days.
6. **Log** sent, replied, won. Recheck won links after 30 days.
Never: bought links, link swaps, PBNs, mass templates, exact-match anchor schemes. Only pitch a page that exists and earns the link.
Don't build: a toxic-backlink classifier or disavow cleanup. Google ignores bad links; the only exception is a manual action shown in Search Console.

## 2. AI-answer citations (AEO)
Rank well first; AI answers mostly pull from pages that already rank, review sites, directories and "best of" lists.
For one money query at a time:
1. **Day 0.** Save the AI Overview or chatbot answer: the named picks, slots ("best for X"), and every cited URL.
2. **Track 7 days.** Note which slots and citations stay stable and which drift.
3. **Reverse the citations.** What do the cited pages share? Tables, numbers, dates, named authors, a clear "best for" line?
4. **Build for a stable slot.** Use seo-page (often the "best [category]" type) with true, sourced "best for" claims the answer can lift word for word.
5. **Day 7 and day 28 recheck.** Log in the site's AEO folder.
Also: get listed on the "best of" lists and directories that the answers cite, through honest pitches, never paid awards. Find them with two Jev nouls per SERP result (third_party_list, lists_us; jev-seo-campaign prompt 15).
- Never rank yourself first in your own list. AI answers learned to discount self-rankings.
- Track 3-5 real buyer prompts a week in a private window, per engine (ChatGPT, Perplexity, Gemini, AI Overviews) and logged apart: brand named yes/no, our URL cited yes/no. Rerun the same prompts after each change. Prompts that name a competitor and not us are the first gaps to read. Skip paid "GEO visibility" scores. Bing Webmaster Tools' AI Performance report shows the real queries AI typed.

## 3. Owned authority beats borrowed rank
Real coverage, expert quotes, interviews, podcasts and partner mentions compound. Posting thin pages on high-trust open hosts (doc tools, script hosts, gists, shared notebooks) can rank fast and vanish fast. Never do it for an owned brand.

## 4. Platform listings (owned surfaces on high-DR hosts)
A real product surface on a big host: a Notion connection, a Fern docs grade, a Postman profile, a Chrome extension, an npm CLI. Full runbooks, fit gate and shared spine: `references/platform-listings.md`.
- Only two of the five give a followed link to the site (Notion, Fern), plus Postman's Website field. CWS and npm are nofollow (checked 2026-10-27). Sell them as distribution and AI citations, not link equity.
- Fit gate: it does one real job, touches only data that is safe to expose, and has an owner. Otherwise it is the section 3 thin-page trick.
- Build the spine once (public API, OpenAPI, docs with llms.txt and .md twins), then Fern, Postman, CLI, extension, Notion.
- Prove each live link: `python3 -I scripts/check-listing-link.py <listing-url> <our-domain>` (exit 0 follow, 1 nofollow, 2 not in server HTML, 3 fetch blocked; on 2 or 3 check in a browser).
- Accounts, fees, submits and publishes are the owner's. We build, pack and write the listing copy.

## 5. Complete answers on platforms that rank
When YouTube, LinkedIn, Reddit or Quora already ranks for a buyer query, a full, honest answer on our own named profile can reach those buyers. This is not section 3's thin-page trick: complete answer, disclosed affiliation, one tagged link to the next step. Steps in `references/link-plays.md` section 10. The owner posts.

## 6. Parasite-SEO watch (defense only)
When a rival or spammer outranks you from a trusted open host:
- Log the host, URL, query, date and evidence.
- Note whether AI answers cite it.
- Check again in 2-4 weeks; these pages often get wiped.
- Answer with a better owned page and earned links, not a copy of the trick.
