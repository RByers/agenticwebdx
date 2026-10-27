# What agents actually write for the web

Research behind the slide `what-agents-write`. Compiled 27 October 2026.
Raw npm data: [`web/data/npm-downloads.csv`](../web/data/npm-downloads.csv),
fetched by [`tools/npm_downloads.py`](../tools/npm_downloads.py).

## Question

When agents build for the web, what do they actually write, and what does
that mean for the web platform?

The hypothesis we tested has two parts:

1. Agents reach for the familiar stack: React + Tailwind + shadcn/ui + a
   handful of npm packages.
2. Agents under-use newer native web platform features (`<dialog>`,
   popover, `:has()`, container queries, CSS nesting, View Transitions,
   anchor positioning, Web Components, Temporal…).

This could lead in two directions:

- **Freeze.** New features aren't adopted, so there's no training data, so
  agents never use them.
- **The framework is the platform.** A few defaults (v0, Lovable,
  shadcn/ui, Tailwind) decide what millions of apps use. They can change
  overnight, so the framework, not the browser, becomes the target that
  matters.

## Key findings

1. **Part 1 is well supported.** Measured agent behaviour, vendor docs and
   registry-wide download data all point to the same stack.
   - In 2,430 open-ended Claude Code runs, shadcn/ui was 90.1% of
     UI-component picks and Tailwind 68.4% of styling picks.
   - v0 and Lovable ship one stack by design. Lovable says it “does not
     offer a choice of framework or database”.
2. **The stack is visible in npm downloads.** From Sep 2024 to Sep 2026,
   the packages that ship with shadcn/ui grew far faster than npm as a
   whole. `lodash` and `express` stand in for all of npm (3–4×).
   - `lucide-react` grew 61× and the `shadcn` CLI 53× (old and new names
     combined).
   - `class-variance-authority` 34×, `tailwind-merge` 23×, Radix Dialog 20×.
   - `tailwindcss` 12×, `react` 6.8×.
   - React's share of react + vue + svelte + angular downloads rose from
     71% to 86%.
   - `lit` (3.7×), `vue` (2.9×) and `@angular/core` (1.7×) grew no faster
     than the baseline, or slower.
3. **Part 2 (under-use of native features) is plausible but unmeasured.**
   - Nobody has published an audit of how often agent output uses
     `<dialog>`, popover, `:has()`, container queries and similar
     features.
   - The only number is Chrome's own eval of its Modern Web Guidance
     skill. It reports “a 37 percentage point improvement in adherence to
     modern best practices” when agents get the guidance. It publishes no
     baseline, no per-feature numbers and no write-up of the method.
   - The gap is itself a finding.
4. **Popularity bias is documented in general.** Twist et al. studied 8
   LLMs. They overuse widely adopted libraries “such as NumPy”, and in up
   to 45% of cases that use is unnecessary. They pick Python in 58% of
   high-performance project setups where it is not suitable, and never
   pick Rust.
5. **The freeze is not inevitable for tools.** Amplifying found “newer
   models tend to pick newer tools”. Their JS ORM pick moved from Prisma
   79% (Sonnet 4.5) to Drizzle 100% (Opus 4.6) within one model
   generation. Whether native platform features get the same lift is the
   open question.
6. **“The framework is the platform” has concrete examples.**
   - Lovable moved every new project from client-rendered React + Vite to
     SSR with TanStack Start on 13 May 2026, with no opt-in. Lovable says
     it builds 100,000 projects a day.
   - shadcn/ui switched its default primitives from Radix to Base UI in
     July 2026.
   - Each decision changed the stack of every new app at once.
7. **Homogenization is clearer at the stack level than at the visual
   level.**
   - Anthropic names the visual sameness “distributional convergence”:
     Inter fonts and purple gradients.
   - The Web Almanac 2025 found that “AI colors” (indigo-500, violet,
     purple) stayed at about 2% of Tailwind pages. Their overall rise
     tracks Tailwind's growth, not AI “choosing” purple.

## Data

### Amplifying: what Claude Code picks (Feb 2026)

Source: <https://amplifying.ai/research/claude-code-picks>.

**Setup:**

- Claude Code v2.1.39, pointed at 4 real repos, 3 runs each.
- 3 models (Sonnet 4.5, Opus 4.5, Opus 4.6) and 20 tool categories.
- Prompts never named a tool.
- 2,430 responses, of which 2,073 had a pick that could be parsed (85.3%).

**Top picks.** The page publishes only these 10 of the 20 categories, and
no runners-up.

| Category | Top pick | Share | n |
|---|---|---|---|
| Deployment (JS frontend) | Vercel | 100% | 86/86 |
| CI/CD | GitHub Actions | 93.8% | 152/162 |
| Payments | Stripe | 91.4% | 64/70 |
| **UI components** | **shadcn/ui** | **90.1%** | **64/71** |
| **Styling** | **Tailwind CSS** | **68.4%** | **52/76** |
| State management | Zustand | 64.8% | 57/88 (Redux: 0 primary picks, 23 mentions) |
| Observability | Sentry | 63.1% | 101/160 |
| Email | Resend | 62.7% | 64/102 |
| Testing | Vitest | 59.1% | 101/171 |
| Databases | PostgreSQL | 58.4% | 73/125 |

**Shifts between models** (Sonnet 4.5 → Opus 4.5 → Opus 4.6):

| Category | Sonnet 4.5 | Opus 4.5 | Opus 4.6 |
|---|---|---|---|
| ORM (JS) | Prisma 79% (Drizzle 21%) | Drizzle 60% | Drizzle 100% (0 Prisma) |
| Background jobs (JS) | BullMQ 50% | BullMQ 56% | Inngest 50% |
| Background jobs (Python) | Celery 100% | FastAPI BackgroundTasks 38% | FastAPI BackgroundTasks 44% |
| Caching (cross-language) | Redis 71% | Redis 31% | Custom/DIY 32% |
| Caching (Python) | Redis 93% | n/a | Redis 29% (Custom/DIY 0% → 50%) |
| Real-time (cross-language) | SSE 23% | Custom/DIY 19% | Custom/DIY 20% |

**Custom/DIY.** “Custom/DIY” (the agent builds it rather than installing a
tool) is the most common single label. It covers 12 of 20 categories and
252 picks in total. Shares where the page gives them:

- Feature flags 69%.
- Authentication: 48% overall, 100% in Python.
- Observability 22%.

The summary is “builds, not buys”. Note the real-time row: SSE is a
platform primitive. It is the one place in this data where a platform
feature competes directly with libraries.

The page does not break out the non-Tailwind styling picks (plain CSS? CSS
Modules?), the non-shadcn component picks, or a framework category.

### npm downloads: Sep 2024 → Sep 2026

These are monthly totals: the sum of daily downloads over the calendar
month. The “vs lodash” column divides the package's growth by lodash's
growth (3.2×), which roughly corrects for npm-wide inflation. Rows are
sorted by growth.

| Package | Sep 2023 | Sep 2024 | Sep 2025 | Sep 2026 | Growth Sep 24 → Sep 26 | vs lodash |
|---|---|---|---|---|---|---|
| `shadcn` (new CLI name only) | 0 | 0.42M | 1.60M | 40.43M | 95.9× | 30.0× |
| `motion` | 0.91M | 1.21M | 8.43M | 88.94M | 73.4× | 23.0× |
| `lucide-react` | 1.16M | 6.95M | 55.84M | 426.24M | 61.3× | 19.2× |
| `shadcn` + `shadcn-ui` (CLI, both names) | 95,202 | 0.78M | 2.27M | 41.10M | 52.9× | 16.5× |
| `class-variance-authority` | 1.63M | 7.75M | 34.06M | 266.21M | 34.3× | 10.7× |
| `tailwind-merge` | 3.36M | 14.76M | 51.57M | 345.36M | 23.4× | 7.3× |
| `@radix-ui/react-dialog` | 3.63M | 14.92M | 56.17M | 296.56M | 19.9× | 6.2× |
| `zustand` | 8.90M | 17.96M | 48.51M | 230.87M | 12.9× | 4.0× |
| `tailwindcss` | 26.97M | 43.99M | 100.22M | 528.51M | 12.0× | 3.8× |
| `vite` | 28.83M | 63.81M | 161.88M | 747.60M | 11.7× | 3.7× |
| `framer-motion` | 10.42M | 18.33M | 45.37M | 191.95M | 10.5× | 3.3× |
| `react-hook-form` | 15.60M | 24.72M | 63.55M | 234.30M | 9.5× | 3.0× |
| `@floating-ui/dom` | 30.10M | 50.95M | 108.85M | 408.73M | 8.0× | 2.5× |
| `preact` | 10.73M | 17.66M | 37.13M | 140.63M | 8.0× | 2.5× |
| `next` | 19.95M | 30.81M | 59.18M | 243.43M | 7.9× | 2.5× |
| `react` | 88.03M | 107.14M | 192.33M | 730.63M | 6.8× | 2.1× |
| `typescript` (baseline) | 182.86M | 251.17M | 401.30M | 1,174.34M | 4.7× | 1.5× |
| `svelte` | 3.00M | 5.65M | 9.76M | 24.26M | 4.3× | 1.3× |
| `express` (baseline) | 119.89M | 135.43M | 204.67M | 561.40M | 4.1× | 1.3× |
| `lit` | 4.78M | 8.18M | 14.78M | 30.00M | 3.7× | 1.1× |
| `lodash` (baseline) | 210.92M | 218.07M | 320.20M | 697.06M | 3.2× | 1.0× |
| `vue` | 16.54M | 22.67M | 33.01M | 66.16M | 2.9× | 0.9× |
| `shadcn-ui` (old CLI name) | 95,202 | 0.36M | 0.67M | 0.67M | 1.9× | 0.6× |
| `@angular/core` | 13.73M | 14.63M | 17.77M | 25.27M | 1.7× | 0.5× |
| `jquery` | 32.01M | 48.84M | 67.34M | 66.34M | 1.4× | 0.4× |

**React's share** of react + vue + svelte + @angular/core downloads:

| Sep 2023 | Sep 2024 | Sep 2025 | Sep 2026 |
|---|---|---|---|
| 72.6% | 71.4% | 76.1% | 86.3% |

Flat until 2025, then a jump during the coding-agent boom.

**Notes:**

- **shadcn rename.** The CLI was renamed from `shadcn-ui` to `shadcn`.
  The `shadcn` package was created on 9 Jul 2024, so the new name's
  Sep 2024 base is artificially small. Use the combined 53×, not 96×. An
  earlier draft of the slide used 96× and was corrected.
- **Shared step.** Every package, including the baselines, steps up
  between Jan and Mar 2026:

  | Package | Jan 2026 | Feb 2026 | Mar 2026 |
  |---|---|---|---|
  | lodash | 353M | 430M | 565M |
  | react | 275M | 333M | 464M |
  | express | 248M | 285M | 396M |

- **JS stand-ins for native features.** Radix Dialog does what
  `<dialog>`/popover now do (20×). Floating UI does what anchor
  positioning now does (8×). Downloads say nothing about whether native
  features were also used.

### App-builder defaults

| Tool | Default stack | Exact words | URL |
|---|---|---|---|
| v0 (Vercel) | Next.js, React, TypeScript, Tailwind, shadcn/ui | “v0 uses Next.js, React, TypeScript, Tailwind CSS, and shadcn/ui.” Also claims “best-in-class expertise in Next.js, React, Tailwind CSS, shadcn/ui, and the AI SDK” and that it “supports popular frontend frameworks and UI libraries” (none named). AI SDK v6 by default. | <https://v0.app/docs/faqs> |
| Lovable | TanStack Start (SSR) since 13 May 2026 (22 Jun 2026 for Enterprise); before that React + Vite + React Router, client-rendered. PostgreSQL via its built-in backend or Supabase. | “Lovable does not offer a choice of framework or database.” | <https://docs.lovable.dev/introduction/faq>, <https://lovable.dev/blog/building-apps-using-tanstack-start> (1 Jun 2026) |
| Lovable (scale) | n/a | “100,000. New projects are built on Lovable every single day” | <https://lovable.dev/blog/one-year-of-lovable> (18 Nov 2025; vendor claim) |
| Claude artifacts (Anthropic skill) | React 18 + TypeScript + Vite + Parcel + Tailwind CSS + shadcn/ui; 40+ shadcn/ui components pre-installed; Tailwind 3.4.1 | “**Stack**: React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui” | <https://github.com/anthropics/skills/blob/main/skills/web-artifacts-builder/SKILL.md> |
| Bolt | React + Vite + Tailwind (reported) | Third-party sources only; Bolt's docs not checked | (unverified, see below) |

Lovable's FAQ does not name a styling or component library. The
shadcn/ui + Tailwind claim for Lovable comes from third-party guides. The
TanStack Start post doesn't mention them either.

### Twist et al.: popularity bias in LLM library choices

Source: <https://arxiv.org/abs/2503.17181>.

Lukas Twist, Mark Harman, Don Syme, Joost Noppen, Helen Yannakoudakis,
Detlef Nauck, Jie M. Zhang, “A Study of LLMs' Preferences for Libraries
and Programming Languages”, arXiv 2503.17181. v1 (21 Mar 2025) was titled
“LLMs Love Python”; v4 is dated 4 Jun 2026.

| Finding (8 LLMs) | Number |
|---|---|
| Unnecessary use of widely adopted libraries (“such as NumPy”), deviating from ground truth | up to 45% of cases (v1 said 48%) |
| Python chosen for high-performance project setups where it is not optimal | 58% |
| Rust chosen in those tasks | 0 |
| Python for language-agnostic benchmark tasks (v1) | 90–97% |
| LLMs contradict their own language recommendation in project setup (v1) | 83% |

The authors warn of “discoverability challenges for newer open-source
projects”. Limitation: the study is about Python and data science, not web
front ends.

### Chrome Modern Web Guidance: the 37-point claim

Primary source: <https://developer.chrome.com/docs/modern-web-guidance/get-started>
(page last updated 30 Jun 2026; covered by web-standards.dev on 20 May 2026).

- “On average, early results show a 37 percentage point improvement in
  adherence to modern best practices.” The page also says “your results
  may vary”.
- **Method** (as described): Playwright-based QA. Each guide has a
  Playwright script, validated against a correct reference demo (expected
  100% pass) and a flawed one (expected 0%). End-to-end evals compare an
  unguided control against the guided run.
- **Not published:** the baseline score, the guided score, results per
  feature or per model, and a write-up of the method.
- **Rationale, in Chrome's words:** “AI coding agents tend to default to
  older, outdated solutions to modern web development problems” and “AI
  models historically haven't been aware of—or have incorrect information
  about—the latest web platform features.”
- **Coverage.** The docs say “over 100 web development use cases”. The
  [repo](https://github.com/GoogleChrome/modern-web-guidance) lists 232
  modern web features (CSS & layout 128, HTML & DOM 36, JS & APIs 68)
  across 186 use cases. The repo says evals are used to “prune
  lowest-common-denominator content that models already know”.

## Evidence

Each source with what it says and its limits.

1. **Amplifying, “What Claude Code Actually Chooses”**, Edwin Ong & Alex
   Vikati, Feb 2026. <https://amplifying.ai/research/claude-code-picks>.
   Numbers are in the Data section.
   - Limitations: one agent (Claude Code) with three Anthropic models;
     four repos that aren't described individually (a Next.js SaaS and a
     Python API are mentioned).
   - Small n per category (71 UI picks, 76 styling picks).
   - Only top-10 categories published, and no raw data.
   - It measures library and vendor choices, not native features.
2. **v0 FAQ.** <https://v0.app/docs/faqs>. Quoted above. Limitation:
   vendor docs describe defaults, not usage shares.
3. **Lovable FAQ and blog.**
   - <https://docs.lovable.dev/introduction/faq>: “does not offer a
     choice of framework or database”.
   - <https://lovable.dev/blog/building-apps-using-tanstack-start>
     (1 Jun 2026). Before: Vite + React Router, static hosting (Cloudflare
     Pages), client-side rendering only, Edge Functions. After: TanStack
     Start, Cloudflare Workers, SSR/SSG/CSR per route, TanStack Server
     Functions.
   - Why TanStack Start: React ecosystem, open and independent, deploys
     anywhere, SSR for search engines, an established maintainer, and
     type safety that gives “the AI clearer guardrails”.
   - TanStack calls Lovable a partner and says it worked on Lovable's
     code-generation guidance (<https://tanstack.com/blog/lovable-partnership>,
     1 Jul 2026; seen via search, not fetched).
   - <https://lovable.dev/blog/one-year-of-lovable> (18 Nov 2025): 100,000
     new projects per day and 5 million daily visits to Lovable-built
     sites. Vendor claims.
4. **Anthropic web-artifacts-builder skill.**
   <https://github.com/anthropics/skills/blob/main/skills/web-artifacts-builder/SKILL.md>.
   - Stack as quoted above.
   - It also says: “To avoid what is often referred to as ‘AI slop’, avoid
     using excessive centered layouts, purple gradients, uniform rounded
     corners, and Inter font.”
   - Limitation: this is a skill for building complex artifacts, not the
     whole artifact runtime. A third-party claim that the artifact runtime
     itself ships shadcn/Tailwind/lucide/recharts comes from Simon
     Willison's Oct 2024 post via search (not fetched).
5. **npm download counts.** Our own pull, method below.
   - Limitations: downloads are not apps or users. CI, mirrors, bots and
     throwaway agent projects all count, and the whole registry grew 3–4×
     over this period.
6. **Twist et al.** arXiv 2503.17181. Above.
7. **GitHub, “How AI is reshaping developer choice (and Octoverse data
   proves it)”**, Andrea Griffiths, 19 Feb 2026.
   <https://github.blog/news-insights/octoverse/how-ai-is-reshaping-developer-choice-and-octoverse-data-proves-it/>
   - TypeScript became the most-used language on GitHub in Aug 2025,
     overtaking Python and JavaScript.
   - TypeScript +66% YoY, JavaScript +24%; shell scripting in
     AI-generated projects +206%.
   - “AI is rewiring developer preferences through convenience loops.”
     “Reduced friction becomes a preference—and preferences at scale can
     shift ecosystems.”
   - “There are concrete, technical reasons AI performs better with
     strongly typed languages.”
   - The post doesn't discuss training data or newer languages losing
     out. InfoQ's coverage
     (<https://infoq.com/news/2026/03/ai-reshapes-language-choice/>, seen
     via search) makes the reverse-loop argument.
8. **Chrome Modern Web Guidance.** Above.
9. **Anthropic, “Improving frontend design through Skills”**, 12 Nov 2025.
   <https://claude.com/blog/improving-frontend-design-through-skills>
   - Names “distributional convergence”: without guidance, a landing page
     will “conform to Inter fonts, purple gradients on white backgrounds,
     and minimal animations”, because “models predict tokens based on
     statistical patterns in training data.”
   - It ties this to the “AI slop” aesthetic. It also notes Claude still
     converges on common choices (e.g. Space Grotesk) across generations.
10. **HTTP Archive Web Almanac 2025, “Generative AI” chapter.** Christian
    Liebel, Yash Vekaria, Jonathan Pagel; reviewed by Thomas Steiner and
    others. Published 15 Jan 2026.
    <https://almanac.httparchive.org/en/2025/generative-ai>
    - **AI colors** (CSS custom properties only, so a conservative
      estimate):
      - Across all pages, purple went from 0.02% (Q3 2022) to 0.49%
        (Q4 2025), and indigo-500 from 0.03% to 0.54%.
      - Within Tailwind pages, indigo-500, violet `#8b5cf6` and purple
        `#a855f7` stayed at about 2% with no surge.
      - Their reading: “this trend may be less a result of AI ‘choosing’
        purple and more a reflection of the general rise in Tailwind's
        popularity.” And: “We also tested for surges in gradients,
        shadows, and specific fonts, but found no statistically
        significant increases.”
    - **Vibe-coding hosts** (subdomains in the crawl):
      - `*.vercel.app` approaches 0.04% of all sites by Oct 2025.
      - “The data showed no immediate surge following the launch of v0.”
      - Lovable subdomains went from 10 (early 2025) to 315 (Oct 2025).
      - Replit is visible from early 2025.
    - **`llms.txt`:** 2.13% of desktop and 2.1% of mobile pages (July
      2025).
    - **New APIs** (not linked to AI-built sites): WebGPU 0.243% / 0.238%
      of pages (desktop/mobile, Jul 2025); Prompt API 0.095% / 0.078%;
      Translator API 0.277% / 0.262%.
    - Limitations: the crawl mostly sees home pages of established sites,
      so most AI-built apps are invisible. It does not measure React,
      shadcn, or native UI features on AI-built sites.
11. **MDN MCP server**, 15 Jun 2026.
    <https://developer.mozilla.org/en-US/blog/introducing-mdn-mcp-server>
    (already cited in the deck's `docs` slide). It exists because AI tools
    “can surface outdated web platform information”.
12. **Lighthouse Baseline Features audit**, July 2026.
    <https://web.dev/blog/baseline-lighthouse-features-audit>. It reports
    the Baseline status of detected features, powered by `web-features`.
    Seen via search, not fetched in full.
13. **Endor Labs, State of Dependency Management 2025**, 4 Nov 2025.
    <https://endorlabs.com/lp/state-of-dependency-management-2025>.
    - Only about 1 in 5 dependency versions recommended by AI coding
      assistants were free of both hallucinations and known
      vulnerabilities.
    - 44–49% of dependencies imported by coding agents had known
      vulnerabilities.
    - Press-release figures seen via search. This is about security, not
      platform features.
14. **Spracklen et al., “We Have a Package for You! A Comprehensive
    Analysis of Package Hallucinations by Code Generating LLMs”**, USENIX
    Security 2025, arXiv 2406.10279.
    - About 19.7% of recommended packages didn't exist (576K samples, 16
      LLMs, per secondary reports).
    - Open-source models 21.7% vs. commercial 5.2%.
    - Not fetched from the primary source; adjacent (slopsquatting), not
      used on the slide.
15. **Di Sipio et al., “Addressing Popularity Bias in Third-Party Library
    Recommendations Using LLMs”**, arXiv 2501.10313 (Jan 2025).
    - LLM-based recommenders did not remove popularity bias. Fine-tuning
      and popularity penalties improved diversity.
    - From the abstract via search, not read in full.
16. **saschb2b, “Six Models, One React Stack: Why Every LLM Builds the
    Same App”**, 4 May 2026.
    <https://saschb2b.com/blog/llm-default-react-stack>
    - An informal table: Claude, DeepSeek, Qwen, v0 and Lovable default
      to Tailwind + shadcn/ui; GPT, Gemini and Grok to Tailwind with mixed
      components; the framework split is Next.js vs. Vite.
    - No method, run count or fixed prompts. Anecdotal; it doesn't
      mention native features.
17. **shadcn/ui changelog**, “July 2026 – Base UI as the Default”.
    <https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default>
    - New projects use Base UI instead of Radix. Radix is still supported,
      with `init -b radix` to opt back in.
    - React Aria was added as a third base the same month.

## Native-feature usage

**What is measured:**

- How often native features appear on the web as a whole. Chrome Platform
  Status use counters (<https://chromestatus.com/metrics>) give the share
  of page loads using `HTMLDialogElement`, popover, `:has()`, container
  queries and so on. The HTTP Archive / Web Almanac measure the share of
  crawled pages.
- The Web Almanac 2025 has no CSS or Markup chapter
  (`/en/2025/css` → 404; `/en/2024/css` → 404; `/en/2022/css` exists).
  The 2025 Generative AI chapter measures new JS APIs (WebGPU, Prompt API,
  Translator) but not on AI-built sites.
- Developer self-reports. The State of CSS 2025
  (<https://2025.stateofcss.com/en-US/usage/>) reportedly puts `:has()` as
  the most-used and most-loved new feature and container size queries at
  41% “used” (via an aggregator; not verified on the official site).
- Chrome's eval: +37 points with guidance. This is the only agent-specific
  number.
- Indirect: JS stand-ins for native features are growing fast on npm
  (Radix Dialog 20×, Floating UI 8× vs. lodash 3.2×).

**What is not measured:**

- No public audit of agent output (Claude Code, Codex, Copilot, Cursor,
  v0, Lovable, Bolt) for which native features it uses.
- No crawl that separates AI-built sites from other sites, by
  `*.lovable.app` / `*.vercel.app` / `*.v0.dev` hosts or by build
  fingerprints, and compares their feature use with the web baseline.
- No published baseline score for the Chrome eval.

**Tooling that exists to push agents toward modern features:**

- **Chrome Modern Web Guidance** (May 2026). An agent skill plus CLI with
  232 features and 186 use cases. Install with
  `npx skills add GoogleChrome/modern-web-guidance`. Backed by the Edge
  team as well, per coverage.
- **MDN MCP server** (Jun 2026). Current docs and browser-compat data for
  agents.
- **Community Baseline MCP servers**, e.g. `yamanoku/baseline-mcp-server`,
  built on the Web Platform Dashboard / webstatus.dev API. Reported as
  small (about 36 stars, last updated Mar 2026, per a directory listing).
- **Lighthouse Baseline Features audit** (Jul 2026). Powered by
  `web-features`.
- **Anthropic frontend-design skill.** Its target is visual sameness, not
  platform features.

Each of these exists because vendors believe agents default to old
patterns. That belief is itself evidence, though weak evidence.

## Homogenization

- **Stack level (strong evidence).**
  - Claude Code picks shadcn/ui 90% of the time. v0 and Lovable each ship
    one stack, and Anthropic's own artifact skill specifies the same one.
  - On npm, the shadcn companion packages grow 20–60× against a 3× npm
    baseline.
  - React's share among the big four frameworks jumped from 71% to 86% of
    downloads.
- **Visual level (mixed evidence).**
  - Anthropic says outright that models converge on “Inter fonts, purple
    gradients on white backgrounds”, and its artifact skill tells Claude
    to avoid them.
  - The Web Almanac found no AI-driven surge in purple, gradients, shadows
    or specific fonts. Within Tailwind pages, AI colors held at about 2%,
    and the overall rise follows Tailwind's growth. But the crawl sees few
    AI-built apps.
- **One decision moves everything.**
  - Lovable → TanStack Start (13 May 2026) changed the rendering model of
    every new Lovable app (about 100K a day, by Lovable's Nov 2025 count)
    without user opt-in.
  - shadcn/ui → Base UI default (Jul 2026) changed the accessibility and
    behaviour primitives under every new shadcn project.
  - TanStack now co-writes Lovable's AI guidance.
  - These are the levers that actually move what agents emit, and they
    move faster than standards.

## Unverified claims

Left off the slide, and why:

- **Lovable totals.** “50M projects”, “60M projects”, “~1M new projects
  per week”, “$500M ARR”, “720M monthly visits”: LinkedIn posts and news
  roundups only. The 100K-a-day figure *is* verified to Lovable's own blog
  (Nov 2025), but it's a vendor claim and older.
- **Adam Wathan's `bg-indigo-500` apology** (X, about 7 Aug 2025): widely
  reported, with reach given as 684K to over 1M views, but the original
  post wasn't reached. The Web Almanac data argues against reading too
  much into it.
- **Bolt's default stack** (React + Vite + Tailwind, maybe shadcn
  pre-integrated, Tailwind v3): third-party sources only.
- **Claude artifact runtime library list** (shadcn, Tailwind, lucide,
  recharts): Simon Willison, Oct 2024, via search. Not re-verified against
  current Anthropic docs.
- **State of CSS 2025 numbers** (`:has()` most used, 41% container
  queries): via an aggregator.
- **Endor Labs, Spracklen et al., Di Sipio et al.:** summaries via
  search, not read from the primary documents.
- **Frontend-design skill install counts** (277K vs. 1.1M): the sources
  conflict.
- **“38% of new web applications in 2025 were built with AI tools
  (Gartner)”:** appears on a comparison site and was not traced to
  Gartner.

## Methodology

**npm downloads:**

- Script: `tools/npm_downloads.py`, run as
  `python3 tools/npm_downloads.py > web/data/npm-downloads.csv` on
  27 Oct 2026.
- Endpoint: `https://api.npmjs.org/downloads/range/<start>:<end>/<package>`.
  It returns daily counts and allows at most 18 months per request.
- Three chunks per package: `2023-09-01:2024-08-31`,
  `2024-09-01:2025-08-31` and `2025-09-01:2026-09-30`. Daily counts are
  summed per calendar month.
- CSV columns: `package,month,downloads`. 24 packages × 37 months
  (2023-09 to 2026-09).
- Cross-checked against the point endpoint
  `https://api.npmjs.org/downloads/point/2024-09-01:2024-09-30/<package>`
  for several packages; the totals match exactly.
- Package choice: the shadcn/ui stack and its companions, JS stand-ins
  for newer native features, the main frameworks, other common React-stack
  picks, and baselines nobody picks for UI (`lodash`, `express`,
  `typescript`).
- The “vs lodash” column is the package's growth divided by lodash's.
- React's share = react / (react + vue + svelte + @angular/core).

**Other sources:** pages were fetched with a web fetcher on 27 Oct 2026
and quoted from the fetched text. Anything known only from search
snippets is marked “via search”.

## Caveats

- npm downloads ≠ apps ≠ users.
  - Agents and app builders generate huge numbers of throwaway installs,
    and CI dominates many counts.
  - React is pulled in by many non-React tools.
  - The whole registry about tripled, so only growth relative to a
    baseline means much, and even that is rough.
- The Amplifying data covers one vendor's agent, and the repos may favour
  certain stacks (one is a Next.js SaaS). Other agents (Codex, Gemini,
  Copilot) may differ. Anecdotally they also converge on Tailwind.
- Vendor defaults (v0, Lovable) say what is generated by default, not
  what share of output it is. Users can sometimes ask for other stacks
  (v0).
- The 37-point claim comes from a vendor with an interest in the outcome,
  has no published baseline, and measures “adherence to modern best
  practices” as Chrome defines it.
- Libraries and native features aren't either/or. A shadcn/Tailwind app
  can still use `:has()`, container queries (Tailwind v4 has container
  query utilities), or `<dialog>` underneath. Base UI and Radix may adopt
  native popover or anchor positioning. Download data can't tell.
- Model recency shifts picks quickly (Prisma → Drizzle within one model
  generation), so any snapshot ages fast.

## Open threads

1. **Audit agent output for native features.** Give several agents
   (Claude Code, Codex, Gemini CLI, Copilot, Cursor; v0, Lovable, Bolt) a
   fixed set of UI tasks: modal, menu/popover, tooltip, responsive card,
   tabs, accordion, page transition, date handling. Parse the output for
   `<dialog>`, `popover`, `:has()`, `@container`, nesting, View
   Transitions, `anchor-name`, `<details name>`, custom elements and
   Temporal. Run with and without Modern Web Guidance or the MDN MCP. That
   produces the missing baseline.
2. **Crawl AI-built sites.** Sample `*.lovable.app`, `*.vercel.app`,
   `*.v0.dev`, `*.replit.app` and `*.bolt.new` hosts (or HTTP Archive rows
   matching them). Compare their feature use with all pages, using the
   HTTP Archive custom metrics or Chrome use counters.
3. **Ask Amplifying for the raw data.** We want all 20 categories, the
   runners-up, what the non-Tailwind styling picks were, whether any
   “Custom/DIY” UI picks used native elements, and the 4 repos.
4. **Ask Chrome for the eval details**: baseline vs. guided scores per
   feature and per model, and the features where agents already do well.
   Their “prune what models already know” step implies they have a list
   of features that are already learned.
5. **Ask app builders** (Vercel, Lovable, StackBlitz, Replit) whether they
   would publish stack and feature telemetry. Ask TanStack, shadcn and
   Base UI whether their primitives now use native popover, `<dialog>` or
   anchor positioning. If they do, the framework becomes the route by
   which native features reach agents.
6. **Time series.** Re-run `tools/npm_downloads.py` quarterly, and track
   Chrome use counters for popover, anchor positioning and View
   Transitions against the agent-era jump.
7. **Check the Web Almanac 2026** for a CSS or Markup chapter, and for any
   AI-site segmentation.

## Slide

Slide id `what-agents-write`. Draft at the time of writing; the deck may
differ.

- **h2:** “Agents build on the default stack, not the platform”.
- **Left column, “What agents reach for”:**
  - **90%** of Claude Code's UI-library picks are shadcn/ui; 68% of its
    styling picks are Tailwind (Amplifying).
  - **1** stack: Lovable “does not offer a choice of framework”; v0 builds
    on Next.js + Tailwind + shadcn/ui.
  - **?** How often agents use `<dialog>`, popover, `:has()`: unmeasured.
    Chrome reports +37 points of “modern best practice” with its guidance.
- **Right column, “npm downloads, Sep 2026 vs. Sep 2024”** (linear bars,
  61× = 80% width):

  | Package | Growth |
  |---|---|
  | `lucide-react` | 61× |
  | `shadcn` CLI (both names) | 53× |
  | `tailwindcss` | 12× |
  | `react` | 6.8× |
  | `lodash`, as the all-of-npm baseline | 3.2× |

- **Closing question** (`p.next`): “Is the framework now the platform
  agents target? If so, what are we standardizing for?”
- **Source line:** Amplifying (Feb 2026); Lovable docs; v0 FAQ; Chrome
  Modern Web Guidance (May 2026); npm registry download API.
