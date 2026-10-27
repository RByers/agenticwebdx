---
section: "4.1"
id: "css-property-separation"
title: "Separate CSS properties based on what should cascade separately"
chapter: "4. Cascading Style Sheets (CSS)"
url: "https://w3ctag.github.io/design-principles/#css-property-separation"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Separating independent CSS concerns into distinct properties prevents coding agents making localized edits from silently clobbering unrelated styles in the cascade."
---

# §4.1 Separate CSS properties based on what should cascade separately

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §4.1 css-property-separation — Separate CSS properties based on what should cascade separately: Separating independent CSS concerns into distinct properties prevents coding agents making localized edits from silently clobbering unrelated styles in the cascade.

- **URL:** https://w3ctag.github.io/design-principles/#css-property-separation
- **Chapter:** 4. Cascading Style Sheets (CSS)
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Separating independent CSS concerns into distinct properties prevents coding agents making localized edits from silently clobbering unrelated styles in the cascade.

## Principle Summary

In CSS, the property is the fundamental unit of the cascade: when a rule with higher specificity or later source order declares a property, it completely replaces any earlier value for that entire property. This principle advises spec authors to group values into a single CSS property only when those values are tightly coupled and must be overridden together as an atomic unit, and to split values into separate properties whenever authors need to set or override them independently across different rules, states, or stylesheets.

For example, in drop-cap styling, the size of the initial letter and how many lines it sinks (`initial-letter: 3 2`) are coupled—overriding the size to `2` while inheriting a sink of `3` from another rule produces broken layout, so they belong in one property. Conversely, `initial-letter-align` is a document-wide or script-level typographic policy that should persist even when individual components override their drop-cap size, so it belongs in a separate property. Better-known platform examples of this principle in action include splitting individual transform properties (`translate`, `rotate`, `scale`) out from the monolithic `transform` list, and splitting `font-variant-*` longhands out from `font-feature-settings`.

## Fit for Coding Agents

This principle is a strong positive fit (`good`) for AI coding agents because agents routinely operate with localized context and struggle with silent cross-rule clobbering. When a user asks an agent to "add a subtle scale-up on hover" or "enable tabular numbers on this table cell," the agent often edits a single selector, component, or utility class without inspecting every base rule, parent stylesheet, or media query that also targets the element. When independent visual axes are packed into a single property—such as `transform` or `font-feature-settings`—writing `.card:hover { transform: scale(1.05); }` silently wipes out a base `.card { transform: translateX(-50%); }` positioning rule. Worse, because CSS property overrides are valid by definition, the browser emits no console error or warning; unless the agent is running a visual screenshot loop and catches the layout shift, the regression ships silently.

Separating independent concerns into distinct properties (`scale: 1.05` alongside `translate: -50% 0`, or `font-variant-numeric: tabular-nums` alongside `font-variant-ligatures`) makes CSS edits compositional and local. It also aligns directly with how LLMs generate modern styles: agents heavily favor atomic utility classes (like Tailwind) and modular state overrides where each class or selector controls one orthogonal property. Without property separation in the underlying platform, frameworks and agents must invent complex CSS custom-property glue (such as composing `--tw-translate-x`, `--tw-rotate`, and `--tw-scale` inside a shared `transform` template) just to simulate independent cascading.

At the same time, the converse half of the principle—keeping genuinely interdependent values together in a single property like `initial-letter`—also helps agents. When two parameters only make sense in coordinated pairs, forcing them into one declaration ensures that an agent overriding a rule in a localized edit must supply a coherent complete state rather than updating one half of a coupled pair and leaving a dangling, incompatible value from a lower-specificity rule.

## Value as a Slide Example

This principle is a strong candidate (`clearly-useful`, `4/5`) for a TPAC slide illustrating how classic human-centric CSS design principles take on even greater urgency for AI agents working under partial context and non-visual feedback loops. While the TAG document's own `initial-letter` / `initial-letter-align` example is somewhat niche for a general audience, pairing §4.1 with the evolution from monolithic `transform` (or `font-feature-settings`) to independent `translate` / `rotate` / `scale` properties makes an immediately recognizable, high-impact slide.

On a slide, you can show a two-line diff where an agent asked to "scale the modal slightly on open" writes `transform: scale(1.02)` and accidentally destroys the modal's `transform: translate(-50%, -50%)` centering—a classic LLM bug that produces zero console errors—versus `scale: 1.02`, which succeeds locally without needing whole-stylesheet awareness. It cleanly demonstrates that APIs with independent, orthogonal properties reduce the context window required to make safe edits and eliminate silent cascade footguns.
