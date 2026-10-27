---
section: "11.4"
id: "implementability"
title: "Resolving tension between interoperability and implementability"
chapter: "11. Writing good specifications"
url: "https://w3ctag.github.io/design-principles/#implementability"
agent_fit: "mixed"
slide_example: "clearly-harmful"
example_strength: 3
verdict: "Primarily a multi-engine spec governance principle, though coding agents amplify its warning about dominant-engine entrenchment while inverting the cost tradeoff between feature-detectable API splits and silent behavioral divergence."
---

# §11.4 Resolving tension between interoperability and implementability

GREP_SUMMARY: slide_example=clearly-harmful | strength=3/5 | agent_fit=mixed | §11.4 implementability — Resolving tension between interoperability and implementability: Primarily a multi-engine spec governance principle, though coding agents amplify its warning about dominant-engine entrenchment while inverting the cost tradeoff between feature-detectable API splits and silent behavioral divergence.

- **URL:** https://w3ctag.github.io/design-principles/#implementability
- **Chapter:** 11. Writing good specifications
- **Agent-Fit:** mixed
- **Slide-Example:** clearly-harmful
- **Example-Strength:** 3/5
- **Verdict:** Primarily a multi-engine spec governance principle, though coding agents amplify its warning about dominant-engine entrenchment while inverting the cost tradeoff between feature-detectable API splits and silent behavioral divergence.

## Principle Summary

This principle guides specification authors when browser vendors cannot agree on a single, fully interoperable design that every engine is willing or able to implement. It prioritizes end-user benefit and outlines a hierarchy of fallback strategies depending on the cause of the disagreement. If an implementor identifies end-user harm (such as `SharedArrayBuffer` enabling high-precision timers for Spectre attacks), the feature should not be specified and existing implementations should un-ship it despite author disruption.

When the disagreement is over engine architecture rather than user harm, the principle weighs three compromises: (1) specifying the same API with minor non-interoperable behavior (e.g., `backdrop-filter`), which avoids forcing authors to branch code now and lets sites benefit automatically if engines converge later, at the cost of making differences impossible to feature-detect; (2) specifying different, feature-detectable APIs or isolated engine-specific sub-components (e.g., Content Decryption Modules in Encrypted Media Extensions or payment method identifiers in `PaymentRequest`), which let authors detect and adapt to differences when behavioral gaps are too large, at the cost of extra authoring complexity and long-term maintenance of multiple APIs; or (3) specifying partial or single-implementor features where authors must feature-detect availability—an outcome the TAG strongly discourages because authors often assume the dominant browser's behavior or API is universal, further entrenching the dominant engine.

## Fit for Coding Agents

While this principle is primarily aimed at standards bodies navigating multi-engine constraints, the developer-experience tradeoffs it weighs behave quite differently when code is written and verified by AI agents rather than human developers (`mixed` fit).

First, coding agents strongly validate and amplify the principle's warnings about dominant-engine entrenchment and single-implementor APIs, as well as the cost of un-shipping features. LLMs learn from open-source corpora that heavily skew toward Chromium-first code, and agentic feedback loops almost always default to a single headless browser (typically Chromium via Playwright or Puppeteer) unless explicitly configured otherwise. When a spec ships in only one engine, an agent will frequently generate it without feature detection because it predominates in training examples and passes the agent's default single-browser test run. Conversely, when a shipped feature is un-shipped or retrofitted with security gates (such as `SharedArrayBuffer` requiring cross-origin isolation via `COOP`/`COEP` headers after Spectre), persistent pre-change examples in model weights cause agents to hallucinate broken, un-gated usage for years. Isolating non-standard parts into small, declarative configuration tokens inside a shared framework (as in `PaymentRequest` or EME) works well for agents, because the structural orchestration code remains uniform across training data while only a small parameter changes.

Second, coding agents invert the principle's tradeoff between non-feature-detectable behavioral differences and explicit, feature-detectable API variants. For humans, writing and maintaining feature-detection branches across multiple APIs is tedious boilerplate, which leads the principle to favor sharing a single API even when visible behavioral differences exist (`backdrop-filter`), provided those differences aren't catastrophic. For an AI agent, however, generating feature-detection branches or fallback logic is cheap in both time and tokens, provided the difference is machine-observable. When engines expose distinct APIs or explicit capability queries, static tooling (TypeScript DOM types, MDN/Baseline MCP servers, ESLint compat plugins) and runtime checks can immediately alert the agent that a fallback is needed. By contrast, when two engines implement the exact same API surface with subtle, non-feature-detectable behavioral differences, neither type-checking nor runtime feature detection can warn the agent, leading to silent cross-browser bugs that evade single-engine agent verification loops.

## Value as a Slide Example

This principle is rated `neither` (2/5 strength) as a standalone TPAC slide example. Because it is fundamentally a meta-governance guideline for W3C working groups handling vendor impasses rather than a direct API design pattern, putting it on a slide would require too much standards-process exposition for a talk focused on agentic DX.

However, two concrete insights from this section make good supporting talking points if the session discusses cross-browser interoperability and Baseline: (1) the TAG's warning that authors may assume the dominant implementation is "correct" applies doubly to LLMs trained on skewed corpora and verified in headless Chromium, and (2) hiding engine differences behind the same API name (`backdrop-filter`) deprives agents of the static and runtime signals they rely on to self-correct, whereas explicit feature-detectable surfaces (`PaymentRequest`, `CSS.supports()`) allow agents and compatibility tools to automatically generate cross-browser fallbacks.
