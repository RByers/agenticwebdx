---
section: "6.3"
id: "live-vs-static"
title: "Consider whether objects should be live or static"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#live-vs-static"
agent_fit: "mixed"
slide_example: "neither"
example_strength: 2
verdict: "The live-versus-static distinction is critical for coding agents because hidden liveness or unexpected staleness causes silent runtime bugs, but this two-sentence introductory section merely defines the terms rather than establishing predictable, self-describing conventions."
---

# §6.3 Consider whether objects should be live or static

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=mixed | §6.3 live-vs-static — Consider whether objects should be live or static: The live-versus-static distinction is critical for coding agents because hidden liveness or unexpected staleness causes silent runtime bugs, but this two-sentence introductory section merely defines the terms rather than establishing predictable, self-describing conventions.

- **URL:** https://w3ctag.github.io/design-principles/#live-vs-static
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** mixed
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** The live-versus-static distinction is critical for coding agents because hidden liveness or unexpected staleness causes silent runtime bugs, but this two-sentence introductory section merely defines the terms rather than establishing predictable, self-describing conventions.

## Principle Summary

Section 6.3 introduces the fundamental distinction between *live objects* (which continuously update to reflect current internal browser state at all times, such as `HTMLCollection` or `element.classList`) and *static objects* (which capture a snapshot of state at the moment of creation, such as the `NodeList` from `querySelectorAll()` or a `DOMRect` from `getBoundingClientRect()`). It serves as the umbrella preamble for its subsections, asking specification authors to consciously decide which model an API object should use when exposing internal state.

## Fit for Coding Agents

Whether an API returns a live object or a static snapshot has a profound effect on LLM coding agents, which rely on local reasoning within a bounded context window and depend on loud, deterministic failures in their edit-test feedback loop. When liveness or staleness is not self-describing at the call site or in TypeScript definitions, agents frequently write code with subtle, silent runtime bugs that pass typechecking and basic unit tests.

On one hand, unexpected liveness causes classic mid-iteration mutation bugs: agents regularly write loops like `for (const child of el.children) { ... }` or iterate over `document.getElementsByClassName(...)` while removing or reparenting nodes, silently skipping elements because the underlying `HTMLCollection` updates in place. Compounding the problem, the DOM uses the exact same `NodeList` interface for both live (`el.childNodes`) and static (`el.querySelectorAll()`) collections, erasing any static type signal. On the other hand, inconsistent choices across similar APIs—such as `window.getComputedStyle(el)` returning a live `CSSStyleDeclaration` while `el.getBoundingClientRect()` returns a static `DOMRect` snapshot—lead agents to cache stale snapshots across layout changes or mispredict how state behaves across `await` boundaries.

Because §6.3 itself is only a two-sentence framing section that tells spec authors to "decide whether" an object should be live or static without prescribing a consistent default or requiring syntactic/type-level signaling, its fit for agents is `mixed`. Asking API designers to be intentional about state updates is helpful, but treating live vs. static as an unopinionated, case-by-case toggle leaves coding agents with fragmented statistical priors unless paired with the stricter guidance in its subsections and clear naming/type conventions.

## Value as a Slide Example

On its own, §6.3 is too brief and definitional (just two sentences introducing the terms "live object" and "static object") to serve as a strong standalone slide example (`2/5`, `neither`). It poses a design question rather than stating an opinionated rule, leaving the substantive guidance to its subsections (§6.3.1 and §6.3.2).

However, the underlying tension it introduces is great supporting material if anchored to concrete Web API pairs where invisible live-vs-static differences trip up agents—most notably `el.childNodes` (live `NodeList`) vs. `el.querySelectorAll()` (static `NodeList`), or `getComputedStyle(el)` (live) vs. `getBoundingClientRect()` (static). On a slide, those examples illustrate that coding agents need liveness to follow strict defaults and be visible in types and method names, rather than varying silently per API.
