---
section: "6.12"
id: "aborting"
title: "Cancel asynchronous APIs/operations using AbortSignal"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#aborting"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Uniformly accepting an AbortSignal in an options dictionary aligns with LLM priors across APIs, prevents hallucinated .cancel() methods on Promises, and eliminates error-prone multi-resource cleanup boilerplate."
---

# §6.12 Cancel asynchronous APIs/operations using AbortSignal

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §6.12 aborting — Cancel asynchronous APIs/operations using AbortSignal: Uniformly accepting an AbortSignal in an options dictionary aligns with LLM priors across APIs, prevents hallucinated .cancel() methods on Promises, and eliminates error-prone multi-resource cleanup boilerplate.

- **URL:** https://w3ctag.github.io/design-principles/#aborting
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Uniformly accepting an AbortSignal in an options dictionary aligns with LLM priors across APIs, prevents hallucinated .cancel() methods on Promises, and eliminates error-prone multi-resource cleanup boilerplate.

## Principle Summary

W3C TAG Design Principle §6.12 states that whenever an asynchronous method or operation can be cancelled, web APIs should allow authors to pass an `AbortSignal` inside an `options` dictionary (e.g., `api.read({ signal })`). Even when underlying cancellation is best-effort rather than guaranteed, `AbortController.abort()` acts as a standard cancellation request rather than a hard guarantee.

This principle exists to prevent every web specification from inventing its own incompatible cancellation primitive (such as returning custom handle objects instead of Promises, adding bespoke `.cancel()` or `.abort()` methods, or requiring separate `unobserve`/`remove*` calls). By standardizing on `AbortController` and `AbortSignal`, developers can coordinate and cancel multiple heterogeneous operations at once—such as network fetches, event listeners, streams, and lock requests—upon user cancellation or single-page application route changes.

## Fit for Coding Agents

This principle is a strong positive fit (`good`) for AI coding agents because it replaces bespoke per-API cancellation idioms with a single, transferable structural pattern (`{ signal }`). Because JavaScript `Promise` objects do not have a built-in `.cancel()` or `.abort()` method, coding agents frequently hallucinate non-existent cancellation methods on returned Promises or struggle to refactor async functions when cancellation is requested after the fact (since returning a custom controller object breaks standard `async`/`await` signatures). Accepting `{ signal }` in the options bag preserves standard Promise return types while giving models a predictable convention that generalizes zero-shot to newer or less-common APIs (`navigator.locks.request(name, { signal })`, `scheduler.postTask(fn, { signal })`, `ReadableStream`, `fetch`, and `addEventListener`).

Using a shared `AbortSignal` also dramatically reduces multi-step bookkeeping and resource-leak bugs in agent-generated teardown code (such as React `useEffect` cleanup functions, Web Component `disconnectedCallback`, or SPA navigation handlers). Without `AbortSignal`, an agent registering three event listeners and an async request must allocate and track named callback references and matching `removeEventListener` flags—a frequent source of subtle bugs when agents pass inline arrow functions or forget to clean up one of several resources. With `{ signal }`, the agent can keep inline closures and emit a single `controller.abort()` on teardown, or use declarative combinators like `AbortSignal.timeout(ms)` and `AbortSignal.any([...])` instead of hand-rolling leaky `setTimeout` + `Promise.race` glue.

The main caveat for coding agents is error-handling ergonomics on the consumer side: when an `AbortSignal` triggers, pending operations reject with an `AbortError` `DOMException` (or custom `signal.reason`), and agents often forget to ignore `err.name === 'AbortError'` inside generic `catch` blocks, unintentionally logging or surfacing user-initiated cancellations as application failures. Additionally, because `addEventListener(..., { signal })` arrived later than `removeEventListener`, training-data priors still sometimes bias agents toward manual `removeEventListener` unless prompted. Even with those nuances, standardizing on `{ signal }` is a major ergonomic and reliability win for LLM code generation.

## Value as a Slide Example

This principle is a strong (`4/5`) candidate for a `clearly-useful` slide example illustrating how cross-API structural uniformity and composable primitives directly reduce LLM hallucinations and state-tracking bugs.

On a TPAC slide, it provides an immediately recognizable contrast between legacy bespoke teardown ceremonies (`xhr.abort()`, `clearTimeout(id)`, storing exact callback references and capture flags for `removeEventListener`, or hallucinating `promise.cancel()`) versus passing `{ signal }` uniformly across `fetch()`, `addEventListener()`, `navigator.locks.request()`, and `scheduler.postTask()`, or using `AbortSignal.timeout(5000)` to eliminate manual timer + `Promise.race` boilerplate.
