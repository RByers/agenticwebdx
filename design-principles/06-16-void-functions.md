---
section: "6.16"
id: "void-functions"
title: "Return undefined from side-effect-causing functions"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#void-functions"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Helps coding agents by enforcing Command–Query Separation and rejecting human-centric fluent chaining (`return this`), though its main rationale is backwards-compatible spec evolution rather than agent ergonomics."
---

# §6.16 Return undefined from side-effect-causing functions

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §6.16 void-functions — Return undefined from side-effect-causing functions: Helps coding agents by enforcing Command–Query Separation and rejecting human-centric fluent chaining (`return this`), though its main rationale is backwards-compatible spec evolution rather than agent ergonomics.

- **URL:** https://w3ctag.github.io/design-principles/#void-functions
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Helps coding agents by enforcing Command–Query Separation and rejecting human-centric fluent chaining (`return this`), though its main rationale is backwards-compatible spec evolution rather than agent ergonomics.

## Principle Summary

When a function's purpose is to cause side effects rather than compute a value, it should be specified to return `undefined` (following Command–Query Separation) rather than returning `this` for method chaining or another incidental value.

Because websites rarely come to depend on an `undefined` return value, this preserves backwards compatibility if the specification later needs to evolve the method to return a meaningful value—as when `HTMLMediaElement.prototype.play()` was upgraded from returning `undefined` to returning a `Promise` to surface asynchronous playback failures.

## Fit for Coding Agents

Fluent method chaining (`return this`, popularized by jQuery and present in APIs like `Set.prototype.add` or `Map.prototype.set`) was designed to save humans keystrokes and temporary variables. Coding agents do not benefit from saving a few tokens to repeat an object identifier, and discrete one-statement-per-line calls produce cleaner diffs and line-level stack traces in an agent's verification loop. Worse, returning non-`undefined` values from side-effecting methods is a well-known source of LLM bugs across JavaScript and the DOM: models frequently confuse in-place mutators that return the receiver (`Array.prototype.sort()`, `Array.prototype.reverse()`) with immutable copy methods (`toSorted()`, `map()`, `slice()`), or misinterpret incidental return values (`Array.prototype.push()` returning the new length, `Node.prototype.appendChild()` returning the appended child rather than the parent). Specifying `undefined` (`void` in WebIDL and TypeScript) makes pure side-effect commands unmistakable to both the LLM and the type checker, as seen in modern DOM methods like `Element.prototype.append()`.

In addition, preserving the ability to upgrade `HTMLMediaElement.prototype.play()` from `undefined` to a `Promise` directly benefited coding agents by turning silent asynchronous playback and autoplay failures (`NotAllowedError`, `AbortError`) into loud, awaitable signals in headless browser test loops. The only caveat for agents is that actually changing a function's return value years after shipping splits the LLM training corpus: because historical web code calls `video.play()` without handling a Promise, agents sometimes generate un-awaited `play()` calls that cause unhandled promise rejections today. For agents, returning a `Promise` or result object from day one whenever an operation can fail is preferable to relying on `undefined` as a temporary placeholder.

## Value as a Slide Example

Although this principle aligns with coding agents by rejecting `return this` method chaining in favor of Command–Query Separation, its primary rationale in the TAG document is backwards-compatible spec evolution rather than authoring ergonomics. Because it focuses mainly on keeping return slots free for future spec revisions, it is too indirect to serve as a standalone headline slide example (`neither`, 2/5).

It could still be mentioned briefly as a supporting detail when contrasting human keystroke-saving idioms with LLM predictability: fluent chaining (`return this`) and incidental return values on mutators (`Node.appendChild()` returning the child, `Array.push()` returning the length, `Array.sort()` mutating in-place while returning the array) blur command vs. query semantics for agents, whereas modern `void` DOM APIs like `Element.append()` make side effects unambiguous in TypeScript signatures.
