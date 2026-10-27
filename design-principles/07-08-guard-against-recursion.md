---
section: "7.8"
id: "guard-against-recursion"
title: "Guard against potential recursion"
chapter: "7. Event Design"
url: "https://w3ctag.github.io/design-principles/#guard-against-recursion"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 2
verdict: "Primarily an internal spec-correctness rule for re-entrancy and cross-thread event queuing; while idempotent guards and event state snapshots protect agent-written listeners from stack overflows and race conditions, silent early returns on non-idempotent methods can mask control-flow bugs."
---

# §7.8 Guard against potential recursion

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=neutral | §7.8 guard-against-recursion — Guard against potential recursion: Primarily an internal spec-correctness rule for re-entrancy and cross-thread event queuing; while idempotent guards and event state snapshots protect agent-written listeners from stack overflows and race conditions, silent early returns on non-idempotent methods can mask control-flow bugs.

- **URL:** https://w3ctag.github.io/design-principles/#guard-against-recursion
- **Chapter:** 7. Event Design
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Primarily an internal spec-correctness rule for re-entrancy and cross-thread event queuing; while idempotent guards and event state snapshots protect agent-written listeners from stack overflows and race conditions, silent early returns on non-idempotent methods can mask control-flow bugs.

## Principle Summary

Section 7.8 ("Guard against potential recursion") advises specification authors on preventing re-entrancy bugs when long-running or complex algorithms fire events. Because events are dispatched synchronously, user event handlers may call back into the same API method or mutate related state while the outer algorithm is still running—for example, `AbortController.abort()` running `AbortSignal` abort steps (like `ReadableStreamPipeTo` cleanup) that resolve promises or invoke callbacks which call `abort()` again or modify the signal's internal algorithm collection mid-iteration.

The principle contrasts two specification techniques to handle this: "guarding" the algorithm (updating state and returning immediately if the algorithm is already running, which allows synchronous events where handlers can inspect live state directly on the target object) and "deferring" events via the task queue ("queue a task to fire an event...", which is required for cross-thread events). Because deferred events may run after the object's state has changed again, specs that defer events must copy relevant state onto an `Event` subclass (e.g., `ProgressEvent.loaded`/`total`), define an explicit guarded state machine (e.g., `PaymentRequest`'s `[[state]]` slot), or use a `Promise` if the event merely signals one-time completion.

## Fit for Coding Agents

This principle is primarily neutral with respect to AI coding agents because its core focus is internal specification soundness and browser engine invariants: preventing iterator invalidation on internal spec collections (such as mutating an `AbortSignal`'s algorithm set while `ReadableStreamPipeTo` abort steps are iterating over it), avoiding re-entrant state corruption, and ensuring cross-thread triggers properly queue tasks onto the event loop. Browser engines must maintain well-defined state transitions under synchronous re-entry regardless of whether the JavaScript callback was authored by a human or an LLM.

Where the principle surfaces in developer-facing API behavior, it offers helpful guardrails for common agent failure modes alongside a minor feedback-loop trade-off. LLM coding agents routinely write local, defensive event handlers—such as calling cleanup or `abort()` helpers inside listeners—without tracing global synchronous call graphs across modules. Guarded idempotent operations (`AbortController.abort()`) safely absorb redundant re-entrant calls without blowing the call stack. Furthermore, the principle's guidance on synchronous state inspection versus snapshotting state onto deferred `Event` subclasses (like `ProgressEvent.loaded` and `total`) protects agents from subtle asynchronous race conditions when reading `event.target` inside queued callbacks.

However, the principle's advice to make recursive calls "simply return immediately" and its caution against throwing exceptions in early termination can cut against agent feedback loops if applied to non-idempotent methods. While silent early return is ideal for idempotent state transitions like `abort()`, a silent no-op when an agent accidentally re-invokes an active multi-step operation from inside an event handler hides a broken control-flow loop. Coding agents iterate fastest when invalid re-entrant calls fail loudly via explicit state-machine rejections (such as `PaymentRequest.show()` rejecting with `InvalidStateError` based on its guarded `[[state]]` slot).

## Value as a Slide Example

This principle is a weak candidate (`2/5`) for a headline TPAC slide because it is largely an internal spec-editing guide on synchronous versus queued event dispatch, cross-thread task queuing, and protecting internal spec collections during iteration (`AbortSignal` and `ReadableStreamPipeTo`). Audience members at W3C TPAC will rightly view this as foundational runtime correctness that applies equally to human- and agent-authored web applications.

Its only slide-relevant angle is a secondary nuance: comparing idempotent guards (`AbortController.abort()` safely ignoring repeated calls) with explicit state-machine errors (`PaymentRequest.show()` rejecting with `InvalidStateError`). For coding agents, silent early returns on non-idempotent re-entrancy can mask recursive callback bugs during automated test runs, whereas explicit state machines and snapshotted event payloads (`ProgressEvent`) make state transitions self-describing and loud on misuse. Even so, other principles illustrate loud failure and state clarity much more directly.
