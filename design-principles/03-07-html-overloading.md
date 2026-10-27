---
section: "3.7"
id: "html-overloading"
title: "Give each HTML element a single purpose"
chapter: "3. HTML"
url: "https://w3ctag.github.io/design-principles/#html-overloading"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Dedicated single-purpose elements give coding agents 1:1 tag-to-type mappings in HTMLElementTagNameMap and prevent cross-mode attribute hallucinations and CSS selector collisions common on overloaded elements like <input>."
---

# §3.7 Give each HTML element a single purpose

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §3.7 html-overloading — Give each HTML element a single purpose: Dedicated single-purpose elements give coding agents 1:1 tag-to-type mappings in HTMLElementTagNameMap and prevent cross-mode attribute hallucinations and CSS selector collisions common on overloaded elements like <input>.

- **URL:** https://w3ctag.github.io/design-principles/#html-overloading
- **Chapter:** 3. HTML
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Dedicated single-purpose elements give coding agents 1:1 tag-to-type mappings in HTMLElementTagNameMap and prevent cross-mode attribute hallucinations and CSS selector collisions common on overloaded elements like <input>.

## Principle Summary

W3C TAG Design Principle §3.7 ("Give each HTML element a single purpose") states that each HTML element should have a single, clear purpose. While HTML attributes can modify or refine an element's semantics, they should not switch an element into a fundamentally different operating mode. Rather than overloading one element to operate in multiple distinct modes via attributes, defining a separate element for each mode is preferable (while avoiding extreme overspecialization).

This principle reflects lessons learned from heavily overloaded legacy HTML elements such as `<input type="...">` (which spans text inputs, checkboxes, file uploaders, date pickers, color pickers, range sliders, and buttons), `<link rel="...">`, `<meta>`, and `<object>`, in favor of dedicated elements like `<dialog>`, `<progress>`, `<meter>`, `<output>`, `<video>`, and `<audio>`.

## Fit for Coding Agents

This principle is a strong positive fit (`good`) for AI coding agents because the HTML tag name serves as the primary structural and type anchor across both the LLM's token stream and the verification toolchain (TypeScript, Web IDL, JSX, and CSS). First, in Web IDL and TypeScript's DOM type definitions (`HTMLElementTagNameMap`), element interfaces are keyed by tag name (`document.querySelector('dialog')` returns `HTMLDialogElement`). When an element is overloaded across radically different modes via an attribute—most notably `<input type="...">`—every mode collapses into a single monolithic `HTMLInputElement` interface containing the union of all modes' properties (`checked`, `files`, `valueAsNumber`, `valueAsDate`, `src`, `alt`, `indeterminate`, `multiple`). If an agent accesses `input.files` on a text input or uses mode-mismatched properties, TypeScript cannot catch the error at compile time, and the browser fails silently at runtime. Dedicated elements (`<progress>`, `<meter>`, `<dialog>`, `<textarea>`, `<select>`) give the agent loop strict, 1:1 mode-specific static type checking.

Second, single-purpose elements prevent cross-mode attribute bleed in LLM token generation. Autoregressive models condition heavily on the opening tag token (`<input`, `<link`, `<dialog`). When a single tag operates in many incompatible modes, attribute co-occurrence priors from one mode bleed into others. A classic, pervasive LLM hallucination is writing `<input type="number" maxlength="5">` or confusing `value`, `checked`, `pattern`, and `size` across `<input>` modes—mistakes that HTML parsers silently ignore. Similarly, `<link rel="...">` overloading (`preload` vs. `stylesheet` vs. `icon`) frequently leads agents to omit mode-required attributes like `as="..."` or misconfigure `crossorigin`.

Third, dedicated tag names prevent CSS selector and DOM query collisions. Coding agents routinely generate tag-level CSS rules like `input { width: 100%; padding: 8px; }` when styling forms, inadvertently breaking checkboxes (`type="checkbox"`), radio buttons (`type="radio"`), range sliders (`type="range"`), or color pickers (`type="color"`). Giving distinct widgets their own tag names (`<select>`, `<textarea>`, `<button>`, `<dialog>`, `<progress>`) isolates styling, closing tags, and DOM queries without requiring verbose compound attribute exclusions (`input:not([type="checkbox"])...`).

## Value as a Slide Example

This principle is a strong, concrete `clearly-useful` candidate for a TPAC slide (4/5) because the contrast between overloaded legacy elements (`<input type="...">`, `<link rel="...">`) and single-purpose modern elements (`<dialog>`, `<progress>`, `<video>`, `<select>`) is immediately recognizable to any W3C audience.

On a slide, it demonstrates how a principle originally stated as a vague human convenience ("simplifies usage for authors") has a rigorous, mechanical justification for coding agents: tag names drive `HTMLElementTagNameMap` in TypeScript (`<dialog>` -> `HTMLDialogElement`), whereas attribute-switched modes on `<input>` collapse into a single untyped `HTMLInputElement` bag and induce silent cross-mode hallucinations like `<input type="number" maxlength="4">` and `input { width: 100% }` CSS collisions.
