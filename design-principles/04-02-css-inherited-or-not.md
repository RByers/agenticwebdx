---
section: "4.2"
id: "css-inherited-or-not"
title: "Make appropriate choices for whether CSS properties are inherited"
chapter: "4. Cascading Style Sheets (CSS)"
url: "https://w3ctag.github.io/design-principles/#css-inherited-or-not"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Predictable override-versus-additive inheritance rules align with LLM priors and prevent silent visual bugs when agents refactor DOM trees or override descendant styles, though this settled CSS baseline is not a compelling TPAC slide example."
---

# §4.2 Make appropriate choices for whether CSS properties are inherited

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §4.2 css-inherited-or-not — Make appropriate choices for whether CSS properties are inherited: Predictable override-versus-additive inheritance rules align with LLM priors and prevent silent visual bugs when agents refactor DOM trees or override descendant styles, though this settled CSS baseline is not a compelling TPAC slide example.

- **URL:** https://w3ctag.github.io/design-principles/#css-inherited-or-not
- **Chapter:** 4. Cascading Style Sheets (CSS)
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Predictable override-versus-additive inheritance rules align with LLM priors and prevent silent visual bugs when agents refactor DOM trees or override descendant styles, though this settled CSS baseline is not a compelling TPAC slide example.

## Principle Summary

W3C TAG §4.2 provides a clear heuristic for CSS specification authors deciding whether a CSS property should be inherited (`Inherited: yes`) or non-inherited (`Inherited: no`). If setting the property on a descendant element is meant to *override* the effect of setting it on an ancestor (such as `font-size` or `color`), the property should be inherited. Conversely, if setting the property on a descendant creates a separate effect that *adds to* the ancestor's effect (such as `background-image`, `border`, or `padding`), the property should not be inherited.

The principle also identifies two specification "code smells" that reveal when the wrong choice was made: (1) a non-inherited property whose specification must walk up the ancestor chain to inspect ancestor values (indicating it should have been inherited, and potentially hurting engine performance), and (2) an inherited property whose specification must ignore a descendant's value when it matches the parent's value to prevent visual compounding (such as avoiding a partially transparent `background-image` being painted repeatedly on every child element).

## Fit for Coding Agents

This principle is a good fit for AI coding agents because CSS failures are entirely silent in non-visual feedback loops—invalid mental models of how styles propagate down the DOM tree produce no console errors, build failures, or DOM exceptions. When CSS properties cleanly follow the override-versus-additive rule, agents can reliably apply container-level typographic defaults (`font-size`, `line-height`, `color`, `visibility`) and override them locally on specific descendant elements without having to emit repetitive selectors for every leaf node, while also freely inserting wrapper `<div>` or `<span>` elements during refactors without causing box-level properties (`background-image`, `border`, `padding`) to duplicate onto children.

Conversely, the exact "code smells" this principle warns against are notorious sources of LLM hallucinations when historical CSS features deviate from simple override-versus-additive semantics. A classic example is `text-decoration`: it is formally non-inherited (`Inherited: no`), yet the specification propagates an ancestor's underline across descendant text boxes in a way that cannot be overridden simply by setting `text-decoration: none` on a child `<span>`. Coding agents routinely hallucinate `.child { text-decoration: none; }` (or similarly `.child { opacity: 1; }` inside a translucent parent, contrasting with `visibility: visible` inside a `visibility: hidden` parent, which works because `visibility` is genuinely inherited) and assume the visual bug is fixed because no error is reported unless a screenshot/vision loop is active. Adhering strictly to §4.2 when designing new CSS properties avoids creating new pseudo-inherited footguns that trap agents in silent visual failures.

## Value as a Slide Example

Despite aligning well with agent ergonomics, §4.2 is a weak candidate (`neither`, strength 2/5) for a slide at a W3C TPAC session on how web standards should adapt to coding agents. The principle's primary examples (`font-size` vs. `background-image`) are foundational CSS 101 design choices that every specification author already takes for granted, and they apply identically to human developers and AI agents.

While the contrast between clean inheritance (`visibility: visible` overriding `visibility: hidden`) and awkward ancestor-propagation rules (`text-decoration: none` failing to cancel an ancestor's `text-decoration: underline`) is an interesting footnote on how agents struggle with silent visual footguns, §4.2 itself does not point to any actionable shift or tension in how the W3C TAG should design standards for agentic workflows.
