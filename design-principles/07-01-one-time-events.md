---
section: "7.1"
id: "one-time-events"
title: "Use promises for one time events"
chapter: "7. Event Design"
url: "https://w3ctag.github.io/design-principles/#one-time-events"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Promises for one-time operations eliminate missed-event race conditions and silent error hangs that frequently stall agent verification loops."
---

# §7.1 Use promises for one time events

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §7.1 one-time-events — Use promises for one time events: Promises for one-time operations eliminate missed-event race conditions and silent error hangs that frequently stall agent verification loops.

- **URL:** https://w3ctag.github.io/design-principles/#one-time-events
- **Chapter:** 7. Event Design
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Promises for one-time operations eliminate missed-event race conditions and silent error hangs that frequently stall agent verification loops.

## Principle Summary

W3C TAG Design Principle §7.1 ("Use promises for one time events") directs specification authors to follow the TAG's *Writing Promise-Using Specifications* guideline and use Promises rather than DOM events (`EventTarget` / `addEventListener`) when an asynchronous operation or state transition happens only once.

For human developers and browsers, legacy APIs that modeled one-shot operations as events—such as `XMLHttpRequest`, `FileReader`, `IDBRequest`, or `HTMLImageElement`'s `load`/`error` events—suffered from temporal race conditions (attaching a listener after the event already fired misses it unless the developer also checks a separate state property like `img.complete` or `document.readyState`), fragmented error handling (`error` events do not integrate with `try/catch` or propagate up the call stack), and callback nesting. Promises solve these problems by latching settled state, unifying success and error handling under `async`/`await`, and composing via `Promise.all()` and `Promise.race()`.

## Fit for Coding Agents

This principle is a strong 'good' fit for AI coding agents—and arguably matters even more for automated agent loops than for human authors. One of the most common failure modes in LLM-generated browser code is the "missed one-time event" race condition: an agent writes `element.addEventListener('load', ...)` or listens for a readiness event without first checking whether the resource or state transition has already completed (for example, omitting `if (img.complete)` when an image is cached, or attaching a `DOMContentLoaded` listener inside an asynchronously loaded script). When a one-time event has already fired, `addEventListener` fails silently—no exception is thrown, the callback simply never executes, and the agent's headless browser or Playwright verification harness hangs until it hits a generic 30-second timeout. Because Promises are state-latching (`await document.fonts.ready`, `await navigator.serviceWorker.ready`, `await animation.finished`, `await img.decode()`), awaiting an already-settled promise resolves immediately, completely eliminating this class of temporal bug.

Second, Promises convert silent hangs into loud, localizable errors in the agent's feedback loop. When agents generate event-driven code for one-shot operations like `FileReader` or `IDBRequest`, they frequently wire the happy-path `load` or `success` listener while omitting the `error` or `abort` listener. If the operation fails at runtime, execution stalls silently with no stack trace. With a Promise-returning API (such as `await blob.text()` or `await fetch()`), an unhandled failure triggers an explicit rejection that surfaces immediately as an `unhandledrejection` console error or test failure with a stack trace pointing directly to the failing `await`.

Finally, Promises align with causal token generation and static type checking. LLMs generate code left-to-right and reason most reliably over linear `async`/`await` control flow with standard `try/catch` blocks, requiring far fewer tokens than instantiating a request object, wiring multiple callbacks, or wrapping events in a manual `new Promise(...)` adapter. Furthermore, `Promise<T>` encodes the resolved payload type directly in TypeScript/JSDoc signatures, whereas DOM events often force agents to guess event name strings and cast untyped targets like `event.target.result`.

## Value as a Slide Example

This principle is a strong (4/5) 'clearly-useful' slide example for W3C TPAC because it demonstrates how agent feedback loops amplify the cost of legacy API ergonomics: for a human developer, an event-based one-shot API is mostly an annoyance of extra boilerplate, whereas for a coding agent running automated browser tests, a missed one-time event or omitted `onerror` listener turns into a silent 30-second test timeout with zero diagnostic signal.

Concrete Web API comparisons for a slide include: (1) Image loading/readiness (`if (!img.complete) img.addEventListener('load', ...)`—where agents routinely forget `img.complete` or `onerror`, causing flaky hangs on cached or broken images—versus state-latching `await img.decode()`); (2) Reading files (`new FileReader()` + `onload`/`onerror`/`readAsText` versus `await blob.text()`); and (3) Readiness latches (`await document.fonts.ready`, `await navigator.serviceWorker.ready`, `await animation.finished`) versus one-time lifecycle events (`DOMContentLoaded`, `window.onload`) that silently never fire if registered after the state transition has already occurred.
