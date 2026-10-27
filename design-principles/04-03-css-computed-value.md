---
section: "4.3"
id: "css-computed-value"
title: "Choose the computed value type based on how the property should inherit"
chapter: "4. Cascading Style Sheets (CSS)"
url: "https://w3ctag.github.io/design-principles/#css-computed-value"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Designing CSS computed values so inherited properties adapt to child context prevents silent visual overlap bugs that text-based coding agents cannot detect without visual rendering feedback, though the principle is primarily internal CSS spec hygiene."
---

# §4.3 Choose the computed value type based on how the property should inherit

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §4.3 css-computed-value — Choose the computed value type based on how the property should inherit: Designing CSS computed values so inherited properties adapt to child context prevents silent visual overlap bugs that text-based coding agents cannot detect without visual rendering feedback, though the principle is primarily internal CSS spec hygiene.

- **URL:** https://w3ctag.github.io/design-principles/#css-computed-value
- **Chapter:** 4. Cascading Style Sheets (CSS)
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Designing CSS computed values so inherited properties adapt to child context prevents silent visual overlap bugs that text-based coding agents cannot detect without visual rendering feedback, though the principle is primarily internal CSS spec hygiene.

## Principle Summary

In CSS, inheritance passes a parent element's *computed value* to its children, whereas processing steps that happen after the computed value stage (to produce the *used value*) are evaluated per element and are not inherited. This principle instructs CSS specification authors to choose what representation a property resolves to at computed-value time based on how it should behave when inherited into descendant elements that have different local context (such as a different `font-size`).

The classic example is `line-height`. When specified as a unitless `<number>` like `line-height: 1.4` on a `<body>` with `font-size: 20px`, its computed value remains the number `1.4` while its used value on body text becomes `28px`. A child `<h2>` with `font-size: 200%` (`40px`) inherits the computed number `1.4` and computes its own used `line-height` of `56px` so the larger font does not overflow. By contrast, when `line-height` is specified as a `<length>` or `<percentage>` (like `28px`, `1.4em`, or `140%`), it resolves to `28px` at computed-value time, causing child headings to inherit a fixed `28px` line height that clips or overlaps larger text.

## Fit for Coding Agents

This principle aligns well with the ergonomics and failure modes of AI coding agents (`good`), primarily because flawed CSS inheritance causes silent visual regressions rather than loud, machine-checkable errors. When an inherited property resolves prematurely to an absolute pixel length at the parent level instead of preserving a scale factor or contextual keyword, the browser does not throw an exception, log a console warning, or fail a DOM assertion. Unless the agent is running an expensive multimodal screenshot loop and happens to trigger multi-line wrapping on a child element, text clipping or vertical overlap goes completely undetected.

Furthermore, coding agents routinely generate and refactor UI components in modular slices—authoring typography or spacing defaults on a layout container while generating nested components in separate files or turns without full visibility into every ancestor's exact `font-size`. When CSS properties inherit context-adaptive computed values (such as unitless `<number>` multipliers), a single declaration on a parent container composes safely across arbitrary component subtrees. This improves token efficiency and avoids forcing agents to defensively redeclare properties like `line-height` on every heading or child component.

Finally, the historical inconsistency illustrated by `line-height`—where unitless `1.4` computes to a `<number>` that inherits cleanly, whereas `1.4em` and `140%` compute to a fixed pixel `<length>` that breaks descendant headings—shows why consistent computed-value design matters for agents. Even though LLM training priors strongly favor unitless `line-height` values (or utility classes like Tailwind's `leading-*`), agents debugging layout bugs programmatically via `getComputedStyle(el).lineHeight` can still be misled by the legacy CSSOM behavior where `getComputedStyle` returns the used pixel value ("resolved value") rather than the spec's computed `<number>`, hiding the underlying inheritance mechanism from DOM inspection scripts.

## Value as a Slide Example

This principle is `neither` a strong "clearly-useful" nor "clearly-harmful" headline slide example for a TPAC session on how web standards should adapt for coding agents (`example_strength: 2`). While the `line-height: 1.4` versus `1.4em` (`28px`) contrast is a concrete illustration of how premature value resolution creates silent visual overlap bugs that text-based agents cannot catch without visual rendering feedback, the principle is fundamentally internal CSS specification hygiene for defining cascade value stages. Because human developers and AI coding agents benefit from composable inheritance in the exact same way, it does not highlight a novel divergence between human DX and agentic DX.
