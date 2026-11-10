# Platform listings: owned surfaces on high-DR hosts

Five places where a product, not a pitch, earns a page on a big domain. Sources: five public X posts from 2026-10-27 (Notion credit to @aarondelasy). Link rel was checked on live pages 2026-10-27. Recheck with `scripts/check-listing-link.py` before you claim a link.

## Verified link value (2026-10-27)

| Surface | Page you get | Link to you | Checked on | Real value |
|---|---|---|---|---|
| Notion Marketplace | notion.com/connections/<name> | FOLLOW | /connections/zapier | Link + install path for users |
| Fern Agent Score | buildwithfern.com/agent-score/company/<docs> | FOLLOW | /company/resend | Link + AEO readiness grade |
| Postman profile | postman.com/<team> | FOLLOW on the Website field only | /stripedev | Link + forkable API docs |
| Chrome Web Store | chromewebstore.google.com/detail/... | NOFOLLOW (`ugc nofollow`) | Grammarly listing | Ranking page, AI citations, real installs |
| npm CLI | npmjs.com/package/<name> + mirrors | NOFOLLOW on npm and Libraries.io | `vercel` package | Distribution to developers, not link equity |

The posts call all five "dofollow" or imply it. Two are not. Never promise a client link equity from CWS or npm.

## Fit gate (run before building any of them)

Build a surface only if all three hold:
1. **It does one real job** a user of the product wants, outside the website. A shell page on a big host is the thin-page trick from SKILL.md section 3; it ranks fast and dies fast.
2. **The data it touches is safe to expose.** Public reference data (rules, limits, prices) is fine. Account data needs OAuth, scoped tokens and a privacy review first.
3. **Someone owns its upkeep.** A broken extension or stale CLI is a public 1-star page on Google's domain.

## Shared spine (build once, feeds four surfaces)

Most of these need the same three things. Build them first:
1. **A public read API** with stable JSON, CORS, a `limit` param, rate limits and an error shape.
2. **An accurate OpenAPI 3 file** at /openapi.json (Postman imports it, the CLI and docs derive from it).
3. **Docs on your own domain** (/developers or /docs) with an llms.txt that lists every docs page and a .md twin of each page.

The order that follows from this: spine, then Fern (free, instant), then Postman, then the CLI, then the extension, then Notion (heaviest).

## 1. Fern Agent Score (FOLLOW, live in minutes)
- Prereqs: the docs on your domain from the spine.
- Local check first: `npx afdocs <docs-url>` (npm `afdocs`, "Agent-Friendly Documentation Spec"). Fix what it flags before you submit, because the public grade is permanent until you rescore.
- Submit: buildwithfern.com/agent-score, then Score docs, then paste the docs URL. The page goes live at once. "Request listing" adds you to the leaderboard.
- Verify: `check-listing-link.py <fern page> <domain>` is client-rendered, so check rel in a browser.

## 2. Postman public profile (FOLLOW on the Website field)
- Owner step: create the Postman account and team (we never create accounts). Team URL = product name.
- Fill the profile: Website (the followed link), About, GitHub, X.
- Create a public workspace, import /openapi.json, and pin the collection on the profile.
- Links inside collection descriptions are nofollow. Only the profile Website field passes equity.
- Keep the collection generated from the OpenAPI file, never hand-edited, so it cannot drift.

## 3. npm CLI (NOFOLLOW, distribution only)
- Wrap the public API: one command per main action, `--json` output, an exit code that means something, and an optional login only if the API has auth.
- package.json: name, description, keywords (the terms buyers search on npm), homepage, repository, bin, engines, license, files.
- Mirrors pick it up automatically: npm.io, Libraries.io, jsDelivr, deps.dev. Libraries.io links are nofollow (checked). The others are unverified.
- Owner step: the npm account or org and `npm publish --access public` (we prepare `npm pack`; the owner publishes).
- Ship provenance (`--provenance` from CI) once a repo exists; it shows a verified badge.

## 4. Chrome Web Store extension (NOFOLLOW, ranks and gets cited)
- One clear job tied to the product. Smallest permissions possible: host permissions only for the sites it reads, no `<all_urls>`, no remote code (MV3 forbids it).
- Owner steps: the developer account ($5 one-time), upload, and submit for review.
- Policy traps: affiliate links only when the user clicks for a direct benefit, disclosed in the listing (CWS tightened this in 2025 after the Honey case; read the current policy before you add any affiliate behavior). Single-purpose policy: one feature set. A privacy policy URL is required if you touch any user data.
- Listing: 1280x800 screenshots, a 128px icon, a description that leads with the job, and the support site = your domain (it shows as a nofollow link, but users click it).

## 5. Notion Marketplace connection (FOLLOW, heaviest)
- A public connection means OAuth. Set the installation scope to "Any workspace"; it cannot be changed later.
- One simple data flow into a Notion database (rows of something the user already has in your product).
- Store tokens encrypted, revoke on disconnect, and push only fields the user picked. Privacy review before launch.
- Owner steps: create the connection in Notion developer settings, then Publish to Marketplace (name, description, category, logo, screenshots). Notion replies in 5-10 business days.

## Proof planes (do not merge them)
Built locally, passed review, submitted, live page exists, rel checked on the live page, referral traffic in GA4, installs or users. A submitted listing is not a live link. A live link is not traffic.

## Log
Per site, keep a `listings.md` row: surface, URL, submitted date, live date, rel result plus date, 30-day referral sessions, installs.
