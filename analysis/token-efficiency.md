# Token efficiency of Web APIs

Research notes behind the `token-efficiency` slide. Last updated 27 Oct 2026.

## Question

From the session description: *What makes a Web API token-efficient, both
when writing code against it and when reading code that uses it?*

Short answer: ceremony makes an API expensive in tokens. That means setup
objects, callbacks, lifecycle boilerplate and glue code, not long
identifiers. Recent platform additions that pave a common pattern cut the
tokens for the same task by about 2–6×. But for an agent, unfamiliarity
costs more than either: lookups, failed attempts and fixes. So a new, terser
API can cost more in practice than an old, verbose one until models have
trained on it.

## Key findings

- **Newer platform APIs need ~2× fewer tokens for the same task (median),
  and up to ~6–7× fewer.** Across 9 old→new pairs I measured, the median
  ratio is 2.15× (o200k), 2.00× (cl100k) and 1.97× (Qwen2.5-Coder). The
  biggest gaps: `className` string ops → `classList.toggle()` 46 → 7 tokens
  (6.6×), and `IntersectionObserver` lazy-loading → `loading=lazy` 76 → 12
  (6.3×). Source: own measurement, [Data](#data).
- **Declarative beats imperative.** The largest saving came from moving a
  behaviour into an HTML attribute (`loading=lazy`). The second largest came
  from a method that bakes in a common pattern (`classList.toggle`).
- **CSS nesting saves characters, not tokens.** 48 → 50 tokens with a
  `.card` selector, and 53 → 51 with `.product-card`, while characters drop
  150 → 138 and 190 → 146. A short, repeated selector is cheap, and nesting
  adds braces and indentation. Source: own measurement.
- **The platform's component model is the most ceremonious option.** The
  same click-counter is 123 tokens as a vanilla custom element, 88 in Lit,
  61 in React and 29 in Svelte 5 (o200k). Source: own measurement.
- **Libraries are still terser than the platform.** jQuery `addClass` is 8
  tokens vs 18 for `querySelectorAll().forEach(classList.add)`. A delegated
  click handler is 24 vs 32. Source: own measurement.
- **The cheapest code can be the unsafe code.** Appending a link with
  `innerHTML +=` is 16 tokens vs 24 for `createElement` + `append`. The
  cheaper version is XSS-prone, so token efficiency and robustness can pull
  in opposite directions. Source: own measurement.
- **Long names are cheap if they're familiar.** GPT-4's tokenizer (cl100k)
  encodes `.getElementsByClassName` (23 chars), `.getElementById` and
  `.addEventListener` as **1 token each**. The 13-char attribute
  `popovertarget` is **4 tokens** in all three tokenizers
  (`pop|o|vert|arget`), and `.adoptedStyleSheets` is 5–6. Every identifier
  that cl100k encodes as a single `.member` token is an older, very common
  DOM/JS API. None of the newer ones are: Web Components, observers,
  `structuredClone`, `AbortSignal`, popover, view transitions. Source: own
  measurement.
- **Unfamiliarity costs more than syntax.** Wu, Anderson & Guha
  (arXiv:2607.22807) pooled three open models. Agents' final OCaml solutions
  were 1.4× the Python ones (median 272 vs 190 tokens), but total output was
  2.6× (6,706 vs 2,548). In their words, “The extra cost is not
  representation.” Error recovery was ~41% of Gemma's OCaml tokens vs ~13%
  for Python.
- **Writing costs more per token; reading costs more in total.** Output
  tokens cost 5× uncached input and 100× a cached read (Claude Sonnet 5.5:
  $2 / $0.10 / $10 per MTok). Even so, “input tokens, not output tokens,
  dominate the overall cost in agentic coding” (Bai et al.,
  arXiv:2604.22750). Boilerplate is paid once when written and again every
  turn it is read back into context.
- **Tool and API outputs: concise formats and meaningful names help.**
  Anthropic's tool-design guidance gives 72 tokens for a concise response vs
  206 for a detailed one (~⅓). It also found that replacing UUIDs with
  meaningful names improved precision.
- **Language-level evidence agrees on direction.** RosettaCode tasks show a
  2.6× token gap across 19 languages, with JavaScript the most verbose
  dynamic language (Alderson, Jan 2026). A grammar designed for AI cut
  tokens 10–13% with no loss of quality (Sun et al., ISSTA '24).

## Data

Raw data:
- [`../web/data/token-counts.csv`](../web/data/token-counts.csv): every snippet, all tokenizers.
- [`../web/data/identifier-tokens.csv`](../web/data/identifier-tokens.csv): identifier tokenization, including the token splits.
- Snippets and scripts: [`../tools/tokens/`](../tools/tokens/), see its [README](../tools/tokens/README.md).

### Older vs newer platform APIs (same task)

Tokens to write each snippet (older → newer, ratio). Characters are given for
comparison.

| Task | Older | Newer | o200k_base | cl100k_base | Qwen2.5-Coder | Chars |
|---|---|---|---|---|---|---|
| Toggle a class | `className` string ops | `classList.toggle()` | 46 → 7 (6.57×) | 43 → 6 (7.17×) | 43 → 6 (7.17×) | 172 → 28 |
| Lazy-load an image | `IntersectionObserver` + `data-src` | `loading=lazy` | 76 → 12 (6.33×) | 76 → 12 (6.33×) | 76 → 12 (6.33×) | 337 → 43 |
| Remove an element | `parentNode.removeChild()` | `remove()` | 7 → 3 (2.33×) | 5 → 3 (1.67×) | 5 → 3 (1.67×) | 30 → 12 |
| Group an array | `Array.reduce` | `Object.groupBy()` | 32 → 14 (2.29×) | 32 → 14 (2.29×) | 32 → 14 (2.29×) | 113 → 56 |
| Promise with external resolvers | `new Promise` + captured resolvers | `Promise.withResolvers()` | 28 → 13 (2.15×) | 28 → 14 (2.00×) | 28 → 14 (2.00×) | 101 → 61 |
| Fetch with timeout | `AbortController` + `setTimeout` | `AbortSignal.timeout()` | 38 → 18 (2.11×) | 37 → 18 (2.06×) | 39 → 20 (1.95×) | 181 → 68 |
| Fetch JSON | `XMLHttpRequest` | `fetch` + `await` (try/catch) | 76 → 40 (1.90×) | 73 → 39 (1.87×) | 77 → 39 (1.97×) | 275 → 138 |
| Deep clone | `JSON.parse(JSON.stringify())` | `structuredClone()` | 9 → 7 (1.29×) | 9 → 7 (1.29×) | 9 → 7 (1.29×) | 46 → 35 |
| Scoped CSS rules (`.card`) | Repeated selectors | CSS nesting | 48 → 50 (0.96×) | 48 → 50 (0.96×) | 48 → 50 (0.96×) | 150 → 138 |
| *Variant:* scoped CSS rules (`.product-card`) | Repeated selectors | CSS nesting | 53 → 51 (1.04×) | 53 → 51 (1.04×) | 53 → 51 (1.04×) | 190 → 146 |
| **Median of the 9 pairs** (excl. variant) | | | **2.15×** | **2.00×** | **1.97×** | |

### Component comparison

The task: a button showing “Clicked N times” that increments on click.
Imports are included.

| Variant | o200k_base | cl100k_base | Qwen2.5-Coder | Chars |
|---|---|---|---|---|
| Vanilla custom element (shadow DOM, constructor, `connectedCallback`, `render()`, `customElements.define`) | 123 | 118 | 118 | 524 |
| Lit (`LitElement`, `static properties`, `html` template) | 88 | 88 | 88 | 350 |
| React function component (`useState`, JSX) | 61 | 58 | 58 | 217 |
| Svelte 5 (`$state` rune) | 29 | 29 | 29 | 107 |

React and Svelte need a build step, and React has no style encapsulation, so
this is not like-for-like on features. It shows the ceremony gap between the
platform's component model and what developers (and agents) reach for.

**The Lit mistake.** My first Lit version initialized state with a standard
class field (`count = 0`). With standard (`[[Define]]`) class-field
semantics, that field shadows the reactive accessor Lit generates from
`static properties`, so updates silently stop re-rendering. The value has to
be initialized in the constructor instead, and the measured version does
this. This is a robustness trap rather than a token cost, and exactly the
kind of thing agents get wrong.

### Libraries and safety

| Task | Variant | o200k_base | cl100k_base | Qwen2.5-Coder | Chars |
|---|---|---|---|---|---|
| Add class to all matches | Platform: `document.querySelectorAll('.item').forEach(el => el.classList.add('active'))` | 18 | 14 | 14 | 77 |
| | jQuery: `$('.item').addClass('active')` | 8 | 7 | 7 | 30 |
| Delegated click handler | Platform: `addEventListener` + `event.target.closest()` | 32 | 30 | 30 | 144 |
| | jQuery: `$(document).on('click', '.delete', …)` | 24 | 24 | 24 | 86 |
| Append a link | DOM: `createElement` + `href`/`textContent` + `append` | 24 | 22 | 22 | 91 |
| | `list.innerHTML += \`<a href="${url}">${label}</a>\`` (XSS-prone) | 16 | 15 | 15 | 50 |

jQuery's set-based API (operate on all matches, no explicit loop) is still
1.3–2.3× terser than the platform. In the link example, the token-cheapest
version injects unescaped strings into HTML.

### Identifier tokenization

Token counts for each identifier bare, and as a member access (with a
leading `.`, the way it usually appears in code). The split shown is o200k's
member form.

| Identifier | Chars | o200k bare | cl100k bare | Qwen bare | o200k `.member` | cl100k `.member` | Qwen `.member` | o200k split |
|---|---|---|---|---|---|---|---|---|
| `document` | 8 | 1 | 1 | 1 | 1 | 1 | 1 | `.document` |
| `fetch` | 5 | 1 | 1 | 1 | 1 | 1 | 1 | `.fetch` |
| `querySelector` | 13 | 2 | 1 | 1 | 2 | 1 | 1 | `.query\|Selector` |
| `querySelectorAll` | 16 | 3 | 2 | 2 | 3 | 1 | 1 | `.query\|Selector\|All` |
| `getElementById` | 14 | 4 | 2 | 2 | 4 | 1 | 1 | `.get\|Element\|By\|Id` |
| `getElementsByClassName` | 22 | 5 | 3 | 3 | 5 | 1 | 1 | `.get\|Elements\|By\|Class\|Name` |
| `addEventListener` | 16 | 3 | 1 | 1 | 3 | 1 | 1 | `.add\|Event\|Listener` |
| `removeEventListener` | 19 | 3 | 2 | 2 | 3 | 1 | 1 | `.remove\|Event\|Listener` |
| `preventDefault` | 14 | 2 | 2 | 2 | 2 | 1 | 1 | `.prevent\|Default` |
| `stopPropagation` | 15 | 2 | 2 | 2 | 2 | 1 | 1 | `.stop\|Propagation` |
| `classList` | 9 | 2 | 1 | 1 | 2 | 1 | 1 | `.class\|List` |
| `textContent` | 11 | 2 | 1 | 1 | 2 | 1 | 1 | `.text\|Content` |
| `innerHTML` | 9 | 2 | 1 | 1 | 2 | 1 | 1 | `.inner\|HTML` |
| `appendChild` | 11 | 2 | 1 | 1 | 2 | 1 | 1 | `.append\|Child` |
| `createElement` | 13 | 2 | 1 | 1 | 2 | 1 | 1 | `.create\|Element` |
| `setAttribute` | 12 | 2 | 1 | 1 | 2 | 1 | 1 | `.set\|Attribute` |
| `requestAnimationFrame` | 21 | 3 | 2 | 2 | 3 | 2 | 2 | `.request\|Animation\|Frame` |
| `setTimeout` | 10 | 2 | 1 | 1 | 2 | 1 | 1 | `.set\|Timeout` |
| `XMLHttpRequest` | 14 | 3 | 2 | 2 | 3 | 2 | 2 | `.XML\|Http\|Request` |
| `localStorage` | 12 | 2 | 1 | 1 | 2 | 1 | 1 | `.local\|Storage` |
| `getBoundingClientRect` | 21 | 4 | 2 | 2 | 4 | 1 | 1 | `.get\|Bounding\|Client\|Rect` |
| `customElements` | 14 | 2 | 2 | 2 | 2 | 2 | 2 | `.custom\|Elements` |
| `attachShadow` | 12 | 2 | 2 | 2 | 2 | 2 | 2 | `.attach\|Shadow` |
| `shadowRoot` | 10 | 2 | 2 | 2 | 2 | 2 | 2 | `.shadow\|Root` |
| `connectedCallback` | 17 | 2 | 2 | 2 | 2 | 2 | 2 | `.connected\|Callback` |
| `attributeChangedCallback` | 24 | 3 | 3 | 3 | 3 | 3 | 3 | `.attribute\|Changed\|Callback` |
| `observedAttributes` | 18 | 3 | 3 | 3 | 3 | 3 | 3 | `.ob\|served\|Attributes` |
| `adoptedStyleSheets` | 18 | 5 | 5 | 5 | 5 | 6 | 6 | `.ad\|opt\|ed\|Style\|Sheets` |
| `CSSStyleSheet` | 13 | 3 | 2 | 2 | 3 | 2 | 2 | `.CSS\|Style\|Sheet` |
| `replaceSync` | 11 | 2 | 2 | 2 | 2 | 2 | 2 | `.replace\|Sync` |
| `ElementInternals` | 16 | 3 | 3 | 3 | 3 | 3 | 3 | `.Element\|Intern\|als` |
| `attachInternals` | 15 | 3 | 3 | 3 | 3 | 3 | 3 | `.attach\|Intern\|als` |
| `setFormValue` | 12 | 3 | 3 | 3 | 3 | 3 | 3 | `.set\|Form\|Value` |
| `formAssociated` | 14 | 2 | 2 | 2 | 2 | 2 | 2 | `.form\|Associated` |
| `IntersectionObserver` | 20 | 2 | 2 | 2 | 3 | 3 | 3 | `.Inter\|section\|Observer` |
| `ResizeObserver` | 14 | 2 | 2 | 2 | 2 | 2 | 2 | `.Resize\|Observer` |
| `MutationObserver` | 16 | 2 | 2 | 2 | 3 | 3 | 3 | `.M\|utation\|Observer` |
| `PerformanceObserver` | 19 | 2 | 2 | 2 | 3 | 3 | 3 | `.Per\|formance\|Observer` |
| `structuredClone` | 15 | 2 | 2 | 2 | 3 | 3 | 3 | `.\|structured\|Clone` |
| `AbortSignal` | 11 | 2 | 2 | 2 | 3 | 3 | 3 | `.Ab\|ort\|Signal` |
| `withResolvers` | 13 | 2 | 3 | 3 | 2 | 3 | 3 | `.with\|Resolvers` |
| `groupBy` | 7 | 2 | 1 | 1 | 2 | 2 | 2 | `.group\|By` |
| `toggleAttribute` | 15 | 2 | 2 | 2 | 2 | 2 | 2 | `.toggle\|Attribute` |
| `replaceChildren` | 15 | 2 | 2 | 2 | 2 | 2 | 2 | `.replace\|Children` |
| `showModal` | 9 | 2 | 2 | 2 | 2 | 2 | 2 | `.show\|Modal` |
| `showPopover` | 11 | 2 | 2 | 2 | 2 | 2 | 2 | `.show\|Popover` |
| `popovertarget` | 13 | 4 | 4 | 4 | 4 | 4 | 4 | `.pop\|o\|vert\|arget` |
| `scrollIntoView` | 14 | 3 | 3 | 3 | 3 | 3 | 3 | `.scroll\|Into\|View` |
| `startViewTransition` | 19 | 3 | 3 | 3 | 3 | 3 | 3 | `.start\|View\|Transition` |
| `CSSNumericValue` | 15 | 3 | 3 | 3 | 3 | 3 | 3 | `.CSS\|Numeric\|Value` |
| `computedStyleMap` | 16 | 3 | 3 | 3 | 4 | 4 | 4 | `.com\|puted\|Style\|Map` |

In short code contexts:

| Code | o200k | cl100k | Qwen | o200k split | cl100k split |
|---|---|---|---|---|---|
| `el.addEventListener(` | 5 | 3 | 3 | `el\|.add\|Event\|Listener\|(` | `el\|.addEventListener\|(` |
| `document.getElementById(` | 6 | 3 | 3 | `document\|.get\|Element\|By\|Id\|(` | `document\|.getElementById\|(` |
| `document.getElementsByClassName(` | 7 | 3 | 3 | `document\|.get\|Elements\|By\|Class\|Name\|(` | `document\|.getElementsByClassName\|(` |
| `<button popovertarget="menu">` | 8 | 8 | 8 | `<button\| pop\|o\|vert\|arget\|="\|menu\|">` | same |
| `this.shadowRoot.adoptedStyleSheets = [sheet];` | 12 | 13 | 13 | `this\|.shadow\|Root\|.ad\|opt\|ed\|Style\|Sheets\| =\| [\|sheet\|];` | `this\|.shadow\|Root\|.\|adopt\|ed\|Style\|She\|ets\| =\| [\|sheet\|];` |
| `el.remove()` | 3 | 3 | 3 | `el\|.remove\|()` | same |
| `el.classList.toggle('open')` | 7 | 6 | 6 | `el\|.class\|List\|.toggle\|('\|open\|')` | `el\|.classList\|.toggle\|('\|open\|')` |

Observations:
- **cl100k memorized the classic DOM.** In member form, 19 identifiers are a
  single cl100k token. All are long-established, very common APIs: `document`,
  `fetch`, `querySelector(All)`, `getElementById`, `getElementsByClassName`,
  `add/removeEventListener`, `preventDefault`, `stopPropagation`, `classList`,
  `textContent`, `innerHTML`, `appendChild`, `createElement`, `setAttribute`,
  `setTimeout`, `localStorage`, `getBoundingClientRect`. No Web Components,
  observer, `structuredClone`, `AbortSignal`, popover or view-transition
  identifier is.
- **o200k splits at camelCase boundaries** (≈1 token per word), regardless of
  familiarity. Why its vocabulary lacks whole DOM identifiers is not
  something I investigated.
- **Lowercase concatenations fragment badly.** `popovertarget` is
  `pop|o|vert|arget` (4 tokens) in all three tokenizers. A camelCase or
  hyphenated spelling would split on word boundaries instead. HTML attribute
  naming conventions (all-lowercase run-together words) are the least
  tokenizer-friendly.
- **Identifiers are a small share of the total.** In the `fetch` snippets,
  for example, most tokens are punctuation, keywords and glue. Saving a token
  on a name matters far less than removing a callback or a setup object.

## Evidence from the literature

1. **Zixuan Wu, Carolyn Jane Anderson, Arjun Guha. “The Best Programming
   Language for Tokenmaxxing: An Investigation of Coding Agent Behavior
   Across Programming Languages.”** arXiv:2607.22807, July 2026 (rev. 21 Oct
   2026), LMPL 2026 workshop at SPLASH/ISSTA.
   <https://arxiv.org/abs/2607.22807>
   - *Measured:* agents solving the same problems in Python, Java, Rust and
     OCaml with five models (Gemma, Qwen, GLM, GPT-5.5, Sonnet). The main
     metric is output tokens, because prefix caching makes input cheap and
     generation time dominates.
   - *Numbers:*
     - Controlled output-token ratios vs Python (Tables 2/5): OCaml 1.44×
       (Gemma), 1.69× (Qwen), 1.54× (GLM), 1.30× (GPT-5.5), 1.28× (Sonnet).
       Java and Rust range 0.85–1.57×.
     - Table 19 (Gemma/Qwen/GLM pooled): median total output Python 2,548 vs
       OCaml 6,706 (2.6×); median final solution 190 vs 272 (1.4×). Quote:
       “The extra cost is not representation.”
     - Error recovery (fix bug, debug failure, infra confusion, revert) is
       ~41% of Gemma's OCaml tokens vs ~13% for Python (Table 12). For Gemma
       on OCaml, 92% of failed snapshots were compile errors.
     - Gemma's ever-solved rate: Python 84%, OCaml 62%.
     - Median input tokens per trajectory also balloon. Gemma: Python 9,558
       vs OCaml 84,781.
   - *Why it matters:* this is the cleanest evidence that the cost of using a
     less familiar target comes mostly from trial and error, not from the
     length of the code. It backs the session's “Evaluation” point:
     measurements today favour the familiar. Caveat: it compares languages,
     not Web APIs, and frontier models show smaller gaps.

2. **Longju Bai, Zhemin Huang, Xingyao Wang, Jiao Sun, Rada Mihalcea, Erik
   Brynjolfsson, Alex Pentland, Jiaxin Pei. “How Do AI Agents Spend Your
   Money? Analyzing and Predicting Token Consumption in Agentic Coding
   Tasks.”** arXiv:2604.22750, Apr 2026 (v3 Oct 2026).
   <https://arxiv.org/abs/2604.22750>
   - *Measured:* token use on SWE-bench Verified (500 instances) with 8
     frontier models, 4 runs each, using OpenHands.
   - *Numbers:*
     - “Input tokens, not output tokens, dominate the overall cost in
       agentic coding.” Cache-read input is “the largest category by a wide
       margin”.
     - Agentic tasks use ~1000× more tokens than code reasoning or code chat
       (abstract). The body gives ~3500× vs single-round reasoning and ~1200×
       vs multi-round chat.
     - Runs on the same task vary by up to 30×. Kimi-K2 and Claude Sonnet
       4.5 use 1.5M+ more tokens than GPT-5 on average.
     - Output tokens are priced ~80× cache reads (GPT-5).
     - Fix and Explore phases are about two-thirds of rounds (33.5% / 30.4%).
     - Cost spikes come from actions that bring new content into context:
       viewing files, running tests.
   - *Why it matters:* reading cost (context re-sent every turn) dominates
     total spend, so verbose code costs more over its lifetime in context
     than when written. The paper gives no per-file or per-API breakdown.

3. **Anthropic pricing page.**
   <https://platform.claude.com/docs/en/about-claude/pricing> (checked 27 Oct
   2026).
   - Claude Sonnet 5.5: $2/MTok input, $0.10 cache hits, $10 output.
     Claude Opus 5.5: $4 / $0.20 / $20.
   - So an output token costs 5× uncached input and 100× a cached read.
     Older models have the same 5× output/input ratio but 50× vs cache reads
     (e.g. Sonnet 4.5: $3 / $0.30 / $15).
   - *Why it matters:* this is the write vs read asymmetry. Output is also
     generated serially, so it costs latency as well as money.

4. **Ken Aizawa et al. (Anthropic). “Writing effective tools for AI agents —
   with agents.”** Anthropic Engineering, 11 Sep 2025.
   <https://www.anthropic.com/engineering/writing-tools-for-agents>
   - *Numbers:* a Slack tool example uses 206 tokens for a detailed response
     vs 72 for a concise one (~⅓). Claude Code caps tool responses at 25,000
     tokens by default.
   - *Other findings:* resolving arbitrary alphanumeric UUIDs to
     semantically meaningful names improved retrieval precision (fewer
     hallucinations). Namespacing tools under common prefixes helps, and
     prefix vs suffix naming “had non-trivial effects” on evals.
   - *Why it matters:* this is guidance for agent-facing APIs (tools), and
     it maps onto Web API outputs (error messages, serialized objects): be
     concise by default, and use meaningful names over opaque IDs.

5. **Martin Alderson. “Which programming languages are most
   token-efficient?”** 8 Jan 2026.
   <https://martinalderson.com/posts/which-programming-languages-are-most-token-efficient/>
   - *Measured:* RosettaCode tasks solved in all of 19 popular languages,
     using the GPT-4 tokenizer (Xenova/gpt-4). The author calls it informal.
   - *Numbers:* a 2.6× gap between C (least efficient) and Clojure (most;
     109 tokens average). JavaScript is the most verbose dynamic language.
     Haskell and F# are close to the best, thanks to type inference. APL's
     terseness didn't help because its glyphs tokenize into several tokens
     each; J (ASCII) averaged 70.
   - *Why it matters:* it is the same lesson as `popovertarget`. Brevity in
     characters is not brevity in tokens, and what counts is what the
     tokenizer has seen.

6. **Zhensu Sun, Xiaoning Du, Zhou Yang, Li Li, David Lo. “AI Coders Are
   Among Us: Rethinking Programming Language Grammar Towards Efficient Code
   Generation.”** ISSTA '24. arXiv:2404.16333.
   <https://arxiv.org/abs/2404.16333>
   - *Measured:* SimPy, a Python-derived grammar designed for AI, vs Python.
   - *Numbers:* 13.5% fewer tokens with CodeLlama and 10.4% with GPT-4, with
     equal or better task performance.
   - *Why it matters:* grammar and API surface redesign for models gives
     real but modest savings (~10%). That is small next to the 2–6× from
     removing ceremony, and next to the familiarity effect.

**Leads seen only in search summaries (not verified, not used on the slide):**
- “Agent-ready” site designs reporting 19–40% fewer prompt tokens (arXiv:2607.12056).
- A WebMCP preprint reporting a 65% mean token reduction (arXiv:2508.09171).
- A HackerNoon post claiming TypeScript costs ~31% more tokens than JavaScript.
- A Towards AI post finding more token variance between projects than between Go, Python and TypeScript.
- A DEV Community write-up noting that UUIDs tokenize worse than ULIDs.

**Not found:** published writing by Lea Verou specifically on API design for
agents or token efficiency (searched Oct 2026). Her 2026 blog posts are on
import maps and web dependencies.

## Methodology

- **Snippets.** I hand-wrote one snippet per variant (Claude, 27 Oct 2026),
  stored in [`../tools/tokens/snippets/`](../tools/tokens/snippets/). Style
  rules:
  - 2-space indent, single quotes in JS, semicolons, no comments.
  - Short realistic names (`el`, `res`, `items`).
  - The same placeholder functions on both sides of a pair (`render`,
    `showError`, `removeItem`).
  - Each pair does the same job, with equivalent error handling: XHR handles
    HTTP and network errors via `onload`/`onerror`, and fetch handles both
    via try/catch. The lazy-loading “old” version includes the
    `<img data-src>` markup plus the observer script, and the “new” one is
    just the `<img loading="lazy">`.
- **Counting.** [`../tools/tokens/measure.py`](../tools/tokens/measure.py)
  strips each file's trailing newline and counts tokens with:
  - `o200k_base` (GPT-4o and later) and `cl100k_base` (GPT-4), via
    `tiktoken` 0.14.0.
  - The Qwen2.5-Coder-7B-Instruct tokenizer (`tokenizer.json` at Hugging Face
    revision `c03e6d358207e414f1eca0bb1891e29f1db0e242`), via `tokenizers`
    0.23.3, with no special tokens.
  - Python 3.13.
  - Output: [`../web/data/token-counts.csv`](../web/data/token-counts.csv).
- **Identifiers.**
  [`../tools/tokens/identifiers.py`](../tools/tokens/identifiers.py)
  tokenizes each identifier bare, with a leading `.`, and in a few short code
  contexts. Output:
  [`../web/data/identifier-tokens.csv`](../web/data/identifier-tokens.csv).
- **Ratios and medians.** A ratio is older ÷ newer. The median is over the 9
  platform pairs, excluding the `.product-card` CSS variant.
- **Slide fit.** I checked the slide by rendering it into a scratch copy of
  the deck with headless Chromium (Playwright).

## Caveats

- **Snippets.** One author, one style. Formatting choices (indentation,
  line breaks, quote style) move counts by roughly ±10%. Other reasonable
  “equivalent” snippets would give different numbers, though I'd expect the
  same direction and rough size.
- **Claude's tokenizer is not public**, so the counts above are for OpenAI's
  tokenizers and Qwen's. Qwen2.5's vocabulary builds on cl100k, so it is not
  an independent check, and its counts match cl100k almost exactly. The
  three agreed within ~10% on every snippet.
- **Static code size ≠ agent cost.** These are tokens for a *correct* final
  snippet. Real agent cost includes lookups, failed attempts and fixes,
  which Wu et al. show can dominate.
- **Component comparison is not feature-equivalent.** React and Svelte need
  build tooling. React has no style encapsulation, while the custom element
  and Lit use shadow DOM. Svelte's count excludes the compiler.
- **Wu et al.** compares programming languages, not Web APIs. I use it as an
  analogy for an unfamiliar API. The 1.4×/2.6× figures pool three open
  models; frontier models show ~1.3× controlled ratios.
- **Bai et al.** gives a qualitative conclusion (input dominates cost) plus
  figures. I did not extract an exact input:output ratio from it.
- **Pricing changes.** The ratios are from Anthropic's page as of 27 Oct
  2026.
- **Identifier observations are correlational.** Single-token entries for
  classic DOM names are consistent with those names being frequent in the
  training text. I did not inspect tokenizer training data.

## Open threads

- **Measure Claude's tokenizer.** Run every snippet through the Anthropic
  API's `count_tokens` endpoint (`POST /v1/messages/count_tokens`). Subtract
  the count for an empty message to remove framing overhead. That would give
  Claude counts for the same snippets. It needs an API key, which wasn't
  available in this session.
- **Add more tokenizers.** Gemini (SentencePiece), Llama 3/4, DeepSeek-Coder,
  and newer GPT encodings, to test whether the “classic DOM = 1 token”
  effect holds outside the cl100k family.
- **Measure agent cost, not snippet size.** Give an agent the same task
  (e.g. “add lazy loading”, “make this a reusable component”, “add a popover
  menu”) with different APIs required or forbidden. Record total input and
  output tokens, turns, doc lookups and failure rate across several models
  and runs. That separates *representation* cost from *familiarity* cost,
  as Wu et al. did for languages.
- **Familiarity vs age.** Correlate token cost and success rate per API with
  a proxy for training-data frequency (GitHub code search hit counts, HTTP
  Archive usage, MDN page age). This would show how fast a new API “becomes
  cheap”, which is the delayed feedback loop the session asks about.
- **Reading cost in real repos.** Count tokens of platform boilerplate (e.g.
  custom-element lifecycle code, observer setup) in real codebases, and
  estimate how often agents re-read those files in a session.
- **Naming experiments.** Test whether agents misspell or misremember
  lowercase-concatenated attributes (`popovertarget`, `formnovalidate`) more
  than camelCase or hyphenated ones. Count tokens and error rates.
- **Error messages and outputs.** Apply Anthropic's tool-design findings to
  Web API outputs. How many tokens do platform error messages cost, and how
  often do they tell an agent what to fix?
- **Robustness vs terseness.** Collect more cases like `innerHTML` (cheap but
  unsafe) and Lit's class-field trap (familiar-looking but broken), to feed
  the session's “harder to misuse” question.
- **Language-level comparison.** Get Alderson's full per-language table,
  including where JavaScript sits, and the TypeScript vs JavaScript overhead
  from a verified source.

## Slide

Used by the slide with id `token-efficiency` in `web/index.html` (“Ceremony
costs tokens. Long names don't.”). Numbers on the slide, all from this file:

- **Table (o200k_base):**
  - Toggle a class 46 → 7.
  - Lazy-load an image 76 → 12.
  - Fetch JSON 76 → 40.
  - Counter component: custom element 123 vs React 61 / Svelte 29.
  - Scoped CSS rules 48 → 50.
- **Stat “1 vs 4”:** `.getElementsByClassName` (1 token in cl100k) vs
  `popovertarget` (4 tokens).
- **Stat “1.4× vs 2.6×”:** Wu, Anderson & Guha, OCaml vs Python, final code
  vs total agent output.
- **Stat “5×”:** output vs input token price (Claude Sonnet 5.5), with Bai et
  al.'s finding that input dominates agent cost.

The slide's speaker notes contain the full sources, all 9 pair results, the
library, `innerHTML` and Lit observations, and the Anthropic tool-design
numbers, consistent with this file.

## Source audit (2026-10-27)

- The "1 vs 4 tokens" stat (`.getElementsByClassName` vs `popovertarget`) holds in cl100k_base and Qwen2.5-Coder. It does not hold in o200k_base, which gives 5 vs 4 (`web/data/identifier-tokens.csv`). The slide now labels the stat "(cl100k)".
- "1.4× vs 2.6×" (Wu, Anderson & Guha): the paper states 2.6×, the ratio of median total output (6,706 vs 2,548 tokens). The 1.4× is derived from Appendix J median representation costs (272 vs 190). Both pool only Gemma, Qwen and GLM. The 1.3–1.7× on the evaluation slide is the paper's difficulty-controlled range across all 5 models.
