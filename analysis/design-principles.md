# Which design principles hold for agents

Research record for the TAG-principles slide (`#design-principles`) of the TPAC 2026 breakout session
“Agents are redefining DX. [How] should web standards adapt?” (28 Oct 2026). Research done 27 Oct 2026.

## Question

The session asks two linked questions (see [README](../README.md)):

- Which existing web platform design principles still hold for agents, and which actively hinder them?
- Where do agent ergonomics and human DX conflict, and how do we weigh them?

This file audits the W3C TAG
[Web Platform Design Principles](https://www.w3.org/TR/design-principles/) (Group Note, 14 Sep 2026),
the [HTML Design Principles](https://www.w3.org/TR/html-design-principles/) (W3C Working Draft,
26 Nov 2007) and the [Extensible Web Manifesto](https://github.com/extensibleweb/manifesto) (2013).
For each principle it asks whether the principle helps or hurts an LLM coding agent that writes or
reads web code, and what evidence supports the answer.

## Key findings

1. **The design principles don't address agents.** The 14 Sep 2026 Note has 103 numbered sections.
   It never mentions AI, LLMs, language models or machine learning. All 30 uses of “agent” mean
   *user agent*. Only one principle names its audience:
   [§2.7 “Design textual formats for humans”](https://www.w3.org/TR/design-principles/#text-formats).
   No issue in the [w3ctag/design-principles tracker](https://github.com/w3ctag/design-principles/issues)
   discusses agents as API consumers.
2. **Most principles hold, and the naming and consistency principles matter even more for agents.**
   Anthropic's and OpenAI's own guidance for designing tools for models closely matches the TAG's
   naming advice. Anthropic: “the tools that are most ‘ergonomic’ for agents also end up being
   surprisingly intuitive to grasp as humans.” OpenAI: “Pass the intern test.” For identifiers,
   readability and token efficiency point the same way. Common words are single tokens, and
   abbreviations break into meaningless fragments.
3. **Silent error recovery is the clearest conflict.** HTML and CSS recover from authoring errors
   without telling anyone ([HTML DP §4.3](https://www.w3.org/TR/html-design-principles/#handle-errors);
   [CSS 2.1 §4.2](https://www.w3.org/TR/CSS2/syndata.html#parsing-errors)). That is right for end
   users, but it leaves an agent with nothing to correct against. Chrome's own framing: agents are
   “programming with a blindfold on”.
4. **Token efficiency and robustness can pull apart.** Dictionary arguments (§6.5) cost ~1.6× the
   tokens of positional ones in the TAG's own examples, but they remove a class of errors. Compact
   formats (§2.7, SVG paths) halve the tokens but are harder to check.
5. **Principles that depend on a feedback loop from usage are the most disrupted.** “Low-level
   primitives, libraries build the high level” (Extensible Web Manifesto, §2.2) and “pave the
   cowpaths” (HTML DP §2.4) assume that what authors do reflects what authors need. As more web code
   is written by agents, usage increasingly reflects model priors. Models favor the familiar
   (Twist et al.) and reuse deprecated APIs (Wang et al.). Their hallucinations repeat run after run
   (Spracklen et al.).
6. **The priority of constituencies has no slot for agents.** §1.1 ranks users > authors >
   implementers > spec writers > theoretical purity. If agents are “authors”, their needs outrank
   implementers'. If they are tools,
   [§2.15](https://www.w3.org/TR/design-principles/#third-party-tools) already says usability beats
   compatibility with third-party tools, because “web platform features last a lot longer than most
   third-party tools”. That is the same objection as the README's: agents are volatile and Web APIs
   are permanent.

## Principle-by-principle audit

Verdicts are from the agent's point of view: ✓ = holds or helps, ? = contested or mixed,
✗ = works against agents. The **Basis** column says whether the verdict rests on published evidence,
our own measurement, or reasoned opinion. ★ = on the slide.

| # | Principle | Source | For humans | For agents | Verdict | Basis |
|---|---|---|---|---|---|---|
| 1★ | Use common words; avoid abbreviations | [TAG §12.1](https://www.w3.org/TR/design-principles/#naming-common-words) | Readable on first sight | Plain names beat cryptic IDs; abbreviations break into meaningless tokens | ✓ | Evidence (Anthropic, Wang et al. 2023) + measurement |
| 2★ | Be consistent / name things consistently / casing rules | [TAG §2.4](https://www.w3.org/TR/design-principles/#consistency), [§12.5](https://www.w3.org/TR/design-principles/#naming-consistency), [casing rules](https://www.w3.org/TR/design-principles/#casing-rules) | Less to memorize | Agents guess names from patterns; every exception invites a wrong guess | ✓ | Indirect evidence (Jain et al.) + opinion |
| 3★ | Accept optional/primitive args through dictionaries | [TAG §6.5](https://www.w3.org/TR/design-principles/#prefer-dictionaries) | Self-documenting calls | No argument order to recall, at ~1.6× the tokens | ✓ (with a cost) | Measurement + opinion |
| 4★ | Design textual formats for humans: readability over compactness | [TAG §2.7](https://www.w3.org/TR/design-principles/#text-formats) | Editable by hand | Compact halves the tokens (SVG paths); readable avoids errors | ? | Measurement + opinion (no direct evidence) |
| 5★ | Prefer graceful error recovery to hard failure | [HTML DP §4.3](https://www.w3.org/TR/html-design-principles/#handle-errors); [CSS 2.1 §4.2](https://www.w3.org/TR/CSS2/syndata.html#parsing-errors) | Users don't see author errors | Silent failure leaves agents “programming with a blindfold on” | ✗ | Evidence (Chrome DevTools MCP) + opinion |
| 6★ | Low-level primitives first; libraries build the high level | [Extensible Web Manifesto](https://github.com/extensibleweb/manifesto); [TAG §2.2](https://www.w3.org/TR/design-principles/#high-level-low-level) | Libraries iterate faster than specs | Glue code is cheap but rewritten for every project; declarative features work in one shot, once models know them | ? | Evidence on familiarity bias (Twist et al.) + opinion |
| 7★ | Pave the cowpaths | [HTML DP §2.4](https://www.w3.org/TR/html-design-principles/#pave-the-cowpaths) | Adopt common practice | Today's cowpaths are model priors, even repeated hallucinations | ? | Evidence (Spracklen et al., Wang et al. 2024) + opinion |
| 8 | Put user needs first (priority of constituencies) | [TAG §1.1](https://www.w3.org/TR/design-principles/#priority-of-constituencies); [HTML DP §3.2](https://www.w3.org/TR/html-design-principles/#priority-of-constituencies) | Clear tie-breaker | No slot for agents: are they authors or tools? | ? | Opinion (used as the slide's discussion prompt) |
| 9 | Prioritize usability over compatibility with third-party tools | [TAG §2.15](https://www.w3.org/TR/design-principles/#third-party-tools) | Platform outlives tools | If agents are “tools”, this says don't design for them | ? | Opinion |
| 10 | Prefer simple solutions; make common cases easy | [TAG §2.1](https://www.w3.org/TR/design-principles/#simplicity) | Low learning cost | Less surface to get wrong; one-shot common cases | ✓ | Opinion |
| 11 | Ensure features are developer-friendly (meaningful errors) | [TAG §10.7](https://www.w3.org/TR/design-principles/#debuggability) | Pinpoints problems | Helps only if agents can see DevTools output | ✓ (needs a channel) | Evidence (Anthropic on error messages, Chrome DevTools MCP) + opinion |
| 12 | New features should be detectable | [TAG §2.6](https://www.w3.org/TR/design-principles/#feature-detect) | Robust code across browsers | Lets agents write robust code without knowing what has shipped | ✓ | Opinion |
| 13 | Enable polyfills | [TAG §10.1](https://www.w3.org/TR/design-principles/#polyfills) | Early adoption | A polyfill puts the new API's name and shape into code early, before training data catches up | ✓ | Opinion |
| 14 | Use overloading wisely | [TAG §6.8](https://www.w3.org/TR/design-principles/#overloading) | Discoverable, readable | Type-dependent behavior is easy for a model to conflate | ✓ | Opinion |
| 15 | Use strings for constants and enums | [TAG §6.13](https://www.w3.org/TR/design-principles/#string-constants) | Readable values | Self-describing; no magic numbers to recall | ✓ | Opinion (consistent with Anthropic's guidance on semantic identifiers) |
| 16 | Use names that describe a purpose | [TAG §12.4](https://www.w3.org/TR/design-principles/#naming-future-proofing) | Future-proof names | Purpose words match how the task is described in a prompt | ✓ | Opinion |
| 17 | Heuristics/“magic” must have overrides (proposed) | [w3ctag/design-principles#455](https://github.com/w3ctag/design-principles/issues/455) | Less typing; escape hatch | Defaults save tokens, but heuristics are invisible and can't be debugged | ? | Evidence (OpenAI on defaults) + opinion |
| 18 | Prioritize compatibility when changing or removing features | [TAG §1.8](https://www.w3.org/TR/design-principles/#removing-features) | Old content keeps working | Old training data stays correct; behavior changes hurt doubly | ✓ | Indirect evidence (Wang et al. 2024 on deprecations) + opinion |
| 19 | Degrade gracefully | [HTML DP §2.2](https://www.w3.org/TR/html-design-principles/#degrade-gracefully) | Works in old browsers | Helpful at run time; same silent-failure problem at authoring time | ? | Opinion (folded into row 5 on the slide) |
| 20 | Don't reinvent the wheel; evolution not revolution | [HTML DP §2.3](https://www.w3.org/TR/html-design-principles/#do-not-reinvent-the-wheel), [§2.5](https://www.w3.org/TR/html-design-principles/#evolution-not-revolution) | No new models to learn | Familiar shapes are what models know | ✓ | Indirect evidence (familiarity bias) + opinion |
| 21 | Don't expose GC; preserve run-to-completion; privacy/security principles | [TAG §5.3](https://www.w3.org/TR/design-principles/#js-gc), [§5.2](https://www.w3.org/TR/design-principles/#js-rtc), §1.2–1.10, §2.8–2.12 | Protect users and predictability | Indifferent to who writes the code | ✓ (unchanged) | Opinion |

### Reasoning per row

**1. Use common words (✓).** §12.1: “Value readability over brevity. Avoid abbreviations, except in
cases where an abbreviation is extremely common and easy to understand.” *Evidence:* Anthropic says
agents “grapple with natural language names, terms, or identifiers significantly more successfully
than they do with cryptic identifiers”. It also says resolving UUIDs to meaningful language
“significantly improves Claude's precision in retrieval tasks by reducing hallucinations”, and it
recommends `user_id` over `user`. Wang et al. (2023/2024) found that LLM-based code analysis “heavily
relies on well-defined names in code”, though they tested older models (CodeBERT, plus a GPT case
study). *Measurement:* common words are cheap tokens. `requestAnimationFrame` = request·Animation·Frame
(3), `structuredClone` = 2. `RTCDTMFSender` = RT·CD·TM·FS·ender (5 meaningless fragments).
*Opinion:* for identifiers, readability and token efficiency point the same way. An abbreviation saves
characters, not tokens.

**2. Be consistent (✓, and if anything more important for agents).** §2.4 already says to weigh
precedent by prevalence (“follow the more popular precedent”), which matches how models generalize.
*Evidence (indirect):* Jain et al. found GPT-4o makes only 38.58% valid calls to low-frequency APIs.
*Opinion:* for any API it has rarely seen, an agent rebuilds the name and shape from platform-wide
patterns, and consistency is what makes that guess right. Humans look things up; agents often don't.
Every historical exception (`XMLHttpRequest`, `HTMLHtmlElement`, `getElementById` vs `pointerId`) is a
plausible wrong guess. A side finding from our measurement: the casing rule says to always capitalize
repeated initialisms, and that produces poorer tokenization. `HTMLHRElement` = HTML·H·RE·lement, while
the “infamous” `XMLHttpRequest` = XML·Http·Request. This is a curiosity, not an argument to change the
rule.

**3. Dictionaries, not positional arguments (✓, at a cost).** *Measurement* on §6.5's own examples:
1.67× and 1.56× the tokens (table below). *Opinion:* still worth it. The keys describe themselves when
code is read. The “Boolean trap” is exactly where a model has to recall what each position means. A
few extra tokens are cheap next to a docs lookup or a failed attempt and retry (Wu et al. show
retries dominate costs). This is a clean case of *token efficiency* and *robustness* pulling apart.

**4. Readable over compact formats (?).** §2.7: “Favor readability over compactness… SVG path syntax
was designed to be compact… the cost to human readability has remained the same.” *Measurement:* SVG
path data takes half the tokens of an equivalent verbose form. *Opinion:* compact syntax is cheaper
to emit but harder to check. §2.7 also argues for lenient syntax (comments, trailing commas, a
contained blast radius for errors), which helps agents as much as humans. No direct evidence found
either way.

**5. Graceful error recovery (✗ for agents as authors).** HTML DP §4.3: “Prefer graceful error
recovery to hard failure, so that users are not exposed to authoring errors.” CSS 2.1: “User agents
must ignore a declaration with an unknown property.” *Evidence:* Chrome DevTools MCP launch post (see
Evidence). Wu et al. found that much of agents' extra cost in unfamiliar languages is error recovery.
Compile errors at least give a signal; a CSS typo gives none. *Opinion:* resilience for end users is
right and should stay. The conflict is that recovery is *silent at authoring time*. §10.7 already
requires meaningful developer-facing errors, but those live in DevTools, which agents reach only
through tooling (DevTools MCP). A possible way out: loud, machine-readable authoring diagnostics
(dropped declarations, ignored attributes, unknown elements) that change nothing users see.

**6. Low-level first, libraries on top (?).** The Manifesto says browsers should “provide new
low-level capabilities” so that vendors and library authors can “iterate on libraries that provide
developer-friendly, high-level APIs”. §2.2 says low-level APIs let “high level APIs … organically
emerge from usage patterns”, while high-level APIs give the UA room for accessibility and privacy.
*Evidence:* Twist et al. found LLMs prioritize “familiarity and popularity over suitability” and use
NumPy unnecessarily in up to 45% of cases. MDN says agents “can surface outdated web platform
information”. *Opinion:* the Manifesto assumes glue code is expensive for humans, so it gets written
once in a shared library. Agents make glue cheap, but they write it fresh for each project, with no
shared bug fixes, or they fall back on the most popular library. A high-level declarative feature
(popover, `<dialog>`, anchor positioning) can be produced in one shot and keeps accessibility in the
browser, but only once models know it, which takes years. Lea Verou's complexity-to-effort curve
(“In the economy of user effort, be a bargain”) also changes shape. Agents don't feel effort, but
they pay for usability cliffs in tokens and bugs.

**7. Pave the cowpaths (?).** HTML DP §2.4: “When a practice is already widespread among authors,
consider adopting it rather than forbidding it or inventing something new.” Precedent in §2.15:
`Array.prototype.contains()` became `includes()` because of PrototypeJS. *Evidence:* Spracklen et al.
found hallucinated packages are frequent and *repeatable*, with 43% repeated in all 10 runs. Wang et
al. (2024) found 25–38% deprecated API usage overall, and 70–90% when the surrounding code is
outdated. *Opinion:* paving cowpaths *helps* agents, because it makes what they already write correct.
But as more web code is agent-written, HTTP Archive and use counters measure model priors as much as
developer needs. Should the platform pave APIs that agents consistently hallucinate, or does that
reward staleness?

**8. Priority of constituencies (?).** §1.1: “User needs come before the needs of web page authors,
which come before the needs of user agent implementors, which come before the needs of
specification writers, which come before theoretical purity.” The agent's place is undefined. If the
agent is the author, its needs outrank implementers'. If it is a tool the author uses, §2.15 applies.
Who bears token cost is also open. It could be the author (paying for tokens), the user (waiting for
slower or buggier software), or neither. This is the slide's discussion prompt.

**9. Third-party tools (?).** §2.15: “Design new features with usability as the primary goal, and
compatibility with third-party tooling as a secondary goal… web platform features last a lot longer
than most third-party tools.” If agents count as tools, this is the TAG already arguing the README's
counterpoint (agents are volatile; Web APIs are permanent). The difference is that agents are now the
*majority* consumer, not a niche preprocessor.

**10. Prefer simple solutions (✓).** Simple, common-case-first APIs give a model fewer ways to go
wrong. The Sanitizer API example in §2.1, a shortcut for a complex but common need, is the kind of
one-shot feature agents benefit from most.

**11. Developer-friendly errors (✓, needs a channel).** §10.7: developer-oriented error messages
“must be meaningful” and “specific to that error case”. Anthropic: “prompt-engineer your error
responses to clearly communicate specific and actionable improvements.” The principle already aligns
with agents. The gap is delivery: console messages aren't in an agent's loop unless tools put them
there.

**12. Feature detection (✓).** Agents often don't know what has shipped where (training cutoff, MDN's
“outdated web platform information”). Feature detection lets them write code that is correct either
way. Kept off the slide because it's uncontroversial.

**13. Polyfills (✓).** Opinion: a polyfill gets the final API name and shape into real-world code
before browsers ship it, which shortens the wait for training data. Lea Verou's “In defense of
polyfills” (Jul 2026) names agents as one of the platform's consumers that benefit from a “shared
vocabulary”. Dropped for space.

**14. Overloading (✓).** §6.8 warns against methods whose behavior or later arguments change
depending on argument types. Opinion: that kind of overloading is easy for a model to conflate. No
evidence found. Dropped.

**15. Strings for enums (✓).** §6.13: “Code that uses this API therefore requires that readers are
familiar with the API to understand it” (of `XMLHttpRequest.readyState` integers). This matches
Anthropic's advice to avoid cryptic identifiers. Dropped as a duplicate of row 1.

**16. Purpose-describing names (✓).** §12.4: name things for what they do. Opinion: agents start from
a description of a task, so purpose words are what they search for. Dropped as a duplicate of row 1.

**17. Heuristics and “magic” (?).** Lea Verou's open proposal #455 asks that heuristics always come
with overrides. Martin Thomson's April 2025 comment there proposes avoiding heuristics in new
capabilities altogether, because sites depend on predictable behavior. For agents, good defaults are
good. OpenAI: “Don't make the model fill arguments you already know.” Unobservable heuristics are bad
because the model can't see why output differs from what it expected. Considered for the slide;
dropped because it's a proposal, not an adopted principle.

**18. Compatibility when changing features (✓).** The web never deprecates, which makes training data
age well for the web compared with Python libraries (Wang et al. 2024: deprecations are a major
source of wrong completions). A strength of the platform for agents. Mention it in discussion if the
“web is unversioned” angle comes up.

**19. Degrade gracefully (?).** Same tension as row 5. Graceful degradation at run time is good, but
it hides the fact that a feature isn't supported while the agent is authoring.

**20. Don't reinvent the wheel; evolution not revolution (✓).** Familiar models are what agents know
(Twist et al.). New paradigms pay the familiarity tax for years.

**21. GC, run-to-completion, privacy and security (✓, unchanged).** These protect users from pages
and keep behavior predictable, whoever writes the code. They are the bulk of the document, and the
reason the slide title says “most principles hold”.

## Human vs. agent DX conflicts

The sharpest examples, roughly in order of strength:

1. **Silent recovery vs. the need for loud failure.** Graceful error recovery keeps authoring errors
   away from users. It also keeps them away from the agent that made them. Resolution candidate:
   separate end-user behavior (lenient) from authoring diagnostics (loud and machine-readable).
2. **Token efficiency vs. robustness.** Dictionaries cost ~1.6× the tokens but remove argument-order
   errors. Compact formats halve the tokens but are harder to check. “Agent DX” isn't one number.
3. **Familiar vs. better.** Every new or redesigned API pays a familiarity tax. Models favor the
   popular option (Twist et al.), make poor calls to rare APIs (38.58% valid, Jain et al.), and reuse
   deprecated ones (Wang et al.). A design that is better for humans can measure as worse for agents
   for years.
4. **Usage signal pollution.** “Pave the cowpaths” and “let libraries iterate” assume that usage
   reflects needs. When agents write the code, usage partly reflects model priors and repeated
   hallucinations (Spracklen et al.).
5. **Low-level flexibility vs. one-shot declarative features.** Humans benefit from primitives plus
   shared libraries. Agents benefit from high-level declarative features, but only once they're in
   training data.
6. **Implicit defaults and “magic” vs. explicitness.** Defaults save agent tokens (OpenAI), but
   unobservable heuristics can't be debugged (#455).

Where they *don't* conflict: naming, consistency, strings for enums, simplicity. In practice,
designing for humans and designing for models give the same answers here (Anthropic, OpenAI's
“intern test”).

## Evidence

### Primary documents

- **W3C TAG, *Web Platform Design Principles*, W3C Group Note, 14 Sep 2026.**
  https://www.w3.org/TR/design-principles/. The anchors used are in the audit table. Quotes in this
  file are from the 14 Sep 2026 version. Text search: 0 occurrences of “AI” (as a word), “LLM”,
  “machine learning” or “language model”. All 30 occurrences of “agent(s)” are “user agent(s)”.
- **W3C, *HTML Design Principles*, W3C Working Draft, 26 Nov 2007.**
  https://www.w3.org/TR/html-design-principles/. Sections used: §2.2
  [degrade-gracefully](https://www.w3.org/TR/html-design-principles/#degrade-gracefully), §2.3
  [do-not-reinvent-the-wheel](https://www.w3.org/TR/html-design-principles/#do-not-reinvent-the-wheel),
  §2.4 [pave-the-cowpaths](https://www.w3.org/TR/html-design-principles/#pave-the-cowpaths), §2.5
  [evolution-not-revolution](https://www.w3.org/TR/html-design-principles/#evolution-not-revolution),
  §3.2 [priority-of-constituencies](https://www.w3.org/TR/html-design-principles/#priority-of-constituencies),
  §4.3 [handle-errors](https://www.w3.org/TR/html-design-principles/#handle-errors). This document
  never advanced beyond Working Draft.
- **The Extensible Web Manifesto, 2013.** https://github.com/extensibleweb/manifesto (the text is on
  the `gh-pages` branch). extensiblewebmanifesto.org now redirects to extensibleweb.org and then to
  extensiblewebsummit.org, so cite the GitHub copy. Its four principles: focus on new low-level
  capabilities; expose low-level capabilities that explain existing features; “Develop, describe and
  test new high-level features in JavaScript, and allow web developers to iterate on them before they
  become standardized”; prioritize efforts that follow these. Also: “Library authors can experiment
  with new APIs and create more cow-paths for the platform to pave.” And: “We want web developers to
  write more declarative code, not less.”
- **W3C, CSS 2.1 §4.2, Rules for handling parsing errors.**
  https://www.w3.org/TR/CSS2/syndata.html#parsing-errors. “Unknown properties. User agents must
  ignore a declaration with an unknown property.”

### Industry guidance on designing for models

- **Anthropic, “Writing effective tools for agents — with agents”, 11 Sep 2025.**
  https://www.anthropic.com/engineering/writing-tools-for-agents. Quotes:
  - “the tools that are most ‘ergonomic’ for agents also end up being surprisingly intuitive to grasp
    as humans.”
  - Agents “grapple with natural language names, terms, or identifiers significantly more
    successfully than they do with cryptic identifiers”.
  - Resolving UUIDs to meaningful language “significantly improves Claude's precision in retrieval
    tasks by reducing hallucinations”.
  - “input parameters should be unambiguously named: instead of a parameter named `user`, try a
    parameter named `user_id`.”
  - “prompt-engineer your error responses to clearly communicate specific and actionable
    improvements”.
  - “A common error we've observed is tools that merely wrap existing software functionality or API
    endpoints”. This is a relevant echo of the low-level vs. high-level debate.
  - Tools are “a contract between deterministic systems and non-deterministic agents”.
- **OpenAI, Function calling guide, “Best practices for defining functions”** (accessed 27 Oct 2026).
  https://developers.openai.com/api/docs/guides/function-calling. Quotes:
  - “Write clear and detailed function names, parameter descriptions, and instructions.”
  - “Pass the intern test. Can an intern/human correctly use the function given nothing but what you
    gave the model?”
  - “Make the functions predictable and intuitive.”
  - “Use enums and object structure to prevent invalid states.”
  - “Don't make the model fill arguments you already know.”
  - “Combine functions that are always called in sequence.”
  - “Aim for fewer than 20 functions available at the start of a turn.”
- **Mathias Bynens & Michael Hablich, “Chrome DevTools (MCP) for your AI agent”, Chrome for
  Developers blog, 23 Sep 2025.** https://developer.chrome.com/blog/chrome-devtools-mcp. Coding
  agents “are not able to see what the code they generate actually does when it runs in the browser.
  They're effectively programming with a blindfold on.”
- **MDN, “Introducing the MDN MCP server”, 15 Jun 2026.**
  https://developer.mozilla.org/en-US/blog/introducing-mdn-mcp-server. AI tools “can surface outdated
  web platform information”. This source is already cited on the deck's `#docs` slide.

### Research

- **Wang, Zhang, Cao, Luo, Luo, Liu. “How Does Naming Affect LLMs on Code Analysis Tasks?”**
  arXiv:2307.12488 (v1 Jul 2023, v5 Jul 2024), *Journal of Software Engineering and Applications*
  17(11), Nov 2024. https://arxiv.org/abs/2307.12488. Datasets with nonsense or misleading names;
  CodeBERT plus a GPT case study. “naming has a significant impact on the performance of code
  analysis tasks based on LLMs”, and LLM code representation “heavily relies on well-defined names in
  code”. The abstract gives no headline percentage.
- **Jain, Kwiatkowski, Ray, Ramanathan, Kumar. “On Mitigating Code LLM Hallucinations with API
  Documentation.”** arXiv:2407.09726, Jul 2024. https://arxiv.org/abs/2407.09726. “GPT-4o achieves
  only 38.58% valid low frequency API invocations.”
- **Twist, Zhang, Harman, Syme, Noppen, Yannakoudakis, Nauck. “A Study of LLMs' Preferences for
  Libraries and Programming Languages”** (v1 title: “LLMs Love Python…”). arXiv:2503.17181 (Mar 2025,
  v2 Jul 2025). https://arxiv.org/abs/2503.17181. Eight LLMs:
  - NumPy used unnecessarily in up to 45% of cases (v1 said 48%).
  - Python chosen in 58% of high-performance project-initialisation tasks; Rust never chosen.
  - LLMs prioritize “familiarity and popularity over suitability and task-specific optimality”.
- **Wang, Huang, Zhang, Feng, Zhang, Liu, Peng. “LLMs Meet Library Evolution: Evaluating Deprecated
  API Usage in LLM-based Code Completion.”** ICSE 2025, arXiv:2406.09834.
  https://arxiv.org/abs/2406.09834. 7 LLMs, 145 API mappings from 8 Python libraries, 28,125
  completion prompts. Results:
  - Deprecated usage rate 25–38% overall.
  - 70–90% when the prompt context uses outdated APIs; 9–18% when it is up to date.
  - Root causes: deprecated usage in training corpora, and no knowledge of deprecations at inference
    time.
- **Spracklen, Wijewickrama, Sakib, Maiti, Viswanath, Jadliwala. “We Have a Package for You! A
  Comprehensive Analysis of Package Hallucinations by Code Generating LLMs.”** USENIX Security 2025,
  arXiv:2406.10279. https://arxiv.org/abs/2406.10279. 576,000 code samples from 16 LLMs in 2
  languages. Results:
  - At least 5.2% hallucinated packages for commercial models, 21.7% for open-source models.
  - 205,474 unique hallucinated names.
  - §5.3: “43% of hallucinated packages were repeated in all 10 queries, while 39% did not repeat at
    all”; “58% of the time, a hallucinated package is repeated more than once in 10 iterations”.
- **Wu, Anderson, Guha. “The Best Programming Language for Tokenmaxxing: An Investigation of Coding
  Agent Behavior Across Programming Languages.”** arXiv:2607.22807 (v1 24 Jul 2026, v2 21 Oct 2026).
  https://arxiv.org/abs/2607.22807. Five models on Python, Java, Rust and OCaml, controlling for
  problem difficulty. Token-cost ratios vs. Python (mixed effects; * p < 0.05):

  | Model | Java | Rust | OCaml |
  |---|---|---|---|
  | Gemma | 0.85 (n.s.) | 1.07 (n.s.) | 1.44* |
  | Qwen | 1.21* | 1.20* | 1.69* |
  | GLM | 1.34* | 1.57* | 1.54* |
  | GPT-5.5 | 1.30* | 1.36* | 1.30* |
  | Sonnet | 1.18* | 1.16* | 1.28* |

  Other findings:
  - Agents produce “noncompiling solutions in unfamiliar languages” and prototype in Python.
  - The extra cost is mostly error recovery, not longer solutions.
  - “After deduplication, The Stack v2 has around 200GB of Java and of Python, but only 12GB of Rust
    and even less OCaml.”
  - Agents “can spend far more tokens on a lower-resource language than higher-resource languages.”
  - Relevance: in this study, familiarity matters more than syntactic terseness. Java is more verbose
    than Rust, yet costs about the same.
- **Lea Verou, “In the economy of user effort, be a bargain”, 29 Sep 2025.**
  https://lea.verou.me/blog/2025/user-effort/. Introduces the complexity-to-effort curve. “A usability
  cliff is when a small increase in use case complexity requires a large increase in user effort.”
  Doesn't mention AI.
- **Lea Verou, “In defense of polyfills”, 13 Jul 2026.** https://lea.verou.me/blog/2026/polyfills/.
  Mentions agents once: “uniting all consumers (developers, agents, tooling, etc) around a shared
  vocabulary.” No other Lea Verou post on AI and API design was found (index checked 27 Oct 2026).

### Our token measurements

`tiktoken` with OpenAI's public `o200k_base` (GPT-4o/5 family) and `cl100k_base` encodings. Claude's
tokenizer isn't public. Exact strings measured:

**Dictionaries vs. positional arguments (TAG §6.5's own examples).** Same counts in both encodings.

| String | Tokens |
|---|---|
| `new Event("example", { bubbles: true, cancelable: false })` | 15 |
| `new Event("example", true, false)` | 9 (ratio 1.67×) |
| `window.scrollBy({ left: 50, top: 0 })` | 14 |
| `window.scrollBy(50, 0)` | 9 (ratio 1.56×) |

**Compact vs. readable format (TAG §2.7's SVG example).** Same counts in both encodings. The verbose
form is hypothetical, for comparison only.

| String | Tokens |
|---|---|
| `M10 10 L20 20` | 8 |
| `moveTo(10, 10) lineTo(20, 20)` | 16 (ratio 0.5×) |

**Identifiers (o200k_base unless noted).**

| String | Tokens | Split |
|---|---|---|
| `requestAnimationFrame` | 3 | request·Animation·Frame |
| `structuredClone` | 2 | structured·Clone |
| `canplaythrough` | 3 | can·play·through |
| `getElementsByTagName` | 5 | get·Elements·By·Tag·Name |
| `getElementById` | 4 (cl100k: 2) | get·Element·By·Id |
| `RTCDTMFSender` | 5 | RT·CD·TM·FS·ender |
| `RTCDtmfSender` | 5 | RT·CD·tm·f·Sender |
| `HTMLHRElement` | 4 | HTML·H·RE·lement |
| `HtmlHrElement` | 3 (cl100k: 4) | Html·Hr·Element |
| `XMLHttpRequest` | 3 (cl100k: 2) | XML·Http·Request |
| `HTMLHtmlElement` | 3 | HTML·Html·Element |
| `innerHTML` | 2 (cl100k: 1) | inner·HTML |
| `no-referrer-when-downgrade` | 9 | no·-ref·errer·-·when·-d·ow·ng·rade |
| `document.querySelectorAll(".item")` | 7 | |
| `$$(".item")` | 4 | |

The `document.querySelectorAll` vs `$$` pair shows the human-typing kind of terseness: about half
the tokens, but much less self-describing. Not used on the slide.

## TAG and standards-community discussion

- **The Note itself.** The 14 Sep 2026 Note never mentions AI or LLMs (see Evidence). Its only
  audience-specific principle is §2.7 “Design textual formats *for humans*”.
- **w3ctag/design-principles issues.** Searched on 27 Oct 2026 through GitHub's web issue search for
  LLM, AI, agents, agentic, “language model”, copilot, “code generation”, coding agent and chatgpt.
  The GitHub search API was unavailable from this session. No issue discusses agents or LLMs as API
  consumers or authors. Hits, none of them on topic: #619, #578, #551, #526, #507, #455, #368, #338,
  #265, #38, #32, #131.
  - **[#551](https://github.com/w3ctag/design-principles/issues/551)** “New principle: Sourcing models
    and compute for inference” (Martin Thomson, 6 Feb 2025, open). About web APIs that *use* ML
    models (translation, speech recognition): local vs. cloud models, bandwidth and compute, consent
    prompts as possible dark patterns. Not about agents writing code.
  - **[#455](https://github.com/w3ctag/design-principles/issues/455)** “New principle: When
    introducing heuristics or ‘magic’, also include a way to override them” (Lea Verou, 27 Nov 2023,
    open). Counterexamples: CSS specificity can only be raised, and z-index “wars”. Martin Thomson
    (April 2025) proposes avoiding heuristics in new capabilities because sites depend on predictable
    behavior, and says unpredictable variation should be treated as a bug. This is the closest
    existing thread to agent needs (predictability, observability).
  - [#507](https://github.com/w3ctag/design-principles/issues/507) “name things for what they do, not
    how they do it” became §12.4. It doesn't mention agents.
- **The §2.15 angle.** “Prioritize usability over compatibility with third-party tools” uses the
  argument that “web platform features last a lot longer than most third-party tools”. The TAG
  already has a principle for a fast-moving class of consumer. The open question is whether agents
  are such a class (so don't design for them), or are now the main audience (so they belong in the
  priority of constituencies).
- **Practitioner “agent experience” (AX) writing** (WorkOS, Apideck, Speakeasy, agentpatterns.ai)
  mostly treats AX as an extension of DX rather than in conflict with it. The common points are
  machine-readable, actionable errors (e.g. Stripe's `doc_url`). These are vendor blogs and are not
  cited on the slide.

## Methodology

1. Downloaded the TAG Note (14 Sep 2026) and extracted every section anchor and the text of the
   relevant sections. Ran a text search for AI-related terms and classified every “agent” occurrence.
2. Read HTML Design Principles (2007), the Extensible Web Manifesto (GitHub copy) and CSS 2.1 §4.2.
3. Searched the w3ctag/design-principles issue tracker (see the previous section).
4. Web searches for model-facing API guidance (Anthropic, OpenAI) and research on naming,
   hallucination, deprecated APIs, library bias and token cost by language. All numbers above were
   checked against the arXiv abstract or HTML full text.
5. Token counts with `tiktoken` (o200k_base, cl100k_base) on the exact strings listed.
6. For each principle, reasoned about the effect on an agent that writes code (emitting tokens,
   recalling APIs) and one that reads code, separating cited evidence from opinion.
7. Built the slide and rendered it in headless Chromium inside a scratch copy of the deck, at
   1600×900 in light and dark mode, to confirm it fits on one slide.

## Caveats

- **The verdicts are opinions.** Rows marked “Opinion” have no direct evidence. Row 2's evidence is
  indirect: Jain et al. measure rarity, not consistency.
- **Tokenizers differ.** Measurements use OpenAI tokenizers. Claude's tokenizer isn't public, so
  exact counts will differ; the ratios are more robust. Identifier counts also differ between
  o200k and cl100k (see table).
- **The studies are mostly Python.** Twist, Wang (deprecations), Spracklen and Wu all test Python or
  general-purpose languages, not web code. No study measuring LLM use of modern web platform features
  (e.g. by Baseline status) was found.
- **Model behavior moves fast.** The studies date from 2023 to 2026. Wang et al. 2023 used CodeBERT.
- **HTML Design Principles is a 2007 Working Draft** that never advanced. It is still widely cited as
  the origin of “pave the cowpaths” and the priority of constituencies.
- **The slide over-samples contested principles.** Most of the Note (privacy, security, GC, events)
  is indifferent to who writes the code. “Most principles hold” refers to the whole document.
- **Issue search is keyword-based.** An agent-related discussion under other words (e.g. “tooling”,
  “code generation”) could have been missed. TAG design-review threads in w3ctag/design-reviews were
  not searched.

## Open threads

- **Propose an agent-consumer section to the TAG.** File an issue on w3ctag/design-principles asking
  whether agents belong in §1.1's priority of constituencies, and whether §2.15 applies to them.
  Candidate principles:
  - Make authoring errors observable (machine-readable diagnostics for dropped CSS declarations,
    unknown elements and attributes) without changing end-user behavior.
  - Prefer consistency over local ergonomics more strongly than §2.4 does today.
- **Experiments that would turn opinion rows into evidence:**
  - *Consistency (row 2):* give models synthetic web-style APIs with consistent vs. inconsistent
    naming (casing, verb patterns) and measure first-try correctness.
  - *Dictionaries (row 3):* compare first-try correctness and total tokens, including retries, for
    positional vs. dictionary signatures of unfamiliar functions. Does the 1.6× write cost pay for
    itself?
  - *Compact vs. readable (row 4):* SVG path generation and editing accuracy vs. a verbose
    equivalent. Also CSS shorthand vs. longhand.
  - *Silent failure (row 5):* run an agent on CSS/HTML tasks with and without a channel that reports
    dropped declarations (e.g. DevTools MCP console, or a strict validator). Measure iterations and
    final correctness.
  - *Low-level vs. high-level (row 6):* one-shot success with `popover`/`<dialog>` vs. hand-rolled
    modals, across models with different training cutoffs. This also measures the familiarity lag the
    README's Evaluation question asks about.
  - *Cowpaths (row 7):* collect web-platform APIs that models repeatedly hallucinate. Are they
    consistent? Do any match real proposals?
- **Measure modern-feature uptake.** Is there a Baseline-by-year analysis of what features agents use?
  Check web-features/Baseline tooling and HTTP Archive for changes in use counters after coding
  agents arrived.
- **Search w3ctag/design-reviews** for TAG reviews that discussed AI-generated code or agent authors.
- **Ask Lea Verou** (co-presenter) whether #455 should be framed as agent-relevant in the session, and
  whether she has unpublished views on AI and API design.

## Slide

Deck slide id: **`design-principles`**. Drafted outside the repo, at
`/tmp/claude-0/-home-user-agenticwebdx/0e091289-2be0-5593-a12f-600241c59a54/scratchpad/slides/design-principles.html`,
for insertion into `web/index.html`.

- **Title:** “Most principles hold. Some backfire.”
- **Table** (Principle | For humans | For agents | verdict). Rows 1–7 of the audit:
  1. Use common words (TAG §12.1), ✓. “Plain names beat cryptic IDs; abbreviations shatter into
     tokens.”
  2. Be consistent (TAG §2.4, §12.5), ✓. “Agents guess names from patterns; exceptions invite wrong
     guesses.”
  3. Dictionaries, not positional args (TAG §6.5), ✓. “No argument order to recall, at ~1.6× the
     tokens.”
  4. Readable over compact formats (TAG §2.7), ?. “Compact halves tokens (SVG paths); readable avoids
     errors.”
  5. Graceful error recovery (HTML §4.3), ✗. “Silent failure leaves agents ‘programming with a
     blindfold on’.”
  6. Low-level first, libraries on top (EWM), ?. “Glue is cheap but per-project; declarative is
     one-shot, once known.”
  7. Pave the cowpaths (HTML §2.4), ?. “Today's cowpaths are model priors, even repeated
     hallucinations.”
- **Discussion prompt** (revealed with `.next`): “No TAG principle mentions AI. Where do agents fit in
  the priority of constituencies?”
- **Source line:** TAG Design Principles (14 Sep 2026); HTML Design Principles (2007); Extensible Web
  Manifesto (2013); Anthropic; Chrome DevTools MCP; Spracklen et al. 2025. Tokens: o200k.
  Legend: ✓ holds · ? contested · ✗ works against agents.
- **Speaker notes** cover rows 1–7, the TAG issue search, the §1.1/§2.15 discussion prompt and the
  caveats. This file is the fuller record, including rows 8–21, which were considered and dropped.
