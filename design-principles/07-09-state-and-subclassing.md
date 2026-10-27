---
section: "7.9"
id: "state-and-subclassing"
title: "Put state on target objects rather than Events"
chapter: "7. Event Design"
url: "https://w3ctag.github.io/design-principles/#state-and-subclassing"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Putting state on the EventTarget rather than bespoke Event subclasses helps coding agents avoid TypeScript event-type hallucinations, write race-free initialization and update logic, and inspect live state synchronously during test/debug loops."
---

# §7.9 Put state on target objects rather than Events

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §7.9 state-and-subclassing — Put state on target objects rather than Events: Putting state on the EventTarget rather than bespoke Event subclasses helps coding agents avoid TypeScript event-type hallucinations, write race-free initialization and update logic, and inspect live state synchronously during test/debug loops.

- **URL:** https://w3ctag.github.io/design-principles/#state-and-subclassing
- **Chapter:** 7. Event Design
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Putting state on the EventTarget rather than bespoke Event subclasses helps coding agents avoid TypeScript event-type hallucinations, write race-free initialization and update logic, and inspect live state synchronously during test/debug loops.

## Principle Summary

W3C TAG Design Principle §7.9 advises API designers to expose current state as properties directly on the `EventTarget` object and use generic events (such as `'change'`) merely to signal that the state has updated, rather than carrying the state exclusively on `Event` objects. New `Event` subclasses should generally be avoided unless needed to describe *how* a transition occurred (such as delta or transition metadata). Where continuously maintaining state on a global or ambient object is prohibitively expensive, the principle recommends returning an `EventTarget` from an async method call (e.g., `const dataUsage = await self.monitorDataUsage()`) that signals active interest before state updates begin.

For human developers and browser engines, this pattern solves a fundamental timing and lifecycle problem: consumers often need to read the current state synchronously during initialization or after a terminal state has already been reached (when no future events will fire). Keeping state on the target object decouples state inspection from event subscription timing and prevents an explosion of one-off `Event` subclasses across the platform.

## Fit for Coding Agents

This principle aligns well with how LLM coding agents generate, type-check, and verify web application code. First, one of the most frequent sources of friction for coding agents working in TypeScript is typing DOM event handlers and remembering bespoke `Event` subclass names and property paths. When an agent extracts a listener function or registers `addEventListener('change', (e) => ...)`, `e` is often typed as the base `Event` interface unless explicitly annotated, and agents routinely hallucinate whether a payload lives on `e.value`, `e.state`, `e.detail.value`, or requires casting to a specialized `FooChangeEvent` subclass. When state lives directly on the `EventTarget` already in lexical scope (such as `dataUsage.bytesReceived`, `AbortSignal.aborted`, `document.visibilityState`, or `HTMLInputElement.value`), the agent accesses a strongly typed property on an object reference it already holds, and any typo is caught immediately as a loud compile-time TypeScript error.

Second, putting state on the target eliminates a class of subtle asynchronous race conditions and stateful glue code that agents frequently struggle with. When state is only delivered inside event payloads (as in older APIs like `DeviceOrientationEvent` or observer entry callbacks), an agent must generate boilerplate to cache the latest value in a mutable closure variable (`let latestState = ...`) and handle the period before the first event arrives—or risk missing an initial/terminal transition if the listener was registered asynchronously (for example, inside a dynamically imported module or React `useEffect`). When state is on the target, agents can write a single idempotent synchronization function (`function sync() { render(target.state); }`) and invoke it both synchronously at setup and inside the `'change'` listener.

Third, synchronous state properties on target objects dramatically improve the agentic verification and debugging feedback loop. Coding agents driving headless browsers via Playwright, WebDriver, or DevTools MCP tools routinely inspect application and platform state using one-shot `page.evaluate(...)` calls. A property on a target object (`navigator.onLine`, `permissionStatus.state`, `video.readyState`, `dialog.open`) can be queried directly at any point in a test assertion without requiring the agent to inject event listeners into the page prior to the action being tested.

## Value as a Slide Example

This principle is a `clearly-useful` supporting example (`3/5` strength) for a TPAC slide showing where existing TAG ergonomics rules naturally reinforce agentic DX. It illustrates a concrete overlap between human cognitive ergonomics and agent reliability: reducing vocabulary proliferation (fewer bespoke `Event` subclasses to memorize or hallucinate in TypeScript) and making state synchronously inspectable at any point in time rather than trapped in transient event callbacks.

While it is more tactical than macro-level architectural principles (and thus better suited as a concise bullet point or code comparison rather than a standalone headline slide), contrasting `AbortSignal.aborted` / `PermissionStatus.state` / `input.value` against event-only payload APIs provides a crisp, relatable example for standards authors of how keeping state on `EventTarget` helps both TypeScript typecheckers and Playwright-based agent verification loops.
