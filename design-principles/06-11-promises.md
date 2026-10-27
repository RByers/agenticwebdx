---
section: "6.11"
id: "promises"
title: "Design asynchronous APIs using Promises"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#promises"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Promises strongly benefit coding agents by standardizing async signatures, enabling linear async/await control flow, and turning forgotten error callbacks into loud, catchable rejections."
---

# §6.11 Design asynchronous APIs using Promises

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §6.11 promises — Design asynchronous APIs using Promises: Promises strongly benefit coding agents by standardizing async signatures, enabling linear async/await control flow, and turning forgotten error callbacks into loud, catchable rejections.

- **URL:** https://w3ctag.github.io/design-principles/#promises
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Promises strongly benefit coding agents by standardizing async signatures, enabling linear async/await control flow, and turning forgotten error callbacks into loud, catchable rejections.

## Principle Summary

W3C TAG Design Principle §6.11 ("Design asynchronous APIs using Promises") states that whenever a web platform API method needs to be asynchronous—such as when waiting for a user permission prompt, performing disk or network I/O, or executing work on another thread or process—it should return a `Promise` rather than accepting callback functions.

The principle exists to ensure that asynchronous APIs across the web platform share a single composable primitive, allowing developers to chain operations, use standard combinators (`Promise.all`, `Promise.race`), write linear `async`/`await` code, and handle errors uniformly rather than dealing with deeply nested, inconsistent callback conventions.

## Fit for Coding Agents

This principle is a strong positive fit (`good`) for AI coding agents across almost every dimension of agentic code generation and verification. First, it eliminates callback-signature hallucinations. Historically, non-Promise asynchronous Web APIs used inconsistent conventions: split callbacks before options in `navigator.geolocation.getCurrentPosition(success, error, options)`, request objects with `.onsuccess`/`.onerror` event properties in `IndexedDB` and `FileReader`, and Node.js error-first `(err, data)` callbacks elsewhere in the training corpus. Because modern JavaScript/TypeScript training data is overwhelmingly centered on `async`/`await`, coding agents frequently hallucinate that legacy web APIs return Promises (e.g., writing `await navigator.geolocation.getCurrentPosition()`) or pass arguments in the wrong order. Standardizing on Promises reduces the async calling convention to a single uniform shape: parameters go in, `Promise<T>` comes out.

Second, Promises directly improve token efficiency and reasoning accuracy by enabling linear `async`/`await` control flow. Autoregressive models generate and track state sequentially; nested callbacks and event-driven state machines invert control flow and scatter state across closures. When forced to interact with legacy non-Promise web APIs like `IndexedDB`, `FileReader`, or `Geolocation`, agents must repeatedly emit verbose `new Promise((resolve, reject) => ...)` wrapper glue in project after project.

Third, Promises make failures loud and observable in the agent's test/browser feedback loop. In callback APIs where the error callback or `.onerror` handler is optional, an agent that omits error wiring creates a silent failure where execution simply stalls. With Promises, unhandled failures reject the Promise, propagating up the `async`/`await` call stack into enclosing `try`/`catch` blocks or firing a loud `unhandledrejection` event in the console and test runner that the agent can immediately diagnose and fix.

## Value as a Slide Example

This principle is `clearly-useful` to coding agents and merits a **3/5** for slide suitability. It offers a very concrete, relatable illustration of how API uniformity and linear control flow help LLMs: contrasting modern Promise-based APIs (`fetch()`, `navigator.clipboard.readText()`) with legacy pre-Promise holdouts (`navigator.geolocation.getCurrentPosition()`, `IndexedDB`'s `IDBRequest.onsuccess`) immediately shows why agents hallucinate `await` on old APIs or waste tokens wrapping them in `new Promise(...)`.

However, its strength as a headline TPAC 2026 slide example is moderate (3/5 rather than 5/5) because using Promises instead of callbacks has already been settled W3C dogma for over a decade—no spec author today is proposing new callback-based one-shot async methods. On a slide, it serves best as a brief baseline example confirming that classic human DX principles (uniformity, composability, structured error propagation) also serve Agent DX, or as an argument for modernizing remaining legacy callback holdouts like Geolocation and IndexedDB that still trip up coding agents.
