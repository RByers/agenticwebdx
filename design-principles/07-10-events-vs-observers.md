---
section: "7.10"
id: "events-vs-observers"
title: "Use Events and Observers appropriately"
chapter: "7. Event Design"
url: "https://w3ctag.github.io/design-principles/#events-vs-observers"
agent_fit: "mixed"
slide_example: "clearly-harmful"
example_strength: 3
verdict: "Defaulting to EventTarget helps agents via shared base-class ergonomics (once, AbortSignal), but the codified Observer pattern permits constructor-vs-observe() option placement and cleanup variations that cause frequent silent failures in LLM-generated code."
---

# §7.10 Use Events and Observers appropriately

GREP_SUMMARY: slide_example=clearly-harmful | strength=3/5 | agent_fit=mixed | §7.10 events-vs-observers — Use Events and Observers appropriately: Defaulting to EventTarget helps agents via shared base-class ergonomics (once, AbortSignal), but the codified Observer pattern permits constructor-vs-observe() option placement and cleanup variations that cause frequent silent failures in LLM-generated code.

- **URL:** https://w3ctag.github.io/design-principles/#events-vs-observers
- **Chapter:** 7. Event Design
- **Agent-Fit:** mixed
- **Slide-Example:** clearly-harmful
- **Example-Strength:** 3/5
- **Verdict:** Defaulting to EventTarget helps agents via shared base-class ergonomics (once, AbortSignal), but the codified Observer pattern permits constructor-vs-observe() option placement and cleanup variations that cause frequent silent failures in LLM-generated code.

## Principle Summary

This principle advises spec authors to default to `EventTarget` and standard notification `Event`s rather than inventing a custom `*Observer` class, unless `EventTarget` genuinely cannot work well for the feature. It emphasizes that inheriting from `EventTarget` ensures an API automatically benefits from platform-wide improvements to the shared base class (such as `{ once: true }` and `AbortSignal` support), and clarifies a common misconception: `EventTarget` events do not have to be synchronous or bubble through the DOM tree, and can batch changes or use microtask/animation-frame timing just like Observers.

When `EventTarget` is insufficient—such as when high-frequency DOM/layout notifications would cause unmanageable synchronous recursion (as legacy DOM Mutation Events did), when multiple targets need to be observed with a single callback, when per-observation configuration options are needed, or when authors need to pull pending notifications synchronously via `takeRecords()`—the principle outlines the standard Web Observer pattern (`MutationObserver`, `IntersectionObserver`, `ResizeObserver`). In this pattern, an Observer is constructed with a callback (and optionally options), begins observing via `observe(target, options?)`, delivers batched change records to the callback, and stops observing via `unobserve()` or `disconnect()`.

## Fit for Coding Agents

This principle cuts both ways (`mixed`) for AI coding agents. On the positive side, pushing spec authors to default to `EventTarget` instead of proliferating bespoke Observer classes is a major win for agent ergonomics. `EventTarget` is one of the most deeply entrenched primitives in LLM training data, and every improvement to `addEventListener`—most notably `{ once: true }` and declarative lifecycle cleanup via `{ signal: abortController.signal }`—transfers across all `EventTarget` subclasses automatically. Furthermore, where Observers are used for high-frequency DOM or layout state (`MutationObserver`, `ResizeObserver`, `IntersectionObserver`), delivering batched asynchronous records avoids the catastrophic failure mode of legacy DOM Mutation Events: infinite synchronous recursion loops and layout thrashing that hang the browser tab without throwing an actionable error into the agent's verification loop.

On the negative side, the Observer pattern as codified by §7.10 contains "near-miss" inconsistencies across Web APIs that are notorious traps for statistical code generators. Specifically, §7.10 explicitly permits observation options to be passed either to the constructor or to `observe()` ("The options to customize what should be observed may be provided here [`observe()`] instead of to the constructor"), and allows cleanup via "a method called `unobserve()` or `disconnect()`". Because LLMs blend priors across the `Observer` family (`IntersectionObserver`, `MutationObserver`, `ResizeObserver`, `PerformanceObserver`), this variability directly produces high-frequency hallucinations—several of which fail silently at runtime due to WebIDL ignoring extra arguments.

For example, an agent applying the `MutationObserver`/`ResizeObserver` signature (`observer.observe(target, options)`) to `IntersectionObserver` by writing `io.observe(el, { threshold: 0.5 })` triggers a completely silent failure: `IntersectionObserver` only accepts options in its constructor, and WebIDL silently drops the second argument to `observe(target)`. Conversely, passing options to `new MutationObserver(cb, { childList: true })` is silently ignored by the constructor and only fails later when `mo.observe(el)` throws a `TypeError`. Similarly, `MutationObserver` lacks `unobserve(el)` (unlike `IntersectionObserver` and `ResizeObserver`), callback parameters are arrays of change records (`entries`) rather than single `Event` objects (leading to silent `undefined` reads when agents write `(entry) => entry.contentRect`), and Observers lack `{ signal }` (`AbortSignal`) integration for cleanup.

## Value as a Slide Example

While not a standalone headline slide example of a principle that is purely useful or purely harmful (`neither`, 3/5), §7.10 provides a sharp supporting contrast between shared base classes (`EventTarget`) and loose structural conventions (`*Observer`). When an API inherits from `EventTarget`, agents benefit from identical argument signatures and platform-wide ergonomics like `{ once, signal }`. By contrast, because the "Observer pattern" is a loose convention where §7.10 permits options in either `new FooObserver(cb, options)` (`IntersectionObserver`) or `observer.observe(target, options)` (`MutationObserver`, `ResizeObserver`), LLMs frequently cross-contaminate the two—turning `io.observe(el, { threshold: 0.5 })` into a silent bug when WebIDL ignores the extra argument.

On a slide, this concrete contrast (`IntersectionObserver` constructor options vs. `MutationObserver`/`ResizeObserver` `observe()` options, plus missing `unobserve()` and `AbortSignal` support) illustrates why "almost-consistent" design patterns are worse for statistical models than true shared base classes or strict WebIDL mixins.
