---
section: "7.3"
id: "promises-and-events"
title: "Events should fire before related Promises resolve"
chapter: "7. Event Design"
url: "https://w3ctag.github.io/design-principles/#promises-and-events"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Helps coding agents by ensuring `await` acts as a deterministic barrier after all synchronous event listeners have completed, preventing obscure multi-listener microtask interleaving bugs, though it is too low-level and non-differentiating between human and agent DX to feature on a slide."
---

# §7.3 Events should fire before related Promises resolve

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §7.3 promises-and-events — Events should fire before related Promises resolve: Helps coding agents by ensuring `await` acts as a deterministic barrier after all synchronous event listeners have completed, preventing obscure multi-listener microtask interleaving bugs, though it is too low-level and non-differentiating between human and agent DX to feature on a slide.

- **URL:** https://w3ctag.github.io/design-principles/#promises-and-events
- **Chapter:** 7. Event Design
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Helps coding agents by ensuring `await` acts as a deterministic barrier after all synchronous event listeners have completed, preventing obscure multi-listener microtask interleaving bugs, though it is too low-level and non-differentiating between human and agent DX to feature on a slide.

## Principle Summary

Section 7.3 ("Events should fire before related Promises resolve") states that when a Promise-based asynchronous algorithm also dispatches DOM events, it must dispatch the events before resolving the Promise.

This principle exists because of how the HTML event loop processes microtasks during native event dispatch. Resolving a Promise queues a microtask, and microtasks run whenever the JavaScript execution stack becomes empty. When the browser dispatches an event from native code with no JavaScript on the stack, the JS stack empties after each individual event listener finishes. If a Promise is resolved before the related event is dispatched, its reaction microtask will execute right after the first event listener returns—interleaving between the first and second listeners of the same event. Dispatching the event first ensures all event listeners run to completion before any Promise reaction callbacks execute.

## Fit for Coding Agents

This principle is a good fit for AI coding agents because it preserves the intuitive, linear invariant that `await operation()` means the operation—and all of its synchronous event notifications—have completely finished. LLM coding agents heavily favor sequential `async`/`await` control flow and routinely write application logic and automated tests that `await` a Promise-returning API (such as `await video.play()` or `await animation.finished`) and immediately read or assert on state mutated by event listeners. Because events fire before the related Promise resolves, `await` acts as a reliable, deterministic synchronization barrier without requiring extra microtask or macrotask flushing.

Crucially, this principle also prevents a non-local failure mode that is particularly toxic to an agent's reasoning and debugging loop. When a specification resolves a Promise before dispatching an event, code with only a *single* event listener still runs that listener before the Promise microtask, appearing to work normally. The bug only manifests when a *second* listener is attached to the same target—for instance, when an agent attaches a test spy, analytics listener, or framework hook alongside an existing listener—causing the JS stack to empty after the first listener and the `await` continuation to interleave between Listener 1 and Listener 2. Because the second listener often resides outside the local function or file in the agent's context window, diagnosing why state is only partially updated after `await` is remarkably difficult for an LLM, which will typically respond by cargo-culting `await Promise.resolve()` or `setTimeout` workarounds rather than identifying the microtask checkpoint interleaving.

## Value as a Slide Example

Although this principle helps coding agents by guaranteeing deterministic ordering between event listeners and `await` continuations, it is a weak candidate for a TPAC slide (`neither`, 2/5). It is a low-level spec-authoring rule about HTML event loop and microtask checkpoint mechanics that applies identically to human developers and AI agents. Explaining the C++ JS-stack-emptying behavior between event listeners on a slide would take too much setup for a point that does not highlight any divergence between human DX and agent DX or suggest any new direction for how web standards should adapt to agents.
