# Where agent and human DX conflict

*Research for the TPAC 2026 breakout “Agents are redefining DX. [How] should
web standards adapt?” Compiled 27 October 2026. The slide that uses it is
`#conflicts` in [`web/index.html`](../web/index.html), right after the
`#topic-conflicts` section slide.*

## Question

> Where agent ergonomics and human DX conflict, how do we weigh them?

Sub-questions:

- Is there measurable evidence of these conflicts in practice, rather than in theory?
- When they conflict, which side is winning today?
- What is the human's role once agents write most of the code, and what does that imply for API design?

The qualitative list of conflicts in API design (silent recovery vs. loud
failure, token efficiency vs. robustness, familiar vs. better, usage-signal
pollution, primitives vs. declarative features, magic vs. explicitness) is in
[`design-principles.md`](design-principles.md#human-vs-agent-dx-conflicts).
This file looks for data on how the conflicts play out.

## Key findings

The short version: **the human's role is shifting from writing code to
reading and reviewing it. Where preferences differ, the agent side mostly
wins, and the cost lands on human reviewers.**

1. **Types: ceremony for humans, guardrails for agents. Types are winning.**
   TypeScript became the most used language on GitHub in August 2025
   (2,636,006 monthly contributors, +66.6% year over year), passing Python by
   about 42k. GitHub attributes the shift to typed languages “that make
   agent-assisted coding more reliable in production”. In the State of JS
   survey, respondents writing *only* TypeScript went 28% (2022) → 34% (2024)
   → 40% (2025); JavaScript-only fell to 6%. Supports the robustness finding
   that 94% of LLM compile errors are type errors
   ([`robustness.md`](robustness.md)).
2. **Docs: what helps agents can starve the human-facing ecosystem.** On
   7 Jan 2026, declining a PR that added an `llms.txt` endpoint to the
   Tailwind docs, Adam Wathan wrote that docs traffic is “down about 40% from
   early 2023 despite Tailwind being more popular than ever”, revenue is
   “down close to 80%”, and “75% of the people on our engineering team lost
   their jobs here yesterday”. Making docs easier for LLMs “just means less
   traffic to our docs”. Agents now dominate Mintlify docs traffic (66%,
   [`the-shift.md`](the-shift.md)). This is an incentive conflict, not an
   ergonomic one, but it affects who funds human-facing docs and tooling.
3. **Review is the new bottleneck.** Faros AI telemetry (10,000+ developers,
   1,255 teams) compares each team's highest- and lowest-AI-adoption quarters:
   tasks completed +21%, PRs merged +98%, but average PR size +154%, PR
   review time +91%, and bugs per developer +9%. No significant improvement
   showed at company level.
4. **Agent-written code is harder for humans to read.** CodeRabbit analyzed
   470 open-source PRs (320 AI-co-authored, 150 human-only): 10.83 vs. 6.45
   issues per PR (1.7×). Readability issues were more than 3× as common;
   formatting 2.66×, naming inconsistencies ~2×, logic and correctness 1.75×.
   GitClear's 2025 report (211M changed lines, 2020–2024) found an 8×
   increase in duplicated 5+ line blocks during 2024; 2024 was the first
   year copy-pasted lines outnumbered moved (refactored) lines.
5. **Humans misjudge the trade-off.** METR's randomized trial (16
   experienced open-source developers, 246 tasks, Feb–Jun 2025): with AI
   allowed, tasks took 19% longer. Developers predicted a 24% speed-up
   beforehand and still believed they'd been 20% faster afterwards.

**Implication for the room:** if humans mostly read, review and debug code
that agents wrote, the human DX that matters is *reading* DX. Several of the
things agents need (explicit types, loud errors, declarative features,
dictionaries over positional arguments) also help a reviewer. The real
conflict may be with *writing* DX for humans (terseness, forgiveness,
shorthand), which matters less each year.

## Data

### Faros AI: high vs. low AI-adoption quarters (slide bar chart)

| Metric | Change |
|---|---|
| Tasks completed | +21% |
| PRs merged | +98% |
| Average PR size | +154% |
| PR review time | +91% |
| Bugs per developer | +9% |

Bars on the slide are scaled so +154% = 80% of the column width.

### TypeScript adoption

| Measure | Value | Source |
|---|---|---|
| GitHub monthly contributors, Aug 2025 | 2,636,006 (+66.6% YoY) | Octoverse 2025 |
| Python, same period | ~2.6M (+48.8% YoY) | Octoverse 2025 |
| State of JS: write only TypeScript | 28% (2022), 34% (2024), 40% (2025) | State of JS 2025, via InfoQ / I-Programmer |
| State of JS: write only JavaScript | 8% (2024) → 6% (2025) | same |

### CodeRabbit: AI-co-authored vs. human-only PRs

| Category | AI ÷ human |
|---|---|
| All issues | 1.7× (10.83 vs. 6.45 per PR) |
| Readability | >3× |
| Formatting | 2.66× |
| Security | up to 2.74× |
| Logic and correctness | ~1.75× |
| Error handling | ~2× |
| Naming inconsistencies | ~2× |
| Excessive I/O | ~8× |

## Sources

- GitHub, *Octoverse: A new developer joins GitHub every second as AI leads TypeScript to #1*, 28 Oct 2025. https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
- Devographics, *State of JavaScript 2025* (survey Nov 2025, published early 2026). https://2025.stateofjs.com/ — figures via InfoQ, https://www.infoq.com/news/2026/03/state-of-js-survey-2025, and I-Programmer, https://www.i-programmer.info/news/167-javascript/18655-state-of-javascript-2025.html
- Adam Wathan, comment on *feat: add llms.txt endpoint for LLM-optimized documentation*, tailwindlabs/tailwindcss.com#2388, 7 Jan 2026. https://github.com/tailwindlabs/tailwindcss.com/pull/2388 — coverage: eWeek, https://www.eweek.com/news/tailwind-labs-lays-off-engineers-due-to-ai/
- Faros AI, *The AI Productivity Paradox Report 2025*, 23 Jul 2025. https://www.faros.ai/blog/ai-software-engineering
- CodeRabbit (D. Loker), *State of AI vs Human Code Generation*, 17 Dec 2025. https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report
- GitClear, *AI Copilot Code Quality 2025*. https://www.gitclear.com/ai_assistant_code_quality_2025_research — figures via DevClass, https://devclass.com/2025/02/20/ai-is-eroding-code-quality-states-new-in-depth-report/
- METR, *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*, Jul 2025. https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ — summary: Simon Willison, https://simonwillison.net/2025/Jul/12/ai-open-source-productivity/

## Methodology

Web search for quantitative evidence of agent/human DX tension, then reading
the primary source where it was reachable (Octoverse, Faros, CodeRabbit,
the Tailwind PR). State of JS, GitClear and METR figures are from secondary
coverage that agreed across outlets; they were not checked against the
primary reports.

## Caveats

- **Vendor data.** Faros sells engineering analytics; CodeRabbit sells AI code
  review. Both have an interest in “AI creates review work”.
- **Correlational.** Faros compares quarters within teams; it can't separate
  AI from other changes in the same period, and can't tell whether longer
  reviews mean more thorough or just more code.
- **Authorship is inferred.** CodeRabbit labels PRs AI-co-authored from
  visible signals; “human-only” PRs may include unlabeled AI code.
- **Dated tools.** METR and Faros measured early/mid-2025 tools. Agents (and
  AI reviewers) have improved since; the review bottleneck may have moved.
- **Correlation with types isn't causation.** TypeScript was growing before
  agents; framework defaults also push it. GitHub's attribution to AI is its
  own interpretation.
- **One company's story.** Tailwind is a vivid case of the docs incentive
  conflict, not evidence of a general trend in docs funding.
- **Not web-platform specific.** None of these measure web APIs directly.
  They describe how code is now produced and consumed, which shapes what
  “human DX” for a web API means.

## Open threads

- Is there data on how *reviewers* interact with web-platform code
  specifically (e.g., whether declarative HTML/CSS features are reviewed
  faster than equivalent JS)?
- API usability studies with humans reading (not writing) code: do the
  designs that help agents also help reviewers?
- State of CSS / State of HTML: has sentiment toward verbose-but-explicit
  patterns (utility classes, typed APIs) changed since agents arrived?
- Do AI code reviewers relieve the bottleneck? Data after mid-2025 on review
  time with AI review bots.
- MDN traffic and funding: does the Tailwind pattern repeat for
  platform docs?
