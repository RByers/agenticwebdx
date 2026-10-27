---
section: "6.5"
id: "prefer-dictionaries"
title: "Accept optional and/or primitive arguments through dictionaries"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#prefer-dictionaries"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 5
verdict: "Named dictionary arguments strongly benefit coding agents by making call sites self-describing in context and eliminating positional argument counting and boolean-trap errors, though Web IDL's silent ignoring of unknown dictionary keys means misspelled property names fail silently at runtime without TypeScript."
---

# §6.5 Accept optional and/or primitive arguments through dictionaries

GREP_SUMMARY: slide_example=clearly-useful | strength=5/5 | agent_fit=good | §6.5 prefer-dictionaries — Accept optional and/or primitive arguments through dictionaries: Named dictionary arguments strongly benefit coding agents by making call sites self-describing in context and eliminating positional argument counting and boolean-trap errors, though Web IDL's silent ignoring of unknown dictionary keys means misspelled property names fail silently at runtime without TypeScript.

- **URL:** https://w3ctag.github.io/design-principles/#prefer-dictionaries
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 5/5
- **Verdict:** Named dictionary arguments strongly benefit coding agents by making call sites self-describing in context and eliminating positional argument counting and boolean-trap errors, though Web IDL's silent ignoring of unknown dictionary keys means misspelled property names fail silently at runtime without TypeScript.

## Principle Summary

W3C TAG Design Principle §6.5 advises web specification authors to accept optional arguments—and even mandatory parameters when they are primitive types like booleans or numbers—through an options dictionary rather than a sequence of positional arguments, while making the dictionary argument itself optional when defaults suffice. It contrasts self-documenting dictionary calls like `new Event("example", { bubbles: true, cancelable: false })` and `window.scrollBy({ left: 50, top: 0 })` against positional equivalents like `new Event("example", true, false)`, `window.scrollBy(50, 0)`, and `element.scrollIntoView(false)`.

For human developers and browser standards evolution, this principle solves three longstanding problems: it prevents the "Boolean Trap" where bare `true`/`false` arguments at a call site are opaque to readers; it spares authors from memorizing strict parameter ordering or passing `undefined` placeholders to reach later options; and it gives spec authors a clean extensibility path to add new options in the future without combinatorial method overloads or breaking existing positional signatures.

## Fit for Coding Agents

This principle is a strong, positive fit (`good`) for LLM coding agents both when reading existing code and when generating or editing API calls. Autoregressive language models operate over token sequences where local semantic context matters heavily. Positional primitive signatures—such as legacy `event.initMouseEvent(...)` with 15 positional parameters, `ctx.drawImage(...)` with 3-, 5-, or 9-number overloads, or `element.scrollIntoView(false)` where `false` counter-intuitively means `alignToTop: false`—are classic failure modes for agents. When generating positional calls, models frequently transpose adjacent numeric coordinates (e.g., swapping `left`/`top` or source/destination rectangles), miscount `undefined` padding slots, or invert bare boolean flags. When reading code in a context window, a dictionary call like `element.scrollIntoView({ behavior: "smooth", block: "end" })` or `addEventListener("click", handler, { once: true, passive: true, signal })` embeds the schema directly at the call site, removing ambiguity during refactoring and code review.

Dictionaries also make incremental, multi-turn code edits far more reliable for agents. A follow-up user prompt such as "make this event listener run only once and cancel on abort" only requires the agent to insert `once: true, signal` into an existing options object, rather than converting a legacy positional boolean (`addEventListener("click", fn, true)`) into a dictionary (`{ capture: true, once: true, signal }`) or shifting positional indices. Even though property names add a few extra tokens compared to bare primitives, those tokens act as semantic anchors that substantially reduce logic bugs.

However, there is an important agent-specific caveat rooted in Web IDL mechanics: Web IDL dictionaries silently ignore unknown keys at runtime to preserve forward and backward compatibility across browser versions. Whereas a human developer primarily struggles to remember argument order, an LLM sometimes hallucinates plausible property names from adjacent APIs or orthographic variants—such as passing `{ cancellable: false }` (with two `l`s) instead of `{ cancelable: false }`, or `{ smooth: true }` instead of `{ behavior: "smooth" }`. In a TypeScript project with `lib.dom.d.ts`, excess-property checking catches these mistakes immediately in the compiler feedback loop; in untyped JavaScript, however, the browser silently drops the misspelled key and falls back to the default value without throwing an error. Even with that caveat, dictionaries remain strictly superior to positional primitives for agent-authored code.

## Value as a Slide Example

§6.5 is a strong candidate (`clearly-useful`, 4/5) for a TPAC slide illustrating how good human ergonomics and good agent ergonomics strongly align on self-describing syntax at the call site, while also surfacing a subtle Web IDL twist worth discussing with spec authors. Everyone in a W3C audience immediately recognizes the contrast between `element.scrollIntoView(false)` or `new Event("x", true, false)` and `element.scrollIntoView({ behavior: "smooth", block: "nearest" })` or `new Event("x", { bubbles: true, cancelable: false })`.

On a slide, this principle lets the presenter make two crisp points: first, LLMs are bad at counting positional `undefined` placeholders and disambiguating bare booleans or coordinate pairs (`scrollBy(50, 0)` vs `scrollBy({ left: 50, top: 0 })`), but excel when key-value pairs explicitly label intent in the token stream and allow additive local edits; second, whereas humans needed dictionaries because they couldn't memorize parameter order, agents sometimes hallucinate a dictionary key name (e.g., `cancellable` with two `l`s), which Web IDL silently ignores at runtime—highlighting why machine-checkable schemas (`lib.dom.d.ts`) or dev-mode warnings for unknown dictionary keys matter for agent feedback loops.
