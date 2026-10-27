---
section: "7.7"
id: "events-are-for-notification"
title: "Use events for notification"
chapter: "7. Event Design"
url: "https://w3ctag.github.io/design-principles/#events-are-for-notification"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Separating imperative state-changing methods from post-facto notification events aligns well with agent priors and avoids magic side effects, though it is too settled and minor to be a headline TPAC slide example."
---

# §7.7 Use events for notification

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §7.7 events-are-for-notification — Use events for notification: Separating imperative state-changing methods from post-facto notification events aligns well with agent priors and avoids magic side effects, though it is too settled and minor to be a headline TPAC slide example.

- **URL:** https://w3ctag.github.io/design-principles/#events-are-for-notification
- **Chapter:** 7. Event Design
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Separating imperative state-changing methods from post-facto notification events aligns well with agent priors and avoids magic side effects, though it is too settled and minor to be a headline TPAC slide example.

## Principle Summary

W3C TAG Design Principle §7.7 states that DOM events should only deliver a notification that a state change has already occurred, rather than serving as the mechanism that causes or triggers the change. Using the `resize` event as its canonical example, the principle notes that authors cannot prevent a window resize by intercepting the `resize` event, nor can they cause the browser window to change size by constructing and dispatching a synthetic `resize` event (`window.dispatchEvent(new Event('resize'))`).

For human developers and browser engines, this principle establishes a clean architectural boundary between commands (imperative APIs like `window.resizeTo()`, `dialog.showModal()`, or `el.showPopover()` that request a state transition) and notifications (events fired after a transition completes so observers can synchronize state). It also aligns with the browser's asynchronous rendering and multi-process architecture, where external changes like viewport resizing have already taken effect in the windowing system or compositor before script on the main thread is notified.

## Fit for Coding Agents

This principle is a good fit for AI coding agents because it enforces a strict separation between imperative mutations and reactive notifications—a pattern that matches dominant software engineering priors across languages and makes control flow locally legible inside a context window. When web APIs adhere to §7.7, state changes are exposed as explicit, discoverable methods or property setters (such as `details.open = true` or `el.showPopover()`) rather than overloaded event dispatch. Crucially for an agent's self-correction loop, imperative methods can return Promises or throw descriptive `DOMException`s when called in an invalid state, whereas `target.dispatchEvent(...)` only returns a boolean (`!event.defaultPrevented`) and gives no error feedback when an operation fails to mutate browser state.

At the same time, the reason this principle is so relevant to agent behavior is that LLM coding agents—especially when generating UI tests or browser automation scripts—frequently hallucinate the exact anti-pattern §7.7 warns against. Agents routinely write code such as `input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }))` expecting a form to submit or an input's value to update, or call `event.preventDefault()` inside a `resize`, `scroll`, or `input` listener expecting to block the change. Because the DOM shares a single `Event` interface across both cancelable pre-action hooks (`click`, `submit`, `beforeinput`, `beforetoggle`) and non-cancelable post-facto notifications (`input`, `toggle`, `resize`, `scroll`), both synthetic `dispatchEvent()` calls and `preventDefault()` calls on notification events become silent no-ops. While §7.7 keeps new specs from making this worse by banning event-triggered mutations, agents still suffer when existing APIs fail silently rather than loudly signaling that a notification event cannot be canceled or synthetically dispatched to cause a native state change.

## Value as a Slide Example

As a standalone rule, §7.7 is rated `neither` (2/5) for a headline TPAC slide because no modern web specification proposes using synthetic event dispatch to trigger browser actions; the principle is uncontroversial baseline hygiene.

However, the agent failure mode adjacent to §7.7 makes a useful supporting anecdote if the talk discusses silent failures in the DOM event model: coding agents constantly confuse cancelable pre-action events (`beforetoggle`, `beforeinput`, `submit`) with post-facto notification events (`toggle`, `input`, `resize`), and they frequently attempt to drive UI state in tests via `dispatchEvent(new KeyboardEvent(...))`. Because `event.preventDefault()` on a non-cancelable notification event (`event.cancelable === false`) and untrusted `dispatchEvent()` calls silently do nothing without throwing or logging a clear diagnostic, agents can waste multiple turns debugging why their event listener or test harness had no effect.
