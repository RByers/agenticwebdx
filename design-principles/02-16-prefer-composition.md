---
section: "2.16"
id: "prefer-composition"
title: "Build complex types by composing simpler types"
chapter: "2. API Design Across Languages"
url: "https://w3ctag.github.io/design-principles/#prefer-composition"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Liskov Substitution and composition over inheritance directly protect LLM coding agents from false-positive type checks in lib.dom.d.ts and supertype-prior hallucinations."
---

# §2.16 Build complex types by composing simpler types

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §2.16 prefer-composition — Build complex types by composing simpler types: Liskov Substitution and composition over inheritance directly protect LLM coding agents from false-positive type checks in lib.dom.d.ts and supertype-prior hallucinations.

- **URL:** https://w3ctag.github.io/design-principles/#prefer-composition
- **Chapter:** 2. API Design Across Languages
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Liskov Substitution and composition over inheritance directly protect LLM coding agents from false-positive type checks in lib.dom.d.ts and supertype-prior hallucinations.

## Principle Summary

W3C TAG Design Principle §2.16 (`prefer-composition`) states that Web APIs should only use interface inheritance when the subtype satisfies the Liskov Substitution Principle (LSP)—meaning every attribute, method, and behavioral expectation of the supertype applies consistently to the subtype so it can always stand in for its parent.

Because maintaining strict behavioral compatibility across inheritance hierarchies is difficult and prone to leaky abstractions, the principle recommends avoiding inheritance when in doubt and instead building complex types by composing simpler existing types as properties on the new interface.

## Fit for Coding Agents

This principle is a strong fit (`good`) for AI coding agents because it directly governs the fidelity of the static type system (`lib.dom.d.ts`) and aligns with how LLMs generalize across API surfaces. In an agentic workflow, TypeScript (`tsc`) and LSP diagnostics are the fastest, cheapest feedback loop available before launching a headless browser. Because WebIDL inheritance maps directly to `interface Child extends Parent` in `lib.dom.d.ts`, any violation of the Liskov Substitution Principle in a web spec corrupts the static type checker: `tsc` will happily permit calling inherited supertype methods or passing the subtype to functions expecting the supertype, hiding the failure until runtime execution. Historical DOM hierarchy quirks—such as leaf `Node` subclasses like `Text` or `Comment` inheriting `appendChild()` and `insertBefore()` only to throw `HierarchyRequestError` at runtime—are classic traps where the type system tells an agent an operation is valid when it is not.

Furthermore, LLMs build strong statistical priors around common base types (`Node`, `Element`, `EventTarget`, `ReadableStream`). When a subtype inherits from a parent interface but overrides methods to throw `NotSupportedError` or subtly changes behavioral contracts, the model's weights bias it toward emitting standard base-class patterns that fail silently or at runtime on the subtype. Conversely, building complex types by composing simpler, well-known primitives on explicit properties—such as `Request`/`Response` exposing `.headers` (`Headers`) and `.body` (`ReadableStream`), `TransformStream` exposing `.readable` and `.writable`, `AbortController` exposing `.signal` (`AbortSignal`), or custom elements exposing `ElementInternals` via `attachInternals()`—makes capabilities self-describing in the token stream and allows agents to reuse standard idioms for the simpler component types without inheritance ambiguity.

## Value as a Slide Example

This principle is a `clearly-useful` (`3/5`) candidate example for TPAC because it highlights an important structural link between web standards and AI coding agents: **WebIDL is the upstream source of `lib.dom.d.ts`, which acts as the primary static verification oracle for coding agents.** Concrete Web API contrasts make this tangible on a slide: legacy DOM inheritance (`Text` and `Comment` inheriting `Node.appendChild()`, which compiles cleanly in TypeScript but throws `HierarchyRequestError` at runtime) vs. modern composable APIs (`TransformStream` composing `.readable` and `.writable`, `AbortController` composing `.signal`, or `Response` composing `.headers` and `.body`).

It rates a `3/5` rather than a `5/5` because Liskov Substitution and "prefer composition over inheritance" are classic object-oriented design principles where human and agent incentives already point in the same direction. While it reinforces why disciplined WebIDL type modeling matters even more when agents rely on `tsc` as a verification loop, it is less counter-intuitive or provocative as a standalone headline slide than principles where agent ergonomics actively conflict with traditional human DX.
