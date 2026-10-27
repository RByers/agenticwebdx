# Should we design for agents at all? Volatility vs. permanence

Research record for the `volatility` slide. Compiled 27 October 2026. All
URLs were fetched or searched on that date unless noted.

## Question

From the session description (README.md):

> Should we take agent consumers into account at all? The counterarguments
> are that agents are not uniform — what is efficient for one model
> generation may not be for the next — and the landscape is still volatile,
> whereas Web APIs are permanent.

This file collects data on both sides so the room can argue from facts:
how fast models change, how long web APIs live, and which properties of
agents have held steady across model generations.

## Key findings

**For the skeptic (the agents change fast):**

- **Price for a fixed capability falls ≥10× a year.** a16z puts it at about
  10×/year; Epoch AI measures 9× to 900×/year depending on the benchmark
  threshold (40×/year for GPT‑4-level PhD science questions).
- **Context windows grew about 30× a year** from mid‑2023 to mid‑2025
  (8K for GPT‑4 in 2023; 1M for Gemini 2.5 Pro and 10M for Llama 4 Scout
  in 2025).
- **Consecutive models from one vendor disagree on defaults.** Prisma was
  79% of Claude Sonnet 4.5's JS ORM picks in Claude Code and 0% of Claude
  Opus 4.6's, four months later. Celery went 100% → 0% and Redis 93% → 29%
  for Python.
- **Models last about a year or two.** Retired Claude models were
  available on Anthropic's first-party API for roughly 12–25 months; Claude
  Opus 4.1 lasted exactly one year (5 Aug 2025 → 5 Aug 2026).

**Against the skeptic (some things hold):**

- **Web APIs last decades.** Mutation events were in a W3C Recommendation
  in Nov 2000, deprecated in 2011 and removed from Chrome in Jul 2024:
  24 years in all, 13 of them deprecated. `document.all`, `<marquee>` and
  synchronous XHR are still required by today's specs.
- **The browser almost never takes things back.** chromestatus.com lists
  1,894 entries "Enabled by default" vs. 198 "Removed" (hand-maintained
  status field; see caveats).
- **Frontier tokens did not get cheap.** GPT‑4 launched at $30/$60 per
  million input/output tokens (Mar 2023); Anthropic's top tier today
  (Claude Fable 5.1, Sep 2026) is $10/$50. Input fell 3×, output barely
  moved. Meanwhile average prompt tokens per request grew about 4×
  (OpenRouter, late 2025). The "tokens are getting 10× cheaper, so
  efficiency doesn't matter" argument only holds for last year's
  capability level.
- **Every generation still hallucinates.** 2026 frontier models invent
  4.62%–6.10% of package names, vs. 5.2% (commercial) to 21.7%
  (open-source) for the 2024 cohort. The range shrank; the floor did not
  go to zero.
- **Every generation has a training cutoff, and docs in context fix it.**
  On Next.js 16 APIs that postdate training data, Vercel's agent eval
  went from 53% with no docs to 100% with an 8KB docs index in
  AGENTS.md.
- **Familiarity bias is structural.** Models overuse popular libraries
  (NumPy used unnecessarily in up to 48% of cases across 8 LLMs) and
  emit deprecated APIs learned from training data (all 7 LLMs tested).

**Implication for the discussion:** the volatile part is token-level
efficiency for a particular model. The stable part is the cost of
unfamiliarity, of silent failure, and of missing or unreadable docs. A
design principle aimed at the stable part survives model turnover; one
tuned to this year's model probably doesn't.

## Data

### Price per million tokens, frontier-tier models, 2021–2026

| Model | Launch | Input $/M | Output $/M | Source |
|---|---|---:|---:|---|
| GPT‑3 (davinci) | Nov 2021 (public availability) | 60 | 60 | a16z LLMflation |
| GPT‑4 (8K context) | 14 Mar 2023 | 30 | 60 | TechCrunch, 14 Mar 2023 |
| GPT‑4 (32K context) | 14 Mar 2023 | 60 | 120 | OpenAI pricing as quoted on Manifold (secondary) |
| OpenAI o1 | Sep 2024 | — | 60 | a16z LLMflation ("same output price as GPT‑3 at launch") |
| Claude Opus 4 / 4.1 | May / Aug 2025 | 15 | 75 | Anthropic pricing page (retired models still listed) |
| Claude Opus 4.5 | Nov 2025 | 5 | 25 | Anthropic pricing page |
| Claude Opus 4.6 / 4.7 / 4.8 / 5 | Feb–Jul 2026 | 5 | 25 | Anthropic pricing page |
| Claude Fable 5 / Mythos 5 | Jun 2026 | 10 | 50 | Anthropic pricing page |
| **Claude Fable 5.1** / Mythos 5.1 | ~1 Sep 2026 | **10** | **50** | Anthropic pricing page |
| Claude Opus 5.5 | Sep 2026 | 4 | 20 | Anthropic pricing page |
| Claude Sonnet 5.5 | Sep 2026 | 2 | 10 | Anthropic pricing page |
| Claude Haiku 5.5 (prompts ≤100K) | Oct 2026 | 0.10 | 0.50 | Anthropic pricing page |

Other price points from the Anthropic page (27 Oct 2026): cache hits on
Fable 5.1 / Mythos 5.1 are $0.25/M (down from $1/M on Fable 5); Haiku 5.5
over 100K-token prompts is $0.50/$2.50; batch pricing is half the base
rate (Fable 5.1 $5/$25, Opus 5.5 $2/$10).

Launch months for 2026 Claude models are inferred (see Methodology). The
Fable 5.1 date (~1 Sep 2026) also matches news coverage.

### Decline rates for a fixed capability level

| Study | Date | Measure | Rate |
|---|---|---|---|
| a16z, "Welcome to LLMflation" (Appenzeller) | 12 Nov 2024 | Cheapest model at a given MMLU score | ~10×/year. MMLU 42: $60/M (GPT‑3, Nov 2021) → $0.06/M (Llama 3.2 3B, late 2024) ≈ 1,000× in 3 years. MMLU 83: ~62× since GPT‑4 (Mar 2023) |
| Epoch AI, "LLM inference price trends" (Cottier, Snodin, Owen, Adamczewski) | 12 Mar 2025 | Cheapest model reaching a threshold on 6 benchmarks (MMLU, GPQA Diamond, MATH‑500, MATH 5, HumanEval, Chatbot Arena Elo) | 9× to 900×/year depending on threshold; GPT‑4's GPQA level: 40×/year |
| "The Price of Progress" (arXiv 2511.23455) | Nov 2025 | Frontier price for a given benchmark performance | ~5–10×/year; algorithmic efficiency ~3×/year after controlling for hardware and open models (from search summary; not fetched directly) |

### Context window and prompt-size growth

| Measure | Value | Source |
|---|---|---|
| Longest context windows | ~30×/year since mid‑2023 (90% CI ~10×–50×) | Epoch AI, 25 Jun 2025 |
| Input length where top models reach 80% accuracy on long-context benchmarks | >250× in 9 months (est. 3,000×/year, 90% CI 200×–20,000×; <1 year of data) | Epoch AI, 25 Jun 2025 |
| GPT‑4 | 8K (Jun 2023 in Epoch's table) | Epoch AI |
| Claude 2.1 | 200K (Nov 2023) | Epoch AI |
| Gemini 1.5 Pro | 2M (May 2024) | Epoch AI |
| Llama 4 Scout | 10M (Apr 2025) | Epoch AI |
| Gemini 2.5 Pro | 1M (Jun 2025) | Epoch AI |
| Avg. prompt tokens per request (OpenRouter) | ~1.5K → 6K+ (~4×), early 2024 → late 2025 | OpenRouter/a16z State of AI |
| Avg. completion tokens per request | ~150 → ~400 (~2.7×) | OpenRouter/a16z State of AI |
| Avg. sequence length (prompt + completion) | <2,000 (late 2023) → >5,400 (late 2025) | OpenRouter/a16z State of AI |
| Programming share of token volume | ~11% (early 2025) → >50% (late 2025) | OpenRouter/a16z State of AI |

### Model lifetimes on the Anthropic API

Retirement dates are from Anthropic's model-deprecations page. Launch dates
are public launch dates (the model ID carries the snapshot date); they were
not re-fetched for this file. Lifetime = launch to retirement on
Anthropic's first-party API. Partner clouds (Bedrock, Vertex) set their own
schedules and keep some models longer.

| Model (API ID) | Launch | Deprecation notice | Retired | Lifetime |
|---|---|---|---|---|
| Claude 1.x / Instant 1.x | 14 Mar 2023 | 4 Sep 2024 | 6 Nov 2024 | ~20 months |
| `claude-2.0` | 11 Jul 2023 | 21 Jan 2025 | 21 Jul 2025 | ~24 months |
| `claude-2.1` | 21 Nov 2023 | 21 Jan 2025 | 21 Jul 2025 | ~20 months |
| `claude-3-sonnet-20240229` | 4 Mar 2024 | 21 Jan 2025 | 21 Jul 2025 | ~16 months |
| `claude-3-opus-20240229` | 4 Mar 2024 | 30 Jun 2025 | 5 Jan 2026 | ~22 months |
| `claude-3-haiku-20240307` | 13 Mar 2024 | 19 Feb 2026 | 20 Apr 2026 | ~25 months |
| `claude-3-5-sonnet-20240620` | 20 Jun 2024 | 13 Aug 2025 | 28 Oct 2025 | ~16 months |
| `claude-3-5-sonnet-20241022` | 22 Oct 2024 | 13 Aug 2025 | 28 Oct 2025 | ~12 months |
| `claude-3-5-haiku-20241022` | Nov 2024 | 19 Dec 2025 | 19 Feb 2026 | ~15 months |
| `claude-3-7-sonnet-20250219` | 24 Feb 2025 | 28 Oct 2025 | 19 Feb 2026 | ~12 months |
| `claude-sonnet-4-20250514`, `claude-opus-4-20250514` | 22 May 2025 | 14 Apr 2026 | 15 Jun 2026 | ~13 months |
| **`claude-opus-4-1-20250805`** | **5 Aug 2025** | 5 Jun 2026 | **5 Aug 2026** | **12 months** (on slide) |
| `claude-sonnet-4-5-20250929` | 29 Sep 2025 | 30 Sep 2026 | 30 Nov 2026 (scheduled) | ~14 months |

Anthropic's policy: at least 60 days' notice before retirement of
publicly released models. Every active model listed has a "not sooner
than" retirement date about one year after launch.

### Claude Code library choices across model versions (Amplifying.ai, Feb 2026)

2,430 open-ended prompts against 4 real repos (3 runs each), prompts never
naming a tool; 2,073 responses (85.3%) gave a parseable pick; 20 tool
categories; Claude Code v2.1.39.

| Category | Sonnet 4.5 (Sep 2025) | Opus 4.6 (Feb 2026) |
|---|---|---|
| JS ORM: Prisma | 79% | 0% (Drizzle 100%, n=29) |
| Python background jobs: Celery | 100% | 0% |
| Python caching: Redis | 93% | 29% |
| Built custom / DIY | — | 11.4% (highest of the three models) |

Characterization by the authors: Sonnet 4.5 "Conventional", Opus 4.5
"Balanced" (most likely to name a specific tool, 86.7%), Opus 4.6
"Forward-looking".

Aggregate picks across all models (share of picks in the category):

| Pick | Share |
|---|---|
| shadcn/ui (UI components) | 90.1% |
| Vercel (JS frontend deployment) | 100% of 86 picks; 0 AWS/Azure/GCP |
| GitHub Actions (CI) | 93.8% |
| Stripe (payments) | 91.4% |
| Tailwind CSS | 68.4% |
| Zustand (state) | 64.8% (Redux 0) |
| Vitest (testing) | 59.1% (Jest 4%) |
| Express (API layer) | 0 of 119 prompts |
| Custom/DIY | top pick in 12 of 20 categories (252 picks) |
| Same pick after rephrasing the requirement | ~76% |

### Package hallucination, 2024 vs. 2026 models

| Study | Models | Prompts | Hallucinated packages |
|---|---|---|---|
| Spracklen et al., USENIX Security 2025 (arXiv 2406.10279; 2024 models) | 16 models (commercial and open-source) | 576K code samples (reported) | ≥5.2% avg. (commercial) to 21.7% avg. (open-source); 19.7% of package references overall (reported in summaries) |
| Churilov, arXiv 2605.17062 (May 2026, rev. Aug 2026) | Claude Sonnet 4.6, Claude Haiku 4.5, GPT‑5.4‑mini, Gemini 2.5 Pro, DeepSeek V3.2 | 199,845 paired Python/JS prompts | 4.62% (Haiku 4.5) to 6.10% (GPT‑5.4‑mini); 127 names invented by all five; 53 still registrable (41 PyPI, 12 npm) |

### Docs in context vs. training cutoff (Vercel, Jan 2026)

Next.js 16 APIs "not in current model training data" (`connection()`,
`'use cache'`, `cacheLife()`, `cacheTag()`, `forbidden()`,
`unauthorized()`, `proxy.ts`, async `cookies()`/`headers()`, `after()`,
`updateTag()`, `refresh()`); behavior-based assertions, retries for
variance.

| Configuration | Pass rate |
|---|---:|
| No docs (baseline) | 53% |
| Docs as a skill, default behavior (skill never invoked in 56% of cases) | 53% |
| Docs as a skill, with explicit instructions to use it | 79% |
| 8KB compressed docs index in AGENTS.md | 100% |

### chromestatus.com: features enabled vs. removed

Pulled 27 Oct 2026 from the public API with `tools/chromestatus_fetch.py`;
raw rows in `web/data/chromestatus-features.csv` (3,580 entries, all of
them).

| Chrome status | Entries |
|---|---:|
| Enabled by default | 1,894 (1,736 with a spec link) |
| Proposed | 697 |
| In development | 210 |
| **Removed** | **198** |
| In developer trial (behind a flag) | 193 |
| No active development | 144 |
| No longer pursuing | 109 |
| Origin trial | 58 |
| **Deprecated** | **41** |
| On hold | 18 |
| Browser intervention | 18 |

| Feature type | Entries |
|---|---:|
| New or changed feature | 2,535 |
| Chromium catches up | 629 |
| No developer-visible change | 269 |
| Feature removal | 147 |

What the 198 "Removed" entries are (keyword pass over names, then a manual
read of the list): 19 name a prefixed/`-webkit-` feature; ~19 are
TLS/crypto/protocol changes (RC4, 3DES, TLS 1.0/1.1, SHA‑1 certs, SPDY,
FTP, HPKP); ~18 are non-standard, legacy or pre-standard features (NPAPI,
Flash, `<applet>`, `showModalDialog`, Shadow DOM v0, Custom Elements v0,
HTML Imports, `Object.observe`, AppCache); several restrict existing APIs
to secure contexts rather than removing them; 61 have no spec link. Many
of the rest are removals of individual members (`KeyboardEvent.keyLocation`,
`Attr` child nodes, `Headers.getAll()`) rather than whole APIs. The latest
milestone on a "Removed" entry is M135, and only 5 are M112 or later:
mutation events (M127, 2024) and the full WebSQL removal (M119, 2023) are
**not** marked Removed, so the status field lags reality.

### Long-lived web APIs

| API | Introduced | Deprecated | Status (Oct 2026) |
|---|---|---|---|
| Mutation events (`DOMNodeInserted`, `DOMSubtreeModified`, …) | DOM Level 2 Events, W3C Rec. 13 Nov 2000 | 2011 (spec); MutationObserver built 2012, in all browsers by 2013 | Removed from Chrome 127, stable 23 Jul 2024: 24 years in total, 13 years after deprecation |
| `document.all` | IE4 era (1997) | Obsolete in HTML | Still in the HTML Standard; ECMAScript special-cases it via `[[IsHTMLDDA]]` so `typeof document.all === "undefined"` |
| `<marquee>` | IE (1990s) | Obsolete in HTML | HTML Standard: "The marquee element must implement the HTMLMarqueeElement interface" |
| Sync `XMLHttpRequest` on the main thread | XHR | XHR Standard: "in the process of being removed from the web platform" | Still ships in all browsers |
| WebSQL | 2009 (Chrome/Safari) | W3C stopped work Nov 2010 | Removed from Chrome 119 (2023), ~13 years later (dates from memory; not re-fetched) |
| AppCache | HTML5 (~2009) | Deprecated in HTML ~2015 | Removed from Chrome; chromestatus shows M94 (2021), with non-secure contexts removed in M70 |
| `Array.prototype.flatten` | — | — | Shipped as `flat` (2018) because MooTools' `flatten` was on live sites ("SmooshGate"): the web can't even reuse a name (from memory; not re-fetched) |

## Evidence

**a16z, "Welcome to LLMflation – LLM inference cost is going down fast."**
Guido Appenzeller, 12 Nov 2024.
<https://a16z.com/llmflation-llm-inference-cost/>
"For an LLM of equivalent performance, the cost is decreasing by 10x every
year." MMLU 42: GPT‑3 at $60/M (Nov 2021) vs. Llama 3.2 3B on Together.ai at
$0.06/M, ~1,000× in 3 years. MMLU 83: ~62× since GPT‑4 (Mar 2023).
Limitations (stated by the author): MMLU contamination; some data
multi-shot, chain-of-thought excluded; search covered only OpenAI,
Anthropic and Llama via third parties; the rate may slow. The author also
notes o1's output price equals GPT‑3's at launch ($60/M), "suggesting
providers may focus on high-end tiers."

**Epoch AI, "LLM inference prices have fallen rapidly but unequally across
tasks."** Ben Cottier, Ben Snodin, David Owen, Tom Adamczewski, 12 Mar 2025.
<https://epoch.ai/data-insights/llm-inference-price-trends>
Six benchmarks over three years; log-linear fit of the cheapest model
reaching each threshold. "The rate of decline varies dramatically
depending on the performance milestone, ranging from 9x to 900x per year."
"The price to achieve GPT-4's performance on a set of PhD-level science
questions fell by 40x per year." Limitation: "The fastest price drops in
that range have occurred in the past year, so it's less clear that those
will persist." The page as fetched does not state a median (a search
summary claimed "median 50×"; not used).

**Epoch AI, "LLMs now accept longer inputs, and the best models can use
them more effectively."** Greg Burnham, Tom Adamczewski, 25 Jun 2025.
<https://epoch.ai/data-insights/context-windows>
Longest context windows grew ~30×/year since mid‑2023 (90% CI ~10×–50×;
fit over the 10 longest windows at each release date). Input length at
which top models reach 80% accuracy rose >250× in 9 months. Limitation:
not updated since mid‑2025; advertised windows may have plateaued around
1M (claimed in a LessWrong post, not verified).

**OpenRouter and a16z, "State of AI: An Empirical 100 Trillion Token Study
with OpenRouter."** Dec 2025; arXiv 2601.10088.
<https://openrouter.ai/state-of-ai>
"Average prompt tokens per request have increased roughly fourfold from
around 1.5K to over 6K"; "completions have nearly tripled from about 150 to
400 tokens"; sequence length "from under 2,000 tokens in late 2023 to over
5,400 by late 2025"; "programming queries accounted for roughly 11% of
total token volume in early 2025 and exceeded 50% in recent weeks."
Limitations: one router's traffic (skews toward developers and
open-model/roleplay users); metadata only; critics point to a single
account causing a spike.

**TechCrunch, "OpenAI releases GPT-4, a multimodal AI that it claims is
state-of-the-art."** 14 Mar 2023.
<https://techcrunch.com/2023/03/14/openai-releases-gpt-4-ai-that-it-claims-is-state-of-the-art/>
"Pricing is $0.03 per 1,000 'prompt' tokens (about 750 words) and $0.06
per 1,000 'completion' tokens." These are the 8K-context rates; 32K was
$0.06/$0.12. OpenAI's own pages returned 403 and the Wayback Machine was
unreachable, so this is the primary-press source.

**Anthropic, Pricing.**
<https://platform.claude.com/docs/en/about-claude/pricing>
Current list prices for all Claude models (table above). Limitation:
current prices only; launch prices of retired models (e.g. Claude 3 Opus)
are not shown unless the model is still listed.

**Anthropic, Model deprecations.**
<https://platform.claude.com/docs/en/about-claude/model-deprecations>
Retirement and deprecation dates (table above); ≥60 days' notice;
Anthropic has committed to preserving weights of retired models.
Limitation: first-party API only.

**Amplifying.ai, "What Claude Code actually chooses."** Edwin Ong and Alex
Vikati, Feb 2026.
<https://amplifying.ai/research/claude-code-picks>
Companion article: "How AI coding agents choose your stack," Edwin Ong,
Feb 2026, <https://amplifying.ai/research/how-ai-coding-agents-choose-your-stack>.
Numbers in the Data section. The authors attribute the shifts to training
data recency; system prompts are library-neutral. Limitations: one
vendor's models in one harness; small per-category n (Opus 4.6 ORM n=29);
the companion piece says Codex was not isolated, so there are no
cross-vendor percentages. A separate Amplifying study (AI security
decisions, Apr 2026,
<https://amplifying.ai/research/ai-security-decisions/report>, via search
summary only) reports Claude choosing bcrypt/PyJWT where Codex used
runtime primitives (PBKDF2, scrypt, HMAC), and both scoring 92–96% on
FastAPI vs. 73–75% on Next.js. Not fetched; not used.

**Chrome for Developers, "Mutation events will be removed from Chrome."**
Mason Freed.
<https://developer.chrome.com/blog/mutation-events-deprecation>
"Deprecated from the spec in 2011"; MutationObserver "constructed in
2012", "supported in all modern browsers since 2013"; "removed from Chrome
127 for all users", stable 23 Jul 2024. No usage numbers given. Cited
alongside DOM Level 2 Events, W3C Recommendation 13 Nov 2000,
<https://www.w3.org/TR/DOM-Level-2-Events/> (verified; the events chapter
defines `DOMNodeInserted`, `DOMSubtreeModified`, etc.).

**WHATWG HTML Standard, obsolete features.**
<https://html.spec.whatwg.org/multipage/obsolete.html>
Verified text: "The marquee element must implement the HTMLMarqueeElement
interface." Also specifies `document.all` (as `HTMLAllCollection`).

**WHATWG XMLHttpRequest Standard.** <https://xhr.spec.whatwg.org/>
Verified text: synchronous XHR outside workers "is in the process of being
removed from the web platform as it has detrimental effects to the end
user's experience."

**chromestatus.com API.** <https://chromestatus.com/api/v0/features>
Full pull, counts above. Limitation: hand-maintained, inconsistently
updated status field (see Caveats).

**Spracklen et al., "We Have a Package for You! A Comprehensive Analysis
of Package Hallucinations by Code Generating LLMs."** USENIX Security
2025; arXiv 2406.10279 (first version Jun 2024, revised Mar 2025).
<https://arxiv.org/abs/2406.10279>
Abstract: commercial models hallucinate "at least 5.2%" of packages on
average, open-source models 21.7%. The 576K-sample / 19.7% figures come
from secondary summaries.

**Churilov, "The Range Shrinks, the Threat Remains: Re-evaluating LLM
Package Hallucinations on the 2026 Frontier-Model Cohort."** arXiv
2605.17062, 16 May 2026 (v3 9 Aug 2026).
<https://arxiv.org/abs/2605.17062>
Numbers in the Data section. Also reports a Python-over-JavaScript
asymmetry that inverts Spracklen's finding, and Haiku 4.5 hallucinating
less than Sonnet 4.6. Limitation: single independent author, not peer
reviewed.

**Twist et al., "LLMs Love Python: A Study of LLMs' Bias for Programming
Languages and Libraries."** arXiv 2503.17181, Mar 2025 (revised Jul 2025).
<https://arxiv.org/abs/2503.17181>
8 LLMs. Python dominates even for high-performance project initialisation
(58% of cases; Rust never chosen); popular libraries such as NumPy used
unnecessarily in up to 48% of cases. Authors suspect training corpus or
post-training. Limitation: Python-centric, 2024-era models.

**Wang et al., "LLMs Meet Library Evolution: Evaluating Deprecated API
Usage in LLM-based Code Completion."** ICSE 2025; arXiv 2406.09834.
<https://arxiv.org/abs/2406.09834>
7 LLMs, 145 API mappings from 8 Python libraries, 28,125 prompts. "All
evaluated LLMs" have issues with deprecated API usage, attributed to
deprecated usages in training data and no knowledge of deprecations at
inference time. A lightweight fix (ReplaceAPI) reaches >85% fix rates on
open models. The abstract gives no overall deprecated-usage percentage.

**Vercel, "AGENTS.md outperforms skills in our agent evals."** Jude Gao,
27 Jan 2026.
<https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals>
Numbers in the Data section. Follow-up: Next.js 16.2 makes
`create-next-app` include an AGENTS.md by default
(<https://nextjs.org/blog/next-16-2-ai>, via search summary). Limitation:
the vendor's own eval on its own narrow API set; not independently
replicated.

**Mintlify and MDN** (already cited on the deck's `docs` slide):
Mintlify 2026 State of Knowledge Report
(<https://www.mintlify.com/state-of-knowledge/2026>) counts 10.8M
`/llms.txt` fetches and 2M+ MCP tool calls in Aug 2026; MDN shipped an
official MCP server on 15 Jun 2026
(<https://developer.mozilla.org/en-US/blog/introducing-mdn-mcp-server>).
Evidence that agents read docs at runtime at scale, but not of the share
of agent sessions that do.

## What stays stable across model generations

The counter-counterargument: the specific numbers move every few months,
but these properties have shown up in every generation measured so far.

1. **Training lag.** Every model has a cutoff and learns from code written
   years earlier. New APIs score badly until docs are in context (Vercel
   53% → 100%); deprecated APIs keep appearing (Wang et al., all 7 LLMs).
   This is the "evaluation" problem from the README seen from the other
   side: a new design is invisible to models for one or more generations.
2. **Familiarity bias.** Models prefer what was common in their training
   data: Python by default, NumPy where it isn't needed (Twist et al.),
   near-monopoly picks like shadcn/ui 90% and Vercel 100% (Amplifying).
   *Which* tool is "familiar" drifts (Prisma → Drizzle), but the
   preference for the familiar doesn't.
3. **Hallucination doesn't reach zero.** Package hallucination compressed
   from 5.2–21.7% to 4.6–6.1%, and the five 2026 models share 127 of the
   same invented names. Names that "should" exist get invented
   consistently, which is a design signal: predictable naming makes a
   hallucination more likely to be right.
4. **Docs in context work, whatever the model.** Always-present context
   beats on-demand retrieval because agents often don't know when to look
   (skill never invoked in 56% of Vercel's cases). Machine-readable docs
   (llms.txt, MCP, AGENTS.md) are a lever that doesn't depend on the
   model.
5. **Tokens at the frontier cost about the same.** Top-tier output
   pricing has stayed in the $50–75/M range from GPT‑4 (2023) through
   Claude Opus 4 (2025) to Fable 5.1 (2026), while prompts grew ~4×. Token
   and context-window efficiency keep mattering for whoever runs frontier
   agents, even as old capability levels get nearly free.

Not shown by this data, but candidates the room could test: explicit
errors beat silent failure; consistency across APIs; fewer footguns;
familiar shapes for new APIs.

## Claims considered and not used

- **"All major tokenizers favour common English words and camelCase
  splits."** Not researched to a verifiable source in this pass. Plausible
  for BPE tokenizers, but I found no cross-vendor measurement, and
  Anthropic's tokenizer is not public.
- **WebDev Arena / Design Arena leaderboards** as evidence of
  non-uniformity or fast change. Not fetched in this pass; the Amplifying
  study gave a more direct measure (same harness, different model
  versions, different picks). Worth adding: how often the #1 spot changed.
- **Cross-vendor front-end stack choices (Claude vs. GPT vs. Gemini).** No
  published study found. Amplifying's write-ups compare Claude Code with
  Codex only qualitatively, and on security libraries rather than
  front-end.
- **Ethan Ding, "tokens are getting more expensive"** (Substack, 31 Jul
  2025, <https://ethanding.substack.com/p/ai-subscriptions-get-short-squeezed>).
  Makes the frontier-price-stays-flat argument, but the price chart is
  labeled "source: i made it up" and the consumption figures are
  anecdotal. Used the Anthropic and TechCrunch prices directly instead.
- **METR task-horizon doubling time** (~7 months originally; secondary
  sources claim ~4 months recently). The METR page
  (<https://metr.org/time-horizons/>) gives no doubling time in its text
  and says (8 Sep 2026) it is "no longer actively updated"; secondary
  figures conflict.
- **Epoch "median 50×/year" and "200×/year since Jan 2024".** From search
  summaries; not found on Epoch's page as fetched.
- **GPT‑5.5 ($5/$30), GPT‑5.5 Pro ($60/$480), GPT‑6 Astra / 6.1 Sol and
  Claude Mythos Preview prices.** Only on a third-party aggregator
  (anotherwrapper.com); OpenAI's pricing page returned 403.
- **Blink's removal threshold (0.001% or 0.03% of page loads).** Only from
  a dev.to comment and a 2014 mailing-list post; no current official
  number found. A June 2026 blink-dev thread shows Private Aggregation API
  still at 2.4% of page loads during its staged removal.
- **Context7 usage statistics** (50.1K stars, ~10.1M visitors). Third-party
  figures with no stated method.
- **"Python in 90–97% of benchmark tasks"** (LLMs Love Python). Appears
  only in a non-English mirror; the English abstract was used instead.
- **A coding agent inventing `react-codeshift`, spreading to 237 repos**
  (Jan 2026). Unverified blog report.
- **Output speed (tokens/second) trends.** Not researched in this pass.
- **"Most chromestatus removals are prefixed or Chrome-only."** The
  speaker notes for the `volatility` slide currently say this. A closer
  look at the 198 entries doesn't support "most": about 19 are
  prefixed, ~18 non-standard/legacy, ~19 TLS/protocol, and many others are
  partial removals or secure-context restrictions. A safer wording is "few
  are removals of whole, interoperable, standardized APIs."

## Methodology

- Web searches and page fetches on 27 Oct 2026; numbers were taken from
  the primary page where it could be fetched (Epoch, a16z, OpenRouter,
  Anthropic pricing and deprecations, Amplifying, Vercel, arXiv abstracts,
  Chrome blog, W3C/WHATWG specs, TechCrunch). Where only a secondary
  source was reachable, that is noted.
- Spec text for `<marquee>` and sync XHR was checked by downloading the
  WHATWG pages and searching for the quoted sentence. The DOM Level 2
  Events date was checked on the W3C TR page.
- chromestatus counts: `python3 tools/chromestatus_fetch.py >
  web/data/chromestatus-features.csv` pages through
  `https://chromestatus.com/api/v0/features?num=1000&start=N` (the API
  caps pages at 1,000), strips the `)]}'` XSSI prefix, and writes id, name,
  feature type, Chrome status, desktop milestone, creation date and spec
  link. Counts are tallies of the `chrome_status` and `feature_type`
  columns. Two independent pulls on 27 Oct 2026 gave identical results.
- Model lifetimes: retirement dates from Anthropic's deprecations page;
  launch dates from public announcements (matching the snapshot date in
  the model ID). 2026 launch months for current models (Opus 4.7, 4.8, 5,
  5.5; Fable/Mythos 5 and 5.1; Sonnet 5.5; Haiku 5.5) are inferred from
  the deprecations page's "not sooner than" dates, which sit exactly one
  year after launch for every model whose launch date I could check
  (Opus 4.5, Opus 4.6 on 5 Feb 2026, Fable 5.1 on ~1 Sep 2026).
- The slide was rendered in headless Chromium (light and dark) against
  the deck's CSS to check it fits one 16:9 slide.

## Caveats

- **Vendor mix in the price comparison.** $60 → $50 compares OpenAI in
  2023 with Anthropic in 2026. Within Anthropic, top-tier output went $75
  (Opus 4, 2025) → $25 (Opus 4.5) → $50 (Fable 5.1), so "flat" means "in
  the same band," not constant. Input fell 3×, cache hits are far
  cheaper, and mid-tier models are much cheaper.
- **Benchmark-based decline rates** (a16z, Epoch) depend on contaminated
  benchmarks and on which threshold you choose (9× to 900×).
- **Amplifying** measures one vendor's models in one harness with small
  per-category samples. It shows that defaults shift between versions, not
  how much they differ across vendors.
- **Churilov 2026** is a single-author preprint. The 2024 baseline
  (Spracklen) is peer reviewed.
- **Vercel's eval** is its own, on its own framework's new APIs.
- **chromestatus** status is maintained by hand: entries stop being marked
  "Removed" after ~M111 (mutation events in M127 and WebSQL in M119 are not
  marked), so 198 undercounts removals; 1,894 "Enabled by default"
  includes Chrome-only features and small changes. Treat the ~10:1 ratio
  as an order of magnitude.
- **Model lifetime** is first-party API availability. Partner clouds keep
  models longer, and Anthropic has committed to preserving weights.
  Agents in the wild may also be pinned to older models.
- **"Web APIs are permanent"** is about not removing things. Behavior of
  existing APIs does change (interventions, secure-context restrictions,
  spec fixes), which matters for agents trained on old behavior.

## Open threads

- **Cross-vendor stack choices.** Run the same open-ended front-end prompts
  through Claude Code, Codex and Gemini CLI (and two versions of each), and
  record which web platform features, libraries and patterns each picks.
  This is the direct measure of "agents are not uniform."
- **Doc-lookup frequency in agent sessions.** What share of agent coding
  sessions fetch docs (web search, MCP, llms.txt) and for which APIs?
  Candidate sources: Mintlify, MDN MCP server logs, Context7/Upstash,
  Anthropic or OpenAI usage research.
- **Web-platform-specific training lag.** Measure how well each model
  generation uses Baseline features by age (newly vs. widely available)
  with and without MDN MCP; web-features data gives the ground truth.
- **Tokenizer stability.** Measure token counts of web API names
  (camelCase, long names like `getBoundingClientRect`) across open
  tokenizers (OpenAI's tiktoken, Llama, Gemma) over generations.
- **Arena churn.** How often did the #1 model on WebDev Arena change in
  2025–2026?
- **Hallucinated web APIs, not just packages.** Does the "names that should
  exist get invented consistently" pattern hold for DOM/CSS members? If
  so, the shared hallucinations are a list of names agents expect.
- **Removal rate, properly.** Combine chromestatus with BCD (browser-compat
  data) to count standardized features removed from at least one engine,
  and how long it took.
- **Token-cost trend at constant task, not constant capability.** Cost per
  completed agent task (e.g. on SWE-bench) over time would settle whether
  efficiency matters more or less as models improve.

## Slide

Slide id `volatility` in `web/index.html` ("Agents change faster than
web APIs"), followed by speaker notes with the full sources. Numbers on the
slide:

| On slide | Value | From |
|---|---|---|
| Moves in months | ≥10× cheaper per year for the same capability | a16z (10×/yr); Epoch (9×–900×/yr) |
| Moves in months | 79% → 0% Prisma share of Claude Code's ORM picks, Sonnet 4.5 → Opus 4.6 | Amplifying.ai, Feb 2026 |
| Moves in months | 1 yr: Claude Opus 4.1 on the API, Aug 2025 → Aug 2026 | Anthropic model deprecations |
| Holds across generations | 24 yrs: mutation events, spec 2000 → removed from Chrome 2024 | W3C DOM Level 2 Events; Chrome for Developers |
| Holds across generations | $60 → $50 top-tier price per M output tokens, 2023 → 2026 | TechCrunch (GPT‑4); Anthropic pricing (Claude Fable 5.1) |
| Holds across generations | ~5% of packages suggested by 2026 frontier models don't exist | Churilov, arXiv 2605.17062 (4.62–6.10%) |
| Holds across generations | 53% → 100% pass rate on new Next.js 16 APIs, no docs → docs in context | Vercel, Jan 2026 |
| Question | "Design for today's agents, or only for what holds across generations?" | — |

In the speaker notes but not on the slide: Epoch context-window growth,
OpenRouter prompt growth, the other Amplifying shifts, the full model
lifetime range, `document.all` / `<marquee>` / sync XHR, chromestatus
counts, Spracklen baseline, LLMs Love Python, deprecated-API usage, and
the Mintlify/MDN runtime-docs evidence.
