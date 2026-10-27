---
section: "6.8"
id: "overloading"
title: "Use overloading wisely"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#overloading"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Strongly helps coding agents by preventing cross-overload parameter hallucination, silent runtime misbehavior, and noisy multi-overload TypeScript diagnostics."
---

# §6.8 Use overloading wisely

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §6.8 overloading — Use overloading wisely: Strongly helps coding agents by preventing cross-overload parameter hallucination, silent runtime misbehavior, and noisy multi-overload TypeScript diagnostics.

- **URL:** https://w3ctag.github.io/design-principles/#overloading
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Strongly helps coding agents by preventing cross-overload parameter hallucination, silent runtime misbehavior, and noisy multi-overload TypeScript diagnostics.

## Principle Summary

W3C TAG §6.8 advises API designers to define separate, distinctly named methods when behavior differs significantly, rather than overloading a single method name with different signatures. It endorses two benign forms of flexibility—allowing an argument to accept either a single value or an array of values (`T | T[]`), and accepting an options dictionary—while warning against overloads where the meaning or types of subsequent arguments change based on earlier arguments or input types.

For human developers and browser engines, this principle exists to keep call sites readable and API capabilities discoverable. When a single method acts as a Swiss-army knife whose positional parameters shift meaning depending on argument count or runtime types, readers cannot tell what a call does without mentally running the overload resolution algorithm, and IDE autocomplete struggles to infer which signature the author intends.

## Fit for Coding Agents

This principle aligns strongly with how LLM coding agents generate, read, and debug code. Autoregressive models predict arguments token-by-token conditioned on the method name and preceding arguments. When one method name maps to multiple distinct behaviors or shifting positional signatures, the model's probability distribution blends patterns from all overloads in its training corpus. This regularly causes cross-overload hallucination—mixing parameters from one overload into another—whereas giving distinct behaviors separate method names (such as `Array.of()` and `Array.from()` instead of overloaded `new Array()`) anchors the model's intent in a single semantic token before any arguments are emitted.

Furthermore, complex overloading degrades the agent's automated feedback loop in both static type-checking and runtime execution. In TypeScript (`lib.dom.d.ts`), heavily overloaded Web APIs produce notorious walls of compiler output (`No overload matches this call. Overload 1 of 3 gave the following error...`), which bloat context windows and frequently mislead agents into "fixing" the call to match the wrong overload signature. Worse, at runtime, type- or arity-based overloads with compatible primitive types often fail silently rather than throwing a `TypeError`: if an agent passes the wrong number of numeric arguments or the wrong type, the browser resolves to a valid but unintended overload, leaving the agent with no exception in the console to trigger self-correction.

Conversely, the two patterns §6.8 explicitly encourages—`T | T[]` unions and options dictionaries—are ideal for coding agents. Accepting either a single value or an array absorbs minor model uncertainty about whether a single argument needs array wrapping, avoiding unnecessary runtime exceptions. Options dictionaries replace fragile positional index tracking with explicit property keys that are self-describing in the prompt context and yield pinpoint, single-line typechecker errors when a key is misspelled or mistyped.

## Value as a Slide Example

§6.8 is a strong (4/5) `clearly-useful` slide candidate, especially paired with §6.7 (options dictionaries), because the Web platform contains famous historical violations that visibly trip up both LLMs and TypeScript tooling. The standout example is `CanvasRenderingContext2D.drawImage()`, which takes 3, 5, or 9 arguments where arguments 2–5 flip meaning from destination coordinates `(dx, dy, dWidth, dHeight)` in the 5-argument form to source crop coordinates `(sx, sy, sWidth, sHeight)` in the 9-argument form. LLMs routinely confuse the parameter order, and because all parameters are numbers, bad calls fail silently by rendering a misplaced image that an agent cannot detect from console logs.

Other concrete Web API examples that resonate immediately with a W3C TPAC audience include `WebGLRenderingContext.texImage2D()` (whose 6- to 10-argument overloads generate notoriously unreadable TypeScript overload errors that derail agent repair loops) and `new Array(3)` vs `new Array("3")` (type-dependent behavior later fixed by explicit factory methods `Array.of()` and `Array.from()`). Together, these illustrate how human readability rules around method naming and overloading directly govern LLM token disambiguation and compiler error quality.
