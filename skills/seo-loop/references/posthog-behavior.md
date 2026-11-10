# PostHog behavior lane

Why: Search Console tells us how people find a page. PostHog tells us what they do once they land. The growth plan is to read that behavior every week and change the site from it before anyone complains, rather than guessing.

## Setup (once per site)
1. One PostHog project per site. Write its name, region (US or EU) and the conversion event name in the site file.
2. Install the snippet or SDK with pageviews, autocapture and session replay on. Mask form inputs in replay. Respect the site's consent banner: PostHog waits for consent where GA4 does.
3. Send the conversion (lead, signup, booking, purchase) as one named event, the same name every time, with the landing page as a property.
4. Prove it: trigger a real test conversion and see the event in PostHog Activity. A snippet in the code is not proof.
5. Save three insights in the project so the weekly pull is one call each: "Search visitors by landing page", "Search landing page to conversion funnel", "Rage and dead clicks by page".

Agents read PostHog through the PostHog MCP (installed in Claude Code 2026-11-03 with `npx -y @posthog/wizard@latest mcp add`). Never print the API key.

## Weekly pull (28 days, search visitors only)
Filter: `$referring_domain` is a search engine (google, bing, duckduckgo) or an AI answer (chatgpt.com, perplexity.ai, gemini, copilot).

| Read | What it tells us |
|---|---|
| Visits and conversion rate by landing page | Which ranking pages make money and which leak |
| Funnel: landing page to CTA click to conversion | Where in the page people give up |
| Scroll depth on the top 10 landing pages | Whether the answer or CTA sits below where people stop |
| Rage clicks and dead clicks by page | Things people think are links or buttons, broken parts |
| Exit pages and next pages | Where they go when the page did not answer them |
| 3-5 replays on the week's chosen page | The why behind the numbers |

## Turning it into a change
- Ranks well, converts badly: fix the page (move the answer up, move the CTA up, cut what people skip). This can beat a new keyword.
- Rage clicks on a non-link: make it a link or stop it looking like one.
- Most people stop before the CTA: add a CTA where they stop.
- Visitors from AI answers behave differently from Google visitors: write for the question the AI sent them with.
- Bounce right away from a query that ranks: the page does not match the intent. Check the SERP again.

Each finding names its source (insight URL or replay ID) like any other receipt. Behavior changes still go through the owner gate and the 90-day wait.
