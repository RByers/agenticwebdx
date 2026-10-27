---
section: "7.2"
id: "promises-and-reaction"
title: "Don’t use promises for cancelable events"
chapter: "7. Event Design"
url: "https://w3ctag.github.io/design-principles/#promises-and-reaction"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Sound baseline API hygiene that keeps event cancellation uniform and synchronous, though the real agent footgun is `event.preventDefault()` silently failing after an `await` inside `async` event listeners."
---

# §7.2 Don’t use promises for cancelable events

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §7.2 promises-and-reaction — Don’t use promises for cancelable events: Sound baseline API hygiene that keeps event cancellation uniform and synchronous, though the real agent footgun is `event.preventDefault()` silently failing after an `await` inside `async` event listeners.

- **URL:** https://w3ctag.github.io/design-principles/#promises-and-reaction
- **Chapter:** 7. Event Design
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Sound baseline API hygiene that keeps event cancellation uniform and synchronous, though the real agent footgun is `event.preventDefault()` silently failing after an `await` inside `async` event listeners.

## Principle Summary

In the W3C TAG Web Platform Design Principles document, §7.2 ("Don’t use promises for cancelable events") is a one-sentence cross-reference stub under Chapter 7 (Event Design) that directs readers to §9.2 ("See when to use callback functions instead"). Substantively, it reminds specification authors that JavaScript Promises are the wrong primitive for delivering cancelable or recurring events.

Because a Promise represents a single asynchronous outcome whose `.then()` or `await` reactions always execute asynchronously in a microtask after the synchronous turn has already finished, a promise consumer cannot synchronously inspect an event and call `event.preventDefault()` before the browser executes its default action. Cancelable notifications must therefore use synchronous event dispatch (`EventTarget` / `addEventListener`) or synchronous callbacks, and when an event does need to coordinate with asynchronous work, specs provide an explicit synchronous method on the event object that accepts a promise or async handler (such as `ExtendableEvent.waitUntil(promise)`, `FetchEvent.respondWith(promise)`, or `NavigateEvent.intercept({ handler })`).

## Fit for Coding Agents

This principle is a good fit for coding agents as baseline platform hygiene because it preserves a single, predictable mental model for event cancellation across the web platform. LLM coding agents have strong training-data priors around synchronous `addEventListener(type, (e) => { e.preventDefault(); })` on the one hand and `const result = await asyncOperation()` on the other. Because JavaScript Promises settle asynchronously on a microtask boundary and provide no channel to propagate a synchronous cancellation decision back to the producer before the browser's default action runs, attempting to deliver cancelable events via promises would require awkward, non-standard API shapes that agents would frequently hallucinate or misuse.

At the same time, examining the intersection of promises and cancelable events from an agentic DX perspective highlights one of the most common bugs LLM coding agents write in frontend code today: passing an `async` function to `addEventListener` and calling `event.preventDefault()` after an `await` (for example, `form.addEventListener('submit', async (e) => { const ok = await check(); if (!ok) e.preventDefault(); })`). Because `EventTarget` ignores the promise returned by an `async` listener and evaluates cancellation as soon as the synchronous call frame yields at the first `await`, the delayed `e.preventDefault()` fails to cancel the default action.

Crucially for an agent's self-correction loop, calling `event.preventDefault()` after synchronous event dispatch has completed is a completely silent no-op—it neither throws an error nor logs a warning. By contrast, modern platform event APIs that explicitly bridge synchronous event interception with asynchronous promise work—such as the Navigation API's `navigateEvent.intercept({ async handler() { ... } })` or Service Worker's `fetchEvent.respondWith(promise)`—require synchronous registration during dispatch and throw a loud `InvalidStateError` `DOMException` if called after an `await`. While §7.2 rightly steers spec authors away from using promises to deliver cancelable events, agents benefit most when event APIs also fail loudly if cancellation or interception is attempted asynchronously.

## Value as a Slide Example

§7.2 is not a strong standalone slide example (`neither`, strength 2/5) because in the W3C TAG document it is literally a seven-word cross-reference stub ("See when to use callback functions instead.") pointing to §9.2 (`when-to-use-callback-functions`). Moreover, the rule that a Promise cannot deliver a synchronously cancelable event is a direct mechanical consequence of JavaScript's microtask queue rather than a revealing tension between human and agent ergonomics.

However, the closely related footgun in consumer code—where coding agents routinely write `async (e) => { await ...; e.preventDefault(); }` and get no feedback because `event.preventDefault()` after an `await` is a silent no-op, whereas `NavigateEvent.intercept()` and `FetchEvent.respondWith()` throw a loud `InvalidStateError` `DOMException`—makes a compelling secondary code example if a slide contrasts legacy silent no-ops with loud, agent-friendly state errors.
