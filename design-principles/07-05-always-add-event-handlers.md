---
section: "7.5"
id: "always-add-event-handlers"
title: "Always add event handler attributes"
chapter: "7. Event Design"
url: "https://w3ctag.github.io/design-principles/#always-add-event-handlers"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Helps coding agents by making event support machine-discoverable in WebIDL/TypeScript and runtime-detectable via `'onfoo' in target`, eliminating silent `addEventListener` blind spots and irregular naming gaps."
---

# §7.5 Always add event handler attributes

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §7.5 always-add-event-handlers — Always add event handler attributes: Helps coding agents by making event support machine-discoverable in WebIDL/TypeScript and runtime-detectable via `'onfoo' in target`, eliminating silent `addEventListener` blind spots and irregular naming gaps.

- **URL:** https://w3ctag.github.io/design-principles/#always-add-event-handlers
- **Chapter:** 7. Event Design
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Helps coding agents by making event support machine-discoverable in WebIDL/TypeScript and runtime-detectable via `'onfoo' in target`, eliminating silent `addEventListener` blind spots and irregular naming gaps.

## Principle Summary

Whenever a specification defines a new event type, it must also define a corresponding `onyourevent` event handler IDL attribute on the relevant `EventTarget` interfaces—and place it on the `GlobalEventHandlers` or `WindowEventHandlers` mixin when handled by HTML/SVG/MathML elements or `Window`.

Even though modern web applications typically attach listeners with `addEventListener()` rather than assigning `element.onyourevent = ...`, the TAG mandates `on*` IDL attributes to preserve platform-wide consistency and to enable feature detection (`'onyourevent' in target`), since `addEventListener('yourevent', fn)` silently accepts arbitrary strings without indicating whether the browser supports the event.

## Fit for Coding Agents

This principle is a good fit for AI coding agents across static type checking, runtime verification, and statistical pattern completion. First, in WebIDL, events described only in prose algorithms are difficult for automated tooling to associate with target interfaces; defining `attribute EventHandler onyourevent;` on `GlobalEventHandlers` or target interfaces is a key signal used by `@webref/idl` and TypeScript's `lib.dom.d.ts` generator to populate `GlobalEventHandlersEventMap`, `HTMLElementEventMap`, and framework JSX event prop types (React, Preact, Solid, Vue). For coding agents operating in a `tsc`/LSP feedback loop, this turns event names from unchecked string literals into statically verified types.

Second, `addEventListener` is one of the web platform's most notorious silent failure modes: if an agent registers an unsupported event or hallucinates an event name, `addEventListener('badname', fn)` succeeds with no error and the listener simply never fires. Consistently exposing `onyourevent` on the target interface enables deterministic runtime feature detection (`'onscrollend' in window`, `'oncommand' in HTMLElement.prototype`) in both production progressive enhancement and agent-written headless browser tests.

Third, LLMs generalize strongly from the convention that every event `foo` has a corresponding `onfoo` property. Historic exceptions to this rule—most notably `DOMContentLoaded` lacking an `ondomcontentloaded` IDL attribute—routinely trip up models that pattern-complete `'ondomcontentloaded' in document` for feature detection or inline handlers. Enforcing "always add event handler attributes" eliminates irregular gaps in the platform surface, with only the minor caveat that agents should still prefer `addEventListener` over `target.onfoo = fn` when attaching listeners in modular code to avoid overwriting existing handlers.

## Value as a Slide Example

Although §7.5 genuinely helps coding agents via WebIDL-to-TypeScript generation and runtime feature detection, it rates as a 2/5 (`neither`) for a TPAC slide example. It is largely a narrow, mechanical corollary of §2.6 ("New features should be detectable") combined with WebIDL mixin hygiene (`GlobalEventHandlers` vs. `WindowEventHandlers`).

Putting "Always add `on*` event handler attributes" on a headline slide risks sidetracking a TPAC audience into debating legacy `el.onclick = fn` property assignment versus `addEventListener`, when the real agent-DX takeaways—avoiding silent no-ops in `addEventListener('unknown')`, eliminating irregular naming exceptions like missing `ondomcontentloaded`, and ensuring capabilities are declared in machine-readable WebIDL rather than just spec prose—are better anchored by higher-level principles.
