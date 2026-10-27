---
section: "4.4"
id: "css-naming"
title: "Name CSS properties and values appropriately"
chapter: "4. Cascading Style Sheets (CSS)"
url: "https://w3ctag.github.io/design-principles/#css-naming"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Morphological and lexical regularity in CSS property and value names directly reduces near-miss token hallucinations—which is especially critical in CSS because unrecognized declarations fail silently."
---

# §4.4 Name CSS properties and values appropriately

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §4.4 css-naming — Name CSS properties and values appropriately: Morphological and lexical regularity in CSS property and value names directly reduces near-miss token hallucinations—which is especially critical in CSS because unrecognized declarations fail silently.

- **URL:** https://w3ctag.github.io/design-principles/#css-naming
- **Chapter:** 4. Cascading Style Sheets (CSS)
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Morphological and lexical regularity in CSS property and value names directly reduces near-miss token hallucinations—which is especially critical in CSS because unrecognized declarations fail silently.

## Principle Summary

W3C TAG Design Principle §4.4 ("Name CSS properties and values appropriately") specifies grammatical and lexical rules for CSS identifiers: property names should be nouns and values should usually be adjectives (or nouns); words should be separated by hyphens without abbreviations; root words should be preferred over inflected forms with prefixes or suffixes (e.g., `size` rather than `sizing`); values should be extensible keywords rather than boolean-like terms (`yes`, `no`, `true`, `false`); and redundant meta-words like `mode` or `state` should be omitted from property names.

For human authors and spec editors, these conventions reduce the cognitive load of remembering exact spelling across hundreds of CSS properties and ensure forward-compatible extensibility so new keyword values can be added to a property over time without breaking existing stylesheets or outgrowing a boolean toggle.

## Fit for Coding Agents

This principle is a good fit for AI coding agents because LLMs generate identifiers autoregressively from statistical and morphological regularities across a language corpus. When CSS properties consistently use hyphenated, unabbreviated root nouns without arbitrary suffixes like `-ing`, `-mode`, or `-state`, coding agents can accurately recall or zero-shot predict property names even for newer specifications with limited training-data coverage. Conversely, historical deviations from this principle create persistent near-miss hallucination traps: for instance, most sizing properties use the root word (`inline-size`, `block-size`, `font-size`, `background-size`), whereas `box-sizing` and `field-sizing` use `-sizing`; similarly, most properties omit `-mode` or `-state`, but `writing-mode`, `mix-blend-mode`, `animation-fill-mode`, and `animation-play-state` require them, inviting agents to guess `field-size` or `animation-play-mode`.

Naming regularity is especially critical for coding agents in CSS because of how it interacts with the agent feedback loop: CSS fails silently by design. In JavaScript or TypeScript, a hallucinated method name or boolean argument immediately produces a loud `TypeError` at runtime or a `tsc` diagnostic, giving the agent an actionable signal to self-correct. In CSS, forward-compatible parsing rules cause the browser to silently discard unrecognized properties or values (`field-size: content` or `blend-mode: multiply`) without throwing errors. Unless the agent runs a strict CSS linter or catches the visual discrepancy via screenshot inspection, a morphological near-miss becomes a silent bug.

Finally, the rule against `true`/`false`/`yes`/`no` values in favor of extensible semantic keywords (`none`, `auto`, `fixed`, `content`, `contain`) aligns with CSS-wide priors in the model's weights and makes CSS declarations self-describing in context. Reading or generating `field-sizing: content` vs. `field-sizing: fixed` explicitly encodes the layout behavior at the point of use without requiring the agent to look up what a boolean flag toggles.

## Value as a Slide Example

§4.4 is a solid supporting example (3/5, `clearly-useful`), particularly valuable when addressing CSS Working Group participants or as a concrete CSS case study alongside §12 (Naming principles). Its strongest hook on a slide is pairing CSS's morphological exceptions (`inline-size` and `font-size` vs. `box-sizing` and `field-sizing`; `isolation` vs. `mix-blend-mode` and `animation-play-state`) with CSS's silent failure model.

While not a standalone 5/5 thesis slide on its own, it vividly illustrates a key insight for spec authors: whereas a minor naming irregularity in a JS API is caught immediately by TypeScript or a runtime `TypeError`, a near-miss hallucination in CSS (`field-size: content` or `animation-play-mode: paused`) is silently ignored by the parser, making strict adherence to root-word naming conventions much higher-leverage for agent reliability than it might first appear.
