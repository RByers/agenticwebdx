---
section: "6.10"
id: "synchronous"
title: "Be synchronous when appropriate"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#synchronous"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Synchronous APIs for fast, local operations help coding agents avoid viral async refactoring across files, silent truthy-Promise bugs in conditionals and array callbacks, and complex async state-synchronization boilerplate in UI components."
---

# §6.10 Be synchronous when appropriate

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §6.10 synchronous — Be synchronous when appropriate: Synchronous APIs for fast, local operations help coding agents avoid viral async refactoring across files, silent truthy-Promise bugs in conditionals and array callbacks, and complex async state-synchronization boilerplate in UI components.

- **URL:** https://w3ctag.github.io/design-principles/#synchronous
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Synchronous APIs for fast, local operations help coding agents avoid viral async refactoring across files, silent truthy-Promise bugs in conditionals and array callbacks, and complex async state-synchronization boilerplate in UI components.

## Principle Summary

W3C TAG Design Principle §6.10 ("Be synchronous when appropriate") advises specification authors to prefer synchronous JavaScript APIs over asynchronous ones whenever an operation is fast, deterministic, purely local (not blocked by locks, disk/network I/O, or cross-process IPC), and will never require gating behind a permission prompt or user dialog. While the web platform generally favors asynchronous APIs to avoid blocking the main thread and to accommodate multi-process browser architectures, making an API asynchronous when none of those constraints apply imposes unnecessary setup and "function coloring" (`async`/`await` propagation) on web developers.

## Fit for Coding Agents

This principle is a strong fit for AI coding agents (`agent_fit: good`), and for deeper structural reasons than mere typing convenience. While it is tempting to assume that `async`/`await` ceremony is virtually free for an LLM to generate, unnecessary asynchrony in JavaScript creates severe structural hazards for coding agents operating within bounded context windows and iterative feedback loops. First, making a leaf operation asynchronous triggers viral "function coloring": the enclosing function must become `async` and return a `Promise`, forcing every caller up the call graph to be refactored across files. Worse, many critical execution contexts on the web and in UI frameworks cannot be made `async` at all—including class constructors, synchronous DOM event listeners that must invoke `event.preventDefault()` before yielding, and synchronous component render passes. In frameworks like React, an asynchronous API for a value needed during render forces an agent to replace a simple inline expression with `useState` and `useEffect` state-synchronization boilerplate, introducing flash-of-incomplete-state bugs and stale closures.

Second, when an operation is conceptually a fast, local computation or check, LLM statistical priors strongly expect a synchronous return value. When such an API returns a `Promise` instead, agents frequently omit `await` in conditionals (`if (checkSomething())`) or pass an `async` callback to synchronous array methods (`items.filter(async item => ...)`). Because every `Promise` object is truthy in JavaScript, these errors fail silently at runtime without throwing an exception—taking the truthy branch unconditionally or keeping every array element—which makes them difficult for an agent to catch without strict type-aware lint rules (`no-floating-promises` / `no-misused-promises`).

Finally, synchronous execution preserves linear control flow and state invariants. Because no microtasks, timers, or concurrent event handlers can interleave during a synchronous call, agents do not need to reason about re-entrancy, race conditions, or component unmounts occurring mid-operation.

## Value as a Slide Example

This principle is a solid supporting candidate (`clearly-useful`, strength 3/5) for a TPAC slide because it counters a common misconception about AI coding agents: that "ergonomic ceremony doesn't matter anymore because LLMs can type `async`/`await` for free." Concrete web platform examples illustrate the contrast well: fast, local, synchronous APIs like `URL.canParse()`, `structuredClone()`, `crypto.randomUUID()`, and `CSS.supports()` compose cleanly in expressions, `.filter()` pipelines, and framework render passes, whereas seemingly local operations that are asynchronous—most notably `crypto.subtle.digest()` for computing a SHA-256 hash in memory—routinely trip up agents into either hallucinating synchronous Node-style `crypto.createHash()` calls in browser code, breaking synchronous call chains across files, or introducing silent truthy-Promise bugs.

However, it rates a 3/5 rather than a 5/5 headline example because the choice between synchronous and asynchronous APIs in web standards is mostly dictated by hard browser architecture and security constraints (cross-process IPC, hardware locks, disk/network I/O, and permission prompts) rather than developer ergonomics alone. Standards groups already make APIs synchronous when those constraints allow, so while the principle clearly benefits agents, it offers less actionable leverage for changing how standards are designed than principles governing error reporting, introspection, or declarative primitives.
