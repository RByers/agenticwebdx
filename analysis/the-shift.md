# How far has web development shifted from human-led to agent-led?

Research record for the "shift" section of the deck: the part divider
(`#shift`) and the four data slides `#stackoverflow`, `#docs`, `#adoption`
and `#commits`. Compiled 27 October 2026. URLs were fetched or searched on
that date unless noted.

## Question

The session's premise (see [README](../README.md)) is that "a growing share
of web code is written by agents". Before the room debates how standards
should adapt, the deck needs to show how true that premise is, using public
data that can be checked:

- Are developers still using the human-centred channels the web platform
  relies on: Q&A sites, documentation, MDN?
- How many developers use AI tools and coding agents, and how often?
- How much public code do agents actually write, and is that share still
  growing?
- Is web development (JS/TS, HTML/CSS) more affected than other areas?

In line with the README's tone guidance, the aim is to show the size of the
change *and* how uncertain it is. The data supports "a large, fast shift". It
does not clearly support "agents have taken over".

## Key findings

1. **Human Q&A has collapsed.** New Stack Overflow questions fell from
   196,527 a month (April 2016) to 1,175 (July 2026), down 99%. Web tags
   fell further: `[javascript]` went from 23,799 to 69 a month (−99.7%) and
   `[css]` from 8,426 to 31 (−99.6%). The decline began slowly around 2017.
   It became a collapse after ChatGPT (Nov 2022) and went close to zero once
   coding agents arrived (2025).
2. **Docs readership is shifting to agents, at least on one platform.** On
   Mintlify-hosted docs, agents' share of traffic rose from 20.8% (Feb 2026)
   to 66% (Aug 2026): 257M agent requests vs. 131M human page loads. Tailwind's
   docs traffic is down about 40% from early 2023 even though Tailwind is
   more popular than ever. Mozilla shipped an official MDN MCP server in June
   2026. No public MDN traffic numbers were found.
3. **AI tool use is now the norm.** In the Stack Overflow surveys, developers
   currently using AI tools rose from 44% (2023) to 62% (2024) and 78.5%
   (2025). In 2026, 66% of AI users use coding agents, 73% of coding-agent
   users use them daily, and 70% of respondents ask an AI when looking for
   answers.
4. **Web code is where coding AI is used most.** In Anthropic's April 2025
   sample of 500K coding conversations, 31% were JavaScript/TypeScript and
   28% HTML/CSS. UI component work was the top task. 79% of Claude Code
   sessions were "automation", where the agent does the task, against 49% on
   Claude.ai.
5. **Agent-written public code rose steeply, then may have levelled off.**
   AI-attributed commits went from ~2% of public GitHub push events
   (Dec 2025) to 15.1% (Apr 2026). They then stayed around 16–18% from May to
   July. Month-on-month growth fell from +89% (March) to +14% (July), and
   S-curve fits now beat an exponential one. This is a lower bound, and one
   instrument. It is the main reason the deck frames the shift as "well
   under way" rather than complete.

## Data

### Stack Overflow: new questions per month

From the public Stack Exchange API (`/2.3/questions?site=stackoverflow&filter=total`),
sampled January, April, July and October each year (`[css]` January and July
only). Full series:
[`web/data/stackoverflow-questions.csv`](../web/data/stackoverflow-questions.csv).
Script: [`tools/so_fetch.py`](../tools/so_fetch.py). Chart:
[`tools/so_chart.py`](../tools/so_chart.py).

| July of | All questions | `[javascript]` | `[css]` |
|---|---:|---:|---:|
| 2009 | 32,463 | 1,750 | 769 |
| 2010 | 60,834 | 3,876 | 1,412 |
| 2011 | 100,419 | 8,069 | 2,960 |
| 2012 | 141,810 | 12,225 | 4,641 |
| 2013 | 176,390 | 16,666 | 6,518 |
| 2014 | 176,581 | 19,869 | 7,515 |
| 2015 | 195,128 | 23,799 | 8,032 |
| 2016 | 176,578 | 22,055 | 6,964 |
| 2017 | 179,742 | 21,478 | 6,744 |
| 2018 | 159,987 | 17,744 | 5,022 |
| 2019 | 150,965 | 16,052 | 4,301 |
| 2020 | 165,978 | 19,770 | 5,046 |
| 2021 | 123,920 | 14,636 | 4,135 |
| 2022 | 110,579 | 12,575 | 3,219 |
| 2023 | 62,557 | 5,839 | 1,910 |
| 2024 | 31,435 | 2,163 | 762 |
| 2025 | 6,621 | 367 | 203 |
| 2026 | 1,175 | 69 | 31 |

Peaks among sampled months: all questions 196,527 (April 2016);
`[javascript]` 23,799 (July 2015); `[css]` 8,426 (January 2014).

### Docs traffic

| Measure | Value | Source |
|---|---|---|
| Agent share of traffic, Mintlify-hosted docs, Feb 2026 | 20.8% | Mintlify, 2026 State of Knowledge Report |
| Agent share of traffic, Mintlify-hosted docs, Aug 2026 | 66% (257M agent requests vs. 131M human page loads) | same |
| `/llms.txt` fetches, Aug 2026 | ~10.8M | same |
| MCP tool calls, Aug 2026 | >2M (~3× since Feb) | same |
| Agents vs. browsers, 30 days to early Apr 2026 (user-agent only) | 45.3% vs. 45.8% of ~790M requests | Mintlify blog, 3 Apr 2026 |
| Claude Code / Cursor share of all requests, same snapshot | 25.2% / 18.0% | same |
| Tailwind docs traffic vs. early 2023 | ≈ −40% | Adam Wathan, 7 Jan 2026 |
| Tailwind revenue | "down close to 80%"; 75% of engineering team laid off | same |

### Developer surveys

| Measure | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|
| Currently using AI tools in development (Stack Overflow) | 44% | 62% (61.8%) | 78.5% (47.1% daily + 17.7% weekly + 13.7% monthly or less) | not published comparably |
| Using or planning to use AI tools | 70% | 76% | 84% | — |
| Using AI agents | — | — | 31% (23% at least weekly) | 66% of AI users use coding agents |
| Daily use among coding assistant/agent users | — | — | — | 73% |
| First stop for answers: search / AI | — | — | — | 83% / 70% |
| Stack Overflow as a source of work answers | — | — | — | 24% |
| Share of own code that is AI-generated (State of JS) | — | 20% | 29% (median 25%) | — |

Agent of choice in 2026: Claude Code (66%), GitHub Copilot (59%).

### Anthropic Economic Index: coding conversations (sampled 6–13 Apr 2025)

| Measure | Value |
|---|---|
| JavaScript/TypeScript share of queries | 31% |
| HTML/CSS share of queries | 28% |
| "UI/UX Component Development" share of tasks | 12% (top task) |
| "Web & Mobile App Development" share of tasks | 8% |
| Automation (vs. augmentation), Claude Code | 79% |
| Automation, Claude.ai | 49% |

### AI-attributed commits on public GitHub (botcommits.dev)

Six tracked tools (Claude Code, Jules, OpenAI Codex, Gemini Code Assist,
Devin, Aider) against GH Archive push events. Copilot coding agent is
reported separately by the site and is not in this total. Derived from
<https://botcommits.dev/data.json> (data updated 18 Aug 2026; the partial
August month is excluded). Full series:
[`web/data/ai-commit-share.csv`](../web/data/ai-commit-share.csv). Chart:
[`tools/botcommits_chart.py`](../tools/botcommits_chart.py).

| Month | AI-attributed commits | of which Claude Code | Push events | Share of pushes |
|---|---:|---:|---:|---:|
| 2025-06 | 294,710 | 224,256 | 66.8M | 0.44% |
| 2025-09 | 570,922 | 486,418 | 71.5M | 0.80% |
| 2025-12 | 1,693,958 | 1,549,783 | 75.6M | 2.24% |
| 2026-01 | 3,604,315 | 3,396,432 | 74.7M | 4.83% |
| 2026-02 | 5,672,580 | 5,439,099 | 66.0M | 8.60% |
| 2026-03 | 10,608,342 | 10,291,623 | 84.0M | 12.63% |
| 2026-04 | 12,066,054 | 11,756,992 | 80.0M | 15.09% |
| 2026-05 | 14,193,313 | 13,854,357 | 88.7M | 16.00% |
| 2026-06 | 17,721,774 | 17,436,783 | 95.4M | 18.58% |
| 2026-07 | 20,083,498 | 19,804,129 | 112.8M | 17.81% |

Model fits reported by the site (Claude Code, linear space, Feb 2025 → Jul 2026):

| Model | Result |
|---|---|
| Exponential | doubling every ~2.6 months (it was 1.2 months when fitted through Mar 2026) |
| Logistic | ceiling ~22.5M commits/month, inflection ≈ Apr 2026 |
| Gompertz (best by AIC) | ceiling ~29.6M commits/month, inflection ≈ Apr 2026 |
| March exponential forecast for July | ~98M commits, vs. ~20M actual |
| Sigmoid beats exponential | in 5 of 6 fit configurations; ceilings range 11M–106M across them |

## Methodology

- **Stack Overflow.** One API call per series per sampled month, with
  `fromdate`/`todate` set to the month's UTC bounds and `filter=total`, so
  only a count is returned. Unauthenticated calls hit rate limits (HTTP 429),
  so the script retries with back-off. The source link on the slide is the
  live query for July 2026. Change the dates or add `&tagged=` to reproduce
  any other point. Re-checked against the live API on 27 Oct 2026.
- **Docs, surveys, Anthropic.** Figures were taken from the primary
  publication and quoted where possible. The 2025 "currently using" figure
  (78.5%) is the sum of the survey's daily, weekly and monthly-or-less
  answers. It is our calculation, not a headline Stack Overflow published.
- **botcommits.dev.** Its method: GH Archive via BigQuery for Jan–Sep 2025,
  where each push payload listed its commits and attribution trailers could
  be matched with a regex. From Oct 2025 it uses the GitHub commit Search
  API, because GH Archive dropped the commit list from push payloads. The
  search queries are split into windows, run three times each, and the
  median is used. The two methods agree within about ±20% where they
  overlap. We divided the six-tool total by monthly push events, as the
  site's own share chart does.

## Caveats

- **Stack Overflow measures substitution, not total demand.** Part of the
  decline started before AI (2017–2022). Deleted questions are excluded,
  which lowers counts for all years. The API counts only questions, not
  traffic to existing answers, and people may still read old answers via
  search or via agents.
- **Mintlify is one platform, not "docs" in general.** Its customers skew
  towards developer tools that agents use heavily. The report says human
  traffic (client-side analytics) and agent traffic (server-side requests)
  are measured differently, so the comparison is an estimate. One fetch by
  an agent is not the same as one page read by a human.
- **Tailwind is one anecdote**, from a founder explaining layoffs. It is
  consistent with the trend but not a measurement of the web as a whole.
- **Survey samples are self-selected** and skew towards engaged developers.
  The 2026 agent figures are shares of AI users, not of all respondents, so
  the 2023–2025 bars can't simply be extended.
- **The Anthropic data covers one vendor's users** in one week of April
  2025, before most agent adoption. Claude's users may skew towards web
  work.
- **botcommits.dev is a lower bound of a specific signal.** It counts
  attribution markers, not AI use. Claude Code adds its trailer by default;
  Cursor and Copilot inline completions add nothing. Squash merges collapse
  many agent commits into one. GitHub reports 81.5% of contributions happen
  in private repos. The commits-per-push ratio is unknown (≈1:1 from
  Octoverse totals, ≈3:1 implied by other estimates), so 17.8% of push
  events reads as about 6–18% of commits. The plateau since April could
  reflect real saturation, a change in attribution habits (e.g. people
  turning the trailer off), or measurement noise in the Search API, which
  the site puts at ±10–15% per month.
- **Different sources tell different-strength stories.** The docs and survey
  data suggest agents are already the majority consumer in some places. The
  commit data suggests agent-written public code is a fast-growing minority
  whose growth is slowing. The deck now presents both.

## Claims considered and not used

| Claim | Why not used |
|---|---|
| Claude Code wrote ~4% of public GitHub commits (SemiAnalysis, 5 Feb 2026), heading for 20%+ by end of 2026 | Paywalled, with no stated method; 20% is an extrapolation. Dropped in favour of botcommits.dev, which publishes method, queries and data. |
| Claude Code commits ~0.7% (Sep 2025) → 4.5% (Mar 2026) (conffab.com) | Second-hand summary; the underlying analysis could not be located. |
| MDN traffic decline | No public MDN numbers found (Mozilla publishes none; search results were for unrelated domains). |
| Wikipedia human pageviews −8% in 2025; Chartbeat publisher pageviews −6% | Real, but about general readers, not developers. |
| GitHub Octoverse 2025: 43.2M merged PRs/month (+23%), "1M+ PRs by Copilot coding agent" | The PR total doesn't separate agents. The Copilot agent figure appeared only in a secondary blog. |
| "42% of code is AI-assisted" (Sonar); State of WebDev AI 2025 | Different definitions from the State of JS question; not needed alongside it. |
| Mintlify "66% in July" / "78% in October" figures seen in search snippets | Not found in the primary report, which gives Feb 20.8% and Aug 66%. |

## Open threads

- **MDN traffic.** Ask Mozilla/OWD for MDN page-view trends since 2022 and
  MDN MCP server usage since June 2026. This would be the most direct
  web-platform signal.
- **Web share of agent commits.** botcommits.dev doesn't break commits down
  by language. A query restricted to JS/TS/HTML/CSS repos would show whether
  web code leads the shift, as the Anthropic data suggests.
- **Is the commit plateau real?** Re-pull botcommits.dev data after August
  2026. Check whether Claude Code's attribution defaults or user settings
  changed around April 2026, and look for a second instrument (e.g. bot
  authors, PR labels, or agent-specific config files in repos).
- **More Stack Overflow tags.** `[html]`, `[reactjs]`, `[typescript]` and
  `[next.js]` would show whether newer frameworks fell as fast as the
  older tags.
- **Who reads specs?** Server logs for w3.org/TR, WHATWG specs or caniuse
  split by user agent would show whether agents read standards directly or
  only via docs.
- **Survey comparability.** The 2026 Stack Overflow full results
  (<https://survey.stackoverflow.co/2026/>) may contain an all-respondent
  "currently using" figure that would extend the 2023–2025 series.

## Sources

- Stack Exchange API, questions endpoint:
  <https://api.stackexchange.com/docs/questions>
- Mintlify, *The 2026 State of Knowledge Report*:
  <https://www.mintlify.com/state-of-knowledge/2026>
- Mintlify, *The state of agent traffic in documentation* (3 Apr 2026):
  <https://www.mintlify.com/blog/state-of-ai>
- Adam Wathan, comment on tailwindlabs/tailwindcss.com#2388 (7 Jan 2026):
  <https://github.com/tailwindlabs/tailwindcss.com/pull/2388#issuecomment-3717222957>
- MDN, *Introducing the MDN MCP server* (15 Jun 2026):
  <https://developer.mozilla.org/en-US/blog/introducing-mdn-mcp-server/>
- Stack Overflow Developer Survey 2024, AI: <https://survey.stackoverflow.co/2024/ai>
- Stack Overflow Developer Survey 2025, AI: <https://survey.stackoverflow.co/2025/ai>
- Stack Overflow, *The results of the 2026 Developer Survey are here* (6 Oct 2026):
  <https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/>
- Anthropic, *Anthropic Economic Index: AI's impact on software development* (28 Apr 2025):
  <https://www.anthropic.com/research/impact-software-development>
- State of JavaScript 2025, usage: <https://2025.stateofjs.com/en-US/usage/>
- botcommits.dev, *AI-attributed commits on public GitHub*: <https://botcommits.dev/>;
  data <https://botcommits.dev/data.json>; code and raw queries
  <https://github.com/edgardomunoznajar/github_explosion>
- SemiAnalysis, *Claude Code is the inflection point* (5 Feb 2026, not used):
  <https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point>

## Slide

Part divider `shift` ("The shift is well under way") and slides
`stackoverflow`, `docs`, `adoption` and `commits` in `web/index.html`, each
followed by speaker notes with the full sources.

| Slide | On slide | Value | From |
|---|---|---|---|
| `stackoverflow` | Chart + "−99% all questions since the 2016 peak" | 196,527 → 1,175 / month | Stack Exchange API |
| `stackoverflow` | `[javascript]`, `[css]` | 23,799 → 69; 8,426 → 31 | Stack Exchange API |
| `docs` | Agent share of docs traffic | 20.8% → 66% | Mintlify |
| `docs` | Tailwind quote | docs traffic −40% | Wathan |
| `docs` | MDN MCP server | June 2026 | MDN blog |
| `adoption` | Developers using AI tools | 44% → 62% → 78% | Stack Overflow surveys |
| `adoption` | Daily coding-agent use; ask AI for answers | 73%; 70% | Stack Overflow 2026 |
| `adoption` | JS/TS or HTML/CSS share of coding conversations | 59% | Anthropic |
| `commits` | Chart: AI-attributed share of push events | 2.2% → 15.1% → 17.8% | botcommits.dev |
| `commits` | Share of public commits | ~6–18% | botcommits.dev |
| `commits` | Monthly growth | +89% → +14% | botcommits.dev |
| `commits` | Takeaway | "…Agents are now a major consumer too; whether they become the typical one is still open." | — |

In the speaker notes but not on the slides: the 2017–2022 pre-AI decline,
the Mintlify April snapshot (Claude Code alone 25% of requests), Tailwind's
revenue and layoffs, the 2025 agent-use figure (31%), Claude Code and
Copilot as agents of choice, Claude Code's 79% automation rate, State of
JS (20% → 29% AI-generated), and the botcommits.dev model fits and caveats.
