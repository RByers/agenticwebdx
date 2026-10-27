# Evaluating API designs under a delayed feedback loop

Research notes behind the `evaluation` slide of the TPAC 2026 breakout
session *Agents are redefining DX. [How] should web standards adapt?*
Compiled 27 Oct 2026.

## Question

From the session description in [README.md](../README.md):

> **Evaluation:** An API's token cost is not an intrinsic property. An agent
> implementing an unfamiliar API spends tokens on lookup, trial and error, and
> correction, so a design that would be more token-efficient at parity of
> familiarity measures as worse until training data catches up — which takes
> years. Any evaluation we run today privileges familiar over better. How do we
> separate the two, and how do we evaluate API designs, or design principles,
> given such a delayed feedback loop?

## Key findings

1. **Familiarity is a large, measurable term, not a rounding error.**
   - *Accuracy.* Rust APIs released after a model's training cutoff are solved
     at 32.5% pass@1, vs. 56.1% for APIs from before it (RustEvo², 5-model
     average).
   - *Pure renaming.* Renaming every pandas keyword without changing the design
     dropped Codex 12B from 18.88% to 1.47% pass@1 (Zan et al. 2022).
2. **For frontier models, the penalty shows up as cost more than as
   failure.**
   - On identical problems with difficulty controlled, agents spend 1.28–1.69×
     the output tokens in OCaml vs. Python (Wu, Anderson & Guha 2026). Pass
     rates barely move.
   - The final code is about the same size. The extra tokens go to
     non-compiling attempts, debugging and reverting.
   - This is the session's premise, observed directly: token cost depends on
     familiarity, not just on the design.
3. **Models default to what they've seen, including the old way.**
   - Among completions that use either a deprecated API or its replacement,
     25–38% use the deprecated one. That rises to 70–90% when the surrounding
     code is outdated (Wang et al., ICSE 2025).
   - LLMs overuse popular libraries "in up to 45% of cases" where they are not
     needed, prioritising "familiarity and popularity over suitability" (Twist
     et al., ACL Findings 2026).
4. **Docs in context help, but don't reliably reach parity.**
   - *Partial gains.* RustEvo²: docs in the prompt lift post-cutoff APIs from
     32.5% to 41.4%, but lift pre-cutoff APIs more (56.1% → 70.9%). RAG adds
     about 10–14 points in RustEvo² and GitChameleon 2.0.
   - *Full parity in an agent setting.* Vercel reports 53% → 100% on Next.js
     16 APIs missing from training data with an 8 KB docs index in
     `AGENTS.md`. Skills the agent had to decide to invoke gave 53% by default
     (not invoked in 56% of cases) and 79% when told to use them.
   - *Docs can hurt.* Naive doc retrieval *hurts* familiar APIs, by up to 39
     points (CloudAPIBench).
5. **Hardly anyone measures this for the web platform.**
   - I found no study of how often agents use newly Baseline features
     (`:has()`, nesting, popover, View Transitions, anchor positioning, Temporal,
     Navigation API) vs. older patterns.
   - The web-specific evidence is:
     - an informal MDN test: Opus 4.7 without the MDN MCP got browser support
       right for 1 of 4 features new in Firefox 151;
     - Chrome's claim of a 37-point best-practice gain from Modern Web
       Guidance, with no methodology published;
     - practitioner anecdotes.
6. **Methods that separate familiarity from design exist, but nobody has
   applied them to API design.**
   - Renamed or synthetic APIs, minimal pairs, unguided-control evals and
     "LLM-as-a-developer" cost proxies have all been used, but not yet to
     compare two candidate *designs* at equal familiarity.

## Data

### RustEvo²: before vs. after training cutoff, with and without API docs

Source: Liang et al. 2025, Table 3. Pass@1 (%). The before-cutoff tasks (204)
use APIs from Rust 1.71–1.73; the after-cutoff tasks (220) use Rust 1.81–1.84.
"Info" means the API's information is provided in the prompt. I recomputed the
averages from the per-model values and they match the paper.

| Model | Before, no info | Before, with info | After, no info | After, with info | Stated cutoff |
|---|---|---|---|---|---|
| DeepSeek-v3 | 57.4 | 71.6 | 34.1 | 46.4 | 2024-07 |
| Gemini 2.0 Flash | 54.4 | 73.5 | 35.9 | 40.0 | 2024-06 |
| Gemini 1.5 Pro | 52.9 | 69.1 | 32.7 | 42.7 | 2024-03 |
| Llama 3.1 70B | 53.9 | 67.2 | 29.1 | 36.4 | 2023-12 |
| o1-mini | 61.8 | 73.0 | 30.5 | 41.4 | 2023-10 |
| **Average** | **56.1** | **70.9** | **32.5** | **41.4** | |

Docs lift familiar APIs by +14.8 points and unfamiliar ones by +8.9.

RustEvo² Table 4: after-cutoff APIs only, with RAG. Pass@1 (%).

| Model | No API info | With RAG | With API info |
|---|---|---|---|
| Claude 3.7 Sonnet | 41.2 | 54.8 | 65.3 |
| o1-mini | 35.6 | 49.3 | 57.5 |
| DeepSeek-v3 | 34.0 | 46.5 | 54.8 |
| Gemini 1.5 Pro | 32.7 | 42.9 | 55.3 |
| GPT-4o | 30.8 | 48.4 | 55.4 |
| **Average** | **34.9** | **48.4** | **57.7** |

The abstract's "+13.5%" for RAG is an absolute gain of 13.5 points
(48.4 − 34.9). Tables 3 and 4 differ slightly for models that appear in both
(e.g. o1-mini after/no-info: 30.5 vs. 35.6), so they are probably different
task subsets or runs. Don't mix their numbers.

Other RustEvo² headline numbers: 65.8% average success on stabilized APIs vs.
38.0% on behavioral changes.

### Wu, Anderson & Guha 2026: token cost by language at controlled difficulty

Output tokens relative to Python, from a mixed-effects model (problem as a
random intercept). 100 LiveCodeBench problems, mini-swe-agent, 2,000
trajectories.

| Model | Java | Rust | OCaml |
|---|---|---|---|
| Claude Sonnet 4.6 | 1.18× | 1.16× | 1.28× |
| GPT-5.5 | 1.30× | 1.36× | 1.30× |
| Gemma-4-26B-A4B | 0.85× (n.s.) | 1.07× (n.s.) | 1.44× |
| Qwen3.6-35B-A3B | 1.21× | 1.20× | 1.69× |
| GLM-5.2 | 1.34× | 1.57× | 1.54× |

Median output tokens (Table 17):

| Model | Python | Java | Rust | OCaml |
|---|---|---|---|---|
| Gemma | 11,099 | 11,552 | 15,014 | 23,097 |
| Qwen | 2,830 | 3,357 | 4,045 | 8,546 |
| GLM | 861 | 902 | 1,679 | 1,587 |
| GPT-5.5 | 643 | 890 | 834 | 965 |
| Sonnet | 1,348 | 1,407 | 1,324 | 1,865 |

- The size of the final solution is not the cause: median representation cost
  is 272 tokens for OCaml vs. 276 for Java and 303 for Rust.
- The extra tokens are labelled error recovery: fixing bugs, debugging
  failures and reverting.
- Pass rates are 92–100% for GPT-5.5, GLM and Sonnet in every language.
  Gemma is the exception, at 62% on OCaml vs. 82–86% elsewhere.
- Intraclass correlation is 0.73–0.97: the problem explains most of the
  variance in tokens.

### Wang et al. (ICSE 2025): deprecated API usage in code completion

145 deprecated→replacement mappings, 8 Python libraries, 28,125 prompts.
DUR is the deprecated usage rate among *plausible* completions (those that
match either the deprecated API or its replacement).

| Model | DUR, outdated context | DUR, up-to-date context | DUR, overall |
|---|---|---|---|
| CodeGen-350M | 77.7% | 9.0% | 24.9% |
| CodeGen-2B | 89.6% | 11.3% | 32.6% |
| CodeGen-6B | 90.0% | 11.1% | 34.2% |
| DeepSeek-Coder-1.3B | 69.7% | 11.6% | 27.2% |
| StarCoder2-3B | 79.4% | 17.0% | 34.4% |
| CodeLlama-7B | 86.9% | 12.1% | 34.2% |
| GPT-3.5 | 85.7% | 17.8% | 37.4% |

Mitigations, as the fix rate on samples that originally produced deprecated
usage:

- ReplaceAPI (decoding-time substitution): 85.2–99.6%.
- InsertPrompt (a prompt hint): 25.7–97.2% (GPT-3.5: 97.2%). The authors say
  it "does not achieve sufficient effectiveness and accuracy".

### Vercel (27 Jan 2026): Next.js 16 APIs not in training data

| Configuration | Overall pass | Build | Lint | Test |
|---|---|---|---|---|
| Baseline, no docs | 53% | 84% | 95% | 63% |
| Docs skill, default | 53% | 84% | 89% | 58% |
| Docs skill, explicitly instructed | 79% | 95% | 100% | 84% |
| 8 KB docs index in `AGENTS.md` | 100% | 100% | 100% | 100% |

- The skill was never invoked in 56% of cases.
- The index was compressed from about 40 KB to 8 KB and kept 100%.
- The APIs tested included `'use cache'`, `connection()`,
  `cacheLife()`/`cacheTag()`, `forbidden()`/`unauthorized()`, `proxy.ts`,
  async `cookies()`/`headers()`, and `after()`/`updateTag()`/`refresh()`.

### Zan et al. (EMNLP Findings 2022): same design, renamed

| Benchmark | Codex 12B pass@1 |
|---|---|
| PandasEval (real pandas) | 18.88% |
| MonkeyEval (every pandas keyword renamed) | 1.47% |

Example renamings: `pandas`→`monkey`, `dataframe`→`knowledgeframe`,
`isin`→`iscontain`. BeatNumEval does the same for NumPy. Each benchmark has 101
problems. CodeGen-Mono 350M also drops sharply (Figure 1).

### Other numbers collected

| Source | What was measured | Number |
|---|---|---|
| CloudAPIBench (Jain et al. 2024) | GPT-4o valid invocations of low-frequency APIs | 38.58%, rising to 47.94% with documentation-augmented generation |
| CloudAPIBench | High-frequency APIs with a sub-optimal retriever | −39.02 points |
| CloudAPIBench | Selective documentation retrieval (API index or model confidence), GPT-4o | +8.20 points overall |
| GitChameleon (2024) | GPT-4o pass@10 on 116 version-specific problems | 39.9%; 43.7% with error feedback |
| GitChameleon 2.0 (NeurIPS 2025) | Greedy success on hidden tests, 328 problems | o1 51.2%, Gemini 2.5 Pro 50.0%, GPT-4o 49.1%, Claude 3.7 Sonnet 48.8%, GPT-4.1 48.5%, Llama 4 Maverick 40.8% |
| GitChameleon 2.0 | RAG, k=3 | GPT-4.1 48.5% → 58.5%; Claude 4 Sonnet 59.4%; "up to 10%" gain; >40% of problems unsolved in the best case |
| GitChameleon 2.0 | Self-debugging | +10–20 points on hidden tests; the gap between visible and hidden tests widens |
| Twist et al. (ACL Findings 2026) | Unnecessary use of popular libraries | Up to 45% of cases; Python is chosen for 58% of high-performance tasks, Rust never |
| MDN MCP blog (June 2026) | Claude Code (Opus 4.7) without the MCP, browser support for 4 features new in Firefox 151 | 1 of 4 correct; answers with the MCP were "roughly twice as fast" |
| Chrome Modern Web Guidance docs | Best-practice adherence with vs. without the guidance | "On average… a 37 percentage point improvement" |
| ADK Arena (June 2026) | LLM-as-a-developer generation cost across 51 Python agent frameworks | 5.6× spread ($0.6–$3.4 per agent); generation succeeds in 57% of runs; real use of each framework 28–40% across doc and source ablations (33% with no reference material) |
| Trivedi & Schmitt (2026) | Clean vs. messy repo minimal pairs, Claude Code, 660 trials | Same pass rate; 7–8% fewer tokens and 34% fewer file revisits on clean code |
| Constraint Decay (2026) | Backend agents as structural constraints accumulate | −27.28 points in assertion pass rate; worse in convention-heavy frameworks (FastAPI, Django) than in Flask |
| Gao & Chen (2026) | What coding agents read, from 3,033 documentation interactions | 60.5% instruction files and notes, 10.6% classic docs, 1.3% API references; consultation is self-initiated 70.2% of the time and failure-driven 7.5% |
| ExploraCoder (2024) | Unseen Torchdata APIs | +11.99 points pass@10 over retrieval-based methods, +17.28 over pretraining-based methods |
| Anthropic tool-writing post (2025) | Detailed vs. concise tool response | 206 vs. 72 tokens |

## Evidence from the literature

**Liang, Gong, Liu, Wang, Ou, Wang, Peng, Zheng. *RustEvo²: An Evolving
Benchmark for API Evolution in LLM-based Rust Code Generation.* arXiv
2503.16922, March 2025.** <https://arxiv.org/abs/2503.16922>

- *What it measures:* 588 real Rust API changes (380 from the standard
  library, 208 from 15 crates), in four categories: stabilizations, signature
  changes, behavioral changes and deprecations. Each change is turned into a
  coding task.
- *Numbers:* see the tables above.
- *Why it matters:* it is the only study I found that directly splits APIs by
  model cutoff and also tests docs in context. That gives a 2×2 of familiarity
  × docs, which is the slide's chart.
- *Limitations:*
  - The before and after task sets use different APIs, so difficulty is not
    controlled.
  - Cutoffs are given for only 5 of the 10 models.
  - The models are early-2025 vintage, and it covers Rust, not the web.

**Wu, Anderson, Guha. *The Best Programming Language for Tokenmaxxing: An
Investigation of Coding Agent Behavior Across Programming Languages.* arXiv
2607.22807, July 2026.** <https://arxiv.org/abs/2607.22807>

- *What it measures:* token consumption of 5 current models on the same 100
  problems in 4 languages, with mixed-effects control for difficulty. It also
  re-executes each intermediate solution and labels the work done between
  them.
- *Numbers:* see the tables above.
- *Why it matters:* it is the closest thing to a direct measurement of the
  session's claim, because it varies familiarity and observes tokens.
  - Frontier models still succeed, so the penalty shows up as cost (retries,
    fixes, reverts), not as the code itself being longer.
  - Agents "sidestep unfamiliar target languages by prototyping in Python".
- *Limitations:*
  - It compares languages, not APIs.
  - Training-data volume is the authors' hypothesis, not tested. The Stack v2
    has about 200 GB of Java and Python, 12 GB of Rust and less OCaml.
  - It uses competitive-programming problems.

**Wang, Huang, Zhang, Feng, Zhang, Liu, Peng. *LLMs Meet Library Evolution:
Evaluating Deprecated API Usage in LLM-based Code Completion.* ICSE 2025
(arXiv 2406.09834).** <https://arxiv.org/abs/2406.09834>

- *What it measures:* how often completions pick the deprecated API over its
  replacement, and two mitigations.
- *Numbers:* see the tables above.
- *Why it matters:* it is the "old way wins" effect. The surrounding code
  matters a lot: outdated context gives 70–90% deprecated usage. That suggests
  legacy web code perpetuates legacy patterns (XHR, `var`, float layouts,
  jQuery-isms).
- *Limitations:*
  - Small 2023-era open models plus GPT-3.5.
  - Python libraries only.
  - Rates are conditional on plausible completions; API usage plausibility was
    only 9.3–23.4%.

**Vercel (Jude Gao). *AGENTS.md outperforms skills in our agent evals.* 27 Jan
2026.**
<https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals>

- *What it measures:* agent pass rate on Next.js 16 APIs absent from training
  data, under four ways of providing docs.
- *Numbers:* see the table above.
- *Why it matters:*
  - It is the strongest evidence that docs in context can bring an unfamiliar
    API to parity in an agent setting.
  - The delivery mechanism matters: always-present context beats on-demand
    retrieval, because agents often don't decide to look things up.
  - Next.js 16.2 now ships `AGENTS.md` in `create-next-app`.
- *Limitations:*
  - Vendor eval, and the model is not named.
  - Small suite, revised during the study.
  - Results were sensitive to how the instruction was worded.

**Zan, Chen, Lin, Guan, Wang, Lou. *When Language Model Meets Private Library.*
EMNLP Findings 2022 (arXiv 2210.17236).** <https://arxiv.org/abs/2210.17236>

- *What it measures:* code generation for private libraries (TorchDataEval,
  50 problems) and for pseudo-private renamed copies of pandas and NumPy
  (MonkeyEval and BeatNumEval, 101 problems each).
- *Numbers:* Codex 12B: 18.88% → 1.47% pass@1, PandasEval → MonkeyEval.
- *Why it matters:* it is the cleanest isolation of familiarity. The design is
  identical and only the names differ, so the whole drop is familiarity. The
  same technique could compare two API *designs*, both renamed, at equal
  (zero) familiarity.
- *Limitations:*
  - 2022 models. Current models may transfer much better from the semantics.
  - Renaming also removes useful transfer that a real new design would get
    from similar APIs.

**Jain, Kwiatkowski, Ray, Ramanathan, Kumar. *On Mitigating Code LLM
Hallucinations with API Documentation* (CloudAPIBench). arXiv 2407.09726, July
2024.** <https://arxiv.org/abs/2407.09726>

- *What it measures:* valid API invocations by how often an API appears in
  training data.
- *Numbers:*
  - GPT-4o on low-frequency APIs: 38.58%, or 47.94% with
    documentation-augmented generation (DAG).
  - Sub-optimal retrieval costs high-frequency APIs 39.02 points.
  - Selective DAG: +8.20 points overall.
- *Why it matters:* it is a direct frequency (familiarity) effect, and it
  shows docs can *hurt* familiar APIs. An eval that adds docs to both arms
  isn't automatically neutral.
- *Limitations:* AWS cloud APIs; 2024 models.

**Islah et al. *GitChameleon* (arXiv 2411.05830, Nov 2024) and *GitChameleon
2.0* (arXiv 2507.12367, NeurIPS 2025).** <https://arxiv.org/abs/2411.05830>,
<https://arxiv.org/abs/2507.12367>

- *What it measures:* version-conditioned Python code generation, checked by
  executable tests.
- *Numbers:*
  - v1: GPT-4o pass@10 39.9%, or 43.7% with error feedback.
  - v2: enterprise models 48–51% on hidden tests (o1 51.2% is the best).
  - RAG adds up to ~10 points.
  - Self-debugging adds 10–20 points on hidden tests.
- *Why it matters:* even for versions *inside* the training window, models
  conflate versions. Familiarity with the *wrong* version is its own failure
  mode.
- *Limitations:*
  - Versions are intentionally within the training window. Release year "does
    not significantly impact the results", so it says nothing about cutoff
    lag.
  - The paper is internally inconsistent about which model is best with RAG.

**Twist, Harman, Syme, Noppen, Yannakoudakis, Nauck, Zhang. *A Study of LLMs'
Preferences for Libraries and Programming Languages.* ACL Findings 2026 (arXiv
2503.17181).** <https://arxiv.org/abs/2503.17181>

- *What it measures:* which library and language 8 LLMs choose.
- *Numbers:*
  - Popular libraries are used unnecessarily in up to 45% of cases.
  - Python is chosen for 58% of high-performance tasks where it isn't optimal;
    Rust is never chosen.
- *Why it matters:* their conclusion, "LLMs prioritise familiarity and
  popularity over suitability", is the session's worry in one line.
- *Limitations:* it measures library and language choice, not API design.

**Liu, Pandit, Ye, Choi, Durrett. *CodeUpdateArena: Benchmarking Knowledge
Editing on API Updates.* arXiv 2407.06249, 2024.**
<https://arxiv.org/abs/2407.06249>

- *What it measures:* knowledge editing on 54 synthetic updates to functions
  in 7 Python packages, with 670 program-synthesis examples.
- *Finding:* prepending the update's documentation did *not* let DeepSeek or
  CodeLlama use the change, and knowledge-editing methods have "substantial
  room for improvement". The abstract gives no numbers.
- *Why it matters:* it shows synthetic API updates as an eval tool, and that
  smaller models can ignore docs that contradict their priors.

**Other evolution benchmarks (no headline numbers in the abstracts; not
deeply read):**

- VersiCode, arXiv 2406.07411: <https://arxiv.org/abs/2406.07411>
- LibEvolutionEval, arXiv 2412.04478: <https://arxiv.org/abs/2412.04478>.
  Found that retrieved version-specific docs help.
- CODESYNC, arXiv 2502.16645: <https://arxiv.org/abs/2502.16645>. 220 APIs;
  14 LLMs "struggle… even with" DPO, ORPO and SimPO updating.
- MUDAPIBench, arXiv 2609.25786, Sept 2026:
  <https://arxiv.org/abs/2609.25786>. Unlearning deprecated API knowledge;
  Gradient Difference gives the best trade-off; no numbers in the abstract.

**ExploraCoder, arXiv 2412.05366.** <https://arxiv.org/abs/2412.05366>

- Uses Torchdata APIs unseen by GPT-3.5 and GPT-4-0613. Planning plus chained
  API exploration beats retrieval by up to 11.99 points pass@10.
- Relevant because the exploration that agents do is exactly the "lookup,
  trial and error" token cost.

**Hsieh et al. *Tool Documentation Enables Zero-Shot Tool-Usage with Large
Language Models.* arXiv 2308.00675, 2023.** <https://arxiv.org/abs/2308.00675>

- Zero-shot prompting with documentation matches few-shot prompting, and beats
  demonstrations on a set of hundreds of tools.
- Early evidence that docs can substitute for familiarity.

**Cheng et al. *Dated Data: Tracing Knowledge Cutoffs in Large Language
Models.* arXiv 2403.12958, 2024.** <https://arxiv.org/abs/2403.12958>

- Effective knowledge cutoffs often differ from, and trail, reported ones.
- Causes: old content in new CommonCrawl dumps, and deduplication effects.
- Relevance to the lag: a feature's representation in training data lags its
  ship date by more than the cutoff alone suggests.

**Mozilla. *Introducing the MDN MCP server.* June 2026.**
<https://developer.mozilla.org/en-US/blog/introducing-mdn-mcp-server>

- AI tools "can surface outdated web platform information based on their
  training data and knowledge cutoff". Its example is not knowing that
  `@view-transition` exists or is Baseline.
- Informal test: Claude Code (Opus 4.7) on four features new in Firefox 151.
  - Without the MCP, browser support was right only for `:buffering`.
    - It wrongly claimed `shadowrootslotassignment` ships in Chrome 120 and
      Safari 18.3.
    - It said Web Serial is "not on the roadmap" for Firefox.
  - With the MCP, answers were correct and about twice as fast.
- *Limitations:* 4 questions and 1 model. These are knowledge questions, not
  code generation.

**Google Chrome. *Modern Web Guidance* (announced at Google I/O 2026; docs
page last updated 30 Jun 2026).**

- *Sources:*
  - Get-started page: <https://developer.chrome.com/docs/modern-web-guidance/get-started>
  - Repo: <https://github.com/GoogleChrome/modern-web-guidance-src>
  - I/O recap: <https://developer.chrome.com/blog/chrome-at-io26>
- *Primary source for the 37-point figure:* "On average, early results show a
  37 percentage point improvement in adherence to modern best practices."
- *Eval design described:*
  - Use-case evals run an automated QA harness built on Playwright, "multiple
    times per week with state-of-the-art models and coding agents".
  - One eval is "unguided, which is a control, using the default training
    data".
- *Pruning:* the README says they "run evals enabling us to prune
  lowest-common-denominator content that models already know". In other
  words, they already measure familiarity per feature.
- *Scope:* covers 232 features and 186 use cases. Integrates with Baseline
  targets.
- *Limitations:*
  - No models, tasks or per-feature numbers are published.
  - "Your results may vary."

**Mintlify traffic data (already in the deck).** The deck's `docs` slide
cites Mintlify: in August 2026, 10.8M `/llms.txt` fetches
and 2M+ MCP tool calls on Mintlify-hosted docs. That shows agents do fetch
docs at scale. I found no controlled measurement of what `llms.txt` itself
gains.

**Gao & Chen. *From Agent Behaviour to Agent-Friendly Documentation.* arXiv
2608.20195, Aug 2026.** <https://arxiv.org/abs/2608.20195>

- Covers 557 agent sessions (3,033 documentation interactions) and 33,097
  agentic PRs.
- API references are only 1.3% of agents' documentation interactions;
  instruction files and notes are 60.5%.
- Consultation is self-initiated in 70.2% of cases and failure-driven in 7.5%.
- *Why it matters:* agents rarely read API reference docs on their own. That
  is consistent with Vercel's finding that skills go uninvoked, and it means
  "the docs exist" does not mean "the agent is at parity".

**ADK Arena. arXiv 2606.05548, June 2026.** <https://arxiv.org/abs/2606.05548>

- *What it does:* "LLM-as-a-Developer". It holds the coding agent constant,
  varies the framework, and treats generation effort as "a quantitative proxy
  for API usability".
- *Numbers:*
  - 51 Python agent frameworks.
  - Cost varies 5.6× ($0.6–$3.4 per agent).
  - Real use of each framework stays at 28–40% whatever the information
    source: docs, source code, or nothing (33%).
- *Why it matters:* it is the closest existing *API-usability* benchmark for
  agents.
- *Limitations:* it does not control for familiarity. Popular frameworks
  benefit from parametric knowledge, which the ablation suggests substitutes
  for docs.

**Trivedi & Schmitt. *Does Code Cleanliness Affect Coding Agents? A Controlled
Minimal-Pair Study.* arXiv 2605.20049, May 2026.**
<https://arxiv.org/abs/2605.20049>

- Minimal-pair repos differ only in cleanliness. 33 tasks, 660 Claude Code
  trials.
- Pass rate is unchanged, but there are 7–8% fewer tokens and 34% fewer file
  revisits on clean code.
- *Why it matters:* it is a methodological template, and like Wu et al. it
  shows design quality appearing in tokens, not pass rate.

**Constraint Decay. arXiv 2605.06445, May 2026.**
<https://arxiv.org/abs/2605.06445>

- 8 backend frameworks with a fixed API contract.
- Mid-tier models do well in "minimal, explicit" frameworks (Flask) and worse
  in "convention-heavy" ones (FastAPI, Django).
- Suggestive for design principles (explicit vs. conventional), but
  familiarity is not controlled.

**Anthropic (Ken Aizawa). *Writing effective tools for agents — with agents.*
11 Sep 2025.** <https://www.anthropic.com/engineering/writing-tools-for-agents>

- Recommends eval-driven tool design: realistic tasks with verifiable
  outcomes, held-out test sets, and tracking tokens, tool calls, runtime and
  errors as well as accuracy.
- Prefix vs. suffix namespacing has "non-trivial effects" that vary by model.
- A concise tool response used 72 tokens vs. 206 for a detailed one.
- Relevant because the same metrics apply to evaluating Web API shapes, and
  the effects are model-specific.

**Anthropic model docs.**
<https://platform.claude.com/docs/en/about-claude/models/overview>

- The current Claude models (Opus 5.5, Sonnet 5.5, Haiku 5.5, Fable 5.1) list
  a June 2026 reliable knowledge cutoff.
- The model-cutoff lag is months. The data lag for a new feature (enough code
  that uses it) is what plausibly takes years. I found no direct measurement
  of that.

**Practitioner reports (anecdotal, not cited on the slide).**

- A freeCodeCamp guide to Modern Web Guidance says agents build JavaScript
  state systems for tooltips "as if it were 2019".
  <https://www.freecodecamp.org/news/how-to-stop-your-ai-coding-agent-from-writing-outdated-code-with-modern-web-guidance/>
- Vendor and blog posts list floats, fixed widths and `!important` as typical
  AI CSS habits.
- A Codex-CLI blog summarises an ICSE 2026 JAWs workshop study: `AGENTS.md`
  cut median output tokens from 2,925 to 2,440 over 124 paired tasks.
  <https://codex.danielvaughan.com/2026/08/07/agents-md-efficiency-impact-icse-2026-jaws-codex-cli-token-savings-runtime-reduction/>
  I did not reach the primary paper.

## Mitigations and how well they work

| Mitigation | Measured effect | Source |
|---|---|---|
| API docs in the prompt | +8.9 points after cutoff (32.5 → 41.4); +14.8 before (56.1 → 70.9) | RustEvo² Table 3 |
| RAG over docs | +13.5 points after cutoff (34.9 → 48.4) | RustEvo² Table 4 |
| RAG over docs | Up to ~10 points (GPT-4.1 48.5 → 58.5) | GitChameleon 2.0 |
| Doc retrieval for rare APIs | +9.4 points on low-frequency APIs (38.58 → 47.94), but up to −39 on high-frequency APIs; selective retrieval +8.2 overall | CloudAPIBench |
| Always-on docs index in `AGENTS.md` | 53% → 100% | Vercel |
| On-demand skill | 53% → 53% (default; not invoked in 56% of cases); 79% when instructed | Vercel |
| MCP docs server | 1/4 → 4/4 on browser-support questions; ~2× faster (informal) | MDN |
| Curated guidance skills | "37 percentage point improvement in adherence to modern best practices" (no methodology) | Chrome Modern Web Guidance |
| Prompt hint about deprecation | Fix rate 25.7–97.2% | Wang et al. (InsertPrompt) |
| Decoding-time API substitution | Fix rate 85.2–99.6% (needs model internals) | Wang et al. (ReplaceAPI) |
| Error feedback / self-debugging | +3.8 points pass@10 (GitChameleon v1); +10–20 points hidden (v2) | GitChameleon |
| Exploration (try the API in a sandbox) | +12 points over retrieval | ExploraCoder |
| Fine-tuning / knowledge editing / unlearning | "Struggle… even with" DPO/ORPO/SimPO (CODESYNC); "substantial room for improvement" (CodeUpdateArena); a trade-off between forgetting and utility (MUDAPIBench) | — |
| `llms.txt`, Context7 | Widely fetched (10.8M `llms.txt` fetches on Mintlify, Aug 2026). No controlled effectiveness numbers found. | Mintlify |

Takeaways:

- Docs help, and the best agent-setting result (Vercel) reaches parity.
- *How* docs are delivered dominates: always-present beats on-demand.
- Every mitigation also costs tokens (reading docs, exploring). So "parity of
  accuracy" can still mean "higher token cost for the new design". That is
  exactly the session's point.

## Candidate evaluation methods

**1. Renamed or synthetic APIs (equal, zero familiarity).**

- *Method:* implement both candidate designs as fresh APIs with invented names
  that don't collide with anything in training data. Give agents identical
  reference docs and the same tasks, and measure pass rate, tokens and turns.
  This follows Zan et al.'s MonkeyEval and CodeUpdateArena's synthetic
  updates.
- *Pros:*
  - Removes the familiarity term entirely.
  - Cheap to run, and repeatable on every model generation.
- *Cons:*
  - Also removes *legitimate* transfer. A design that is consistent with
    existing web conventions should benefit from that, and it is a real design
    virtue: the "consistency" principle.
  - Renaming can make the semantics opaque.
  - Results may not predict behaviour once the real API is in training data.
- *Mitigation of the cons:* use semantically plausible but novel names, and
  run a variant that keeps platform-consistent naming.

**2. Minimal pairs.**

- *Method:* build two versions of the same task or codebase that differ only
  in the API shape under test (e.g. options bag vs. positional arguments;
  promise vs. event; declarative attribute vs. imperative call). Run many
  trials and compare tokens and pass rate (Trivedi & Schmitt).
- *Pros:*
  - Isolates one design decision.
  - Statistically tractable.
  - Shows effects in tokens even when pass rate saturates.
- *Cons:*
  - Real designs differ in many ways at once.
  - Building faithful pairs is labour-intensive.
  - Still confounded by familiarity unless combined with method 1.

**3. Docs-in-context parity.**

- *Method:* give *both* designs complete docs in context, ideally always
  present as in Vercel's `AGENTS.md` index, not retrieved on demand. The goal
  is to approximate the "after training data catches up" state.
- *Pros:*
  - Easy, and close to how agents increasingly work (MDN MCP, Modern Web
    Guidance).
- *Cons:*
  - Doesn't fully equalise. RustEvo² still shows a 29-point gap with docs
    (70.9 vs. 41.4).
  - Docs can hurt the familiar arm (CloudAPIBench).
  - Doc quality becomes a confound: you are partly evaluating the docs.

**4. Tokens-to-correct vs. tokens-at-parity.**

- *Method:* decompose cost into:
  - (a) tokens for the final correct code: an intrinsic proxy, like Wu et
    al.'s "representation cost";
  - (b) tokens spent getting there: lookup, failed attempts, fixes.
- Report (a) as the design's long-run cost, and (b) as the current familiarity
  tax. Re-execute intermediate states to label the work, as Wu et al. do.
- *Pros:*
  - Directly operationalises the session's distinction.
  - (a) is measurable today.
- *Cons:*
  - (a) ignores reading cost and ease of verification.
  - (b) also contains genuine design-difficulty costs, such as confusing
    semantics, not just unfamiliarity.

**5. Unguided control vs. guided (Chrome's design).**

- *Method:* run the same use-case evals with and without guidance. The delta
  per feature estimates how much the model "already knows" each feature, and
  features that need no guidance get pruned.
- *Pros:*
  - Already running at Google, multiple times a week, with Playwright. It
    could be opened up and published per feature.
- *Cons:*
  - It measures the *familiarity gap*, not design quality.
  - No methodology has been published yet.

**6. Longitudinal re-measurement.**

- *Method:* freeze an eval suite and re-run it on each model generation. Track
  how fast a given feature's tokens and pass rate converge to the familiar
  baseline, as with a feature's Baseline date vs. agent adoption.
- *Pros:*
  - Measures the lag itself, which is the real unknown here.
  - Could inform how long to wait before judging a design.
- *Cons:*
  - Slow by definition, and models change in other ways too.
  - Needs a stable owner, e.g. the WebDX CG.

**7. LLM-as-a-developer cost as a usability proxy (ADK Arena).**

- *Method:* hold the agent constant, vary the API, and use generation
  cost/effort as a usability score.
- *Pros:* scalable, and it already exists.
- *Cons:* confounded by popularity unless combined with method 1 or 3.

**8. Human-parity cross-check.**

- *Method:* compare agent results with human API-usability studies of the
  same designs. If both prefer the same design under equal unfamiliarity, the
  signal is more trustworthy.
- *Pros:* connects to the existing DX literature.
- *Cons:* expensive, and humans also have familiarity bias.

## Methodology

- *How sources were found:*
  - Web search for the topics in the brief: version and evolution benchmarks,
    deprecated-API studies, low-frequency APIs, cutoff lag, web-feature
    adoption, mitigations, and API-design evals.
  - arXiv abstracts via the arXiv export API.
  - Full-text HTML or PDF reads for the per-model numbers.
- *Checks on the numbers:*
  - Tables were extracted from paper HTML by a fetch tool that summarises
    pages with a model.
  - I recomputed the RustEvo² averages from the per-model rows, and they
    match.
  - The Zan et al. numbers were read from the PDF text.
  - Spot-check the other tables against the PDFs before quoting them beyond
    the slide.
- *Other sources:* Vercel, MDN, Chrome and Anthropic were read from the
  primary pages. The Modern Web Guidance 37-point claim was first seen on a
  third-party blog, then confirmed on Chrome's get-started page.
- *Slide fit:* checked by rendering a scratch copy of the deck at 1280×720 in
  headless Chromium (Playwright).

## Caveats

- **Almost none of this is web-platform data.** The quantitative studies cover
  Python, Rust, AWS APIs, Next.js and OCaml. Extrapolating to Web APIs is
  reasonable but unproven.
- **Model vintage.** Most controlled studies use 2023–early-2025 models
  (Codex, GPT-3.5, GPT-4o, Claude 3.5/3.7). Only Wu et al. (Sonnet 4.6,
  GPT-5.5) and the MDN test (Opus 4.7) are recent. Frontier models may close
  the accuracy gap and leave mainly a token gap, which is what Wu et al. show.
- **RustEvo²'s before and after task sets differ in APIs**, so some of the gap
  may be task difficulty.
- **"Familiarity" is never measured directly.** Every study uses a proxy:
  release date vs. cutoff, call frequency, language, or renaming.
- **Vendor sources** (Vercel, Chrome) publish numbers without full
  methodology. Chrome's 37 points comes with no models, tasks or variance.
- **Wang et al.'s rates are conditional** on plausible completions.
- **Docs-in-context results depend on doc quality and delivery.** They can't
  be read as properties of the API.

## Open threads

- **Web-specific measurement.**
  - *What:* pick about 10 recently Baseline features, each with a
    long-standing older pattern: `:has()` vs. JS class toggling; CSS nesting;
    popover vs. custom JS; `<dialog>`; View Transitions; anchor positioning;
    `fetch` vs. XHR; Temporal vs. Date/moment; the Navigation API vs.
    History; `structuredClone`.
  - *How:* give current agents tasks where the modern feature is the better
    fit, with and without MDN MCP or Modern Web Guidance. Measure feature use
    rate, pass rate and tokens.
  - Could run before TPAC (28 Oct) in a scaled-down form with 2–3 features.
- **Renamed-API design comparison.** Take a real design debate, e.g. two
  candidate shapes for one proposal. Implement both as shims with invented
  names and run a minimal-pair eval at zero familiarity. A good demo for the
  "how do we separate the two?" question.
- **Ask Chrome to publish Modern Web Guidance's per-feature eval data.** The
  unguided-control deltas are a familiarity map of the web platform, and
  exactly the dataset this question needs.
- **Lag curve.** Correlate web-features Baseline dates with when the
  unguided control starts passing for each feature, across model generations.
  Is the lag one model generation or several years?
- **Primary sources not yet read:**
  - the ICSE 2026 JAWs `AGENTS.md` efficiency paper;
  - controlled evaluations of Context7 or `llms.txt`;
  - Adam Wathan's original "indigo" post (relevant to the homogenization
    slide, not this one);
  - the VersiCode, LibEvolutionEval and CODESYNC full results.
- **Recruit:** people at TPAC interested in running a shared WebDX-CG-style
  agent eval harness (Chrome Modern Web Guidance team, MDN, WebDX CG).

## Slide

Deck slide id `evaluation` in `web/index.html`, titled "Evals reward the
familiar". Numbers on the slide:

- Bar chart (RustEvo², Table 3, 5-model average pass@1):
  - APIs older than the model: 56.1%; + docs in prompt: 70.9%.
  - APIs newer than the model: 32.5%; + docs in prompt: 41.4%.
- Stat row:
  - **1.3–1.7×** tokens in OCaml vs. Python on the same tasks (Wu, Anderson &
    Guha 2026; range across 5 models, OCaml vs. Python).
  - **25–38%** of completions choose a deprecated API over its replacement
    (Wang et al., ICSE 2025; overall DUR range across 7 models).
  - **53% → 100%** pass rate on Next.js 16 APIs absent from training data,
    once docs are in context (Vercel, Jan 2026).
- Closing question (revealed on click): "So how do we evaluate a design that
  is better, but new?"

Everything else here (Zan et al., CloudAPIBench, GitChameleon, MDN, Modern Web
Guidance, ADK Arena, minimal pairs and so on) is in the slide's speaker notes
or only in this file.
