---
section: "3.2"
id: "html-lists"
title: "Use space-separated attributes for short lists of values, separate elements for longer lists"
chapter: "3. HTML"
url: "https://w3ctag.github.io/design-principles/#html-lists"
agent_fit: "mixed"
slide_example: "clearly-harmful"
example_strength: 3
verdict: "Space-separated DOMTokenList attributes and child elements work well for agents, but framing the tradeoff around list length and human verbosity rather than flat tokens vs. structured microsyntaxes misses what actually trips up LLMs."
---

# §3.2 Use space-separated attributes for short lists of values, separate elements for longer lists

GREP_SUMMARY: slide_example=clearly-harmful | strength=3/5 | agent_fit=mixed | §3.2 html-lists — Use space-separated attributes for short lists of values, separate elements for longer lists: Space-separated DOMTokenList attributes and child elements work well for agents, but framing the tradeoff around list length and human verbosity rather than flat tokens vs. structured microsyntaxes misses what actually trips up LLMs.

- **URL:** https://w3ctag.github.io/design-principles/#html-lists
- **Chapter:** 3. HTML
- **Agent-Fit:** mixed
- **Slide-Example:** clearly-harmful
- **Example-Strength:** 3/5
- **Verdict:** Space-separated DOMTokenList attributes and child elements work well for agents, but framing the tradeoff around list length and human verbosity rather than flat tokens vs. structured microsyntaxes misses what actually trips up LLMs.

## Principle Summary

This principle advises web specification authors to represent short lists of element metadata as space-separated attribute strings backed by a `DOMTokenList` reflection (such as `element.classList` for `class` or `iframe.sandbox` for `sandbox`), while allowing other delimiters when platform consistency demands it (such as comma-separated values in `<input accept>` to match the HTTP `Accept` header).

For longer lists or items that carry their own metadata, the principle discourages packing the list into a single attribute. Instead, it recommends representing items as separate elements—either direct children (such as `<option>` inside `<select>` or `<source>` inside `<video>`) or external elements linked via an attribute (such as `<datalist>` referenced by `<input list="...">`). It notes `<img srcset>` as a rare exception where a comma-separated microsyntax was chosen because `<img>` is a void element and to avoid the verbosity of child elements.

## Fit for Coding Agents

The baseline pattern recommended by this principle—space-separated `DOMTokenList` attributes for simple token sets and child elements for structured items—aligns well with coding agents. Space-separated token lists map naturally to BPE whitespace tokenization and have massive training-data priors (`class`, `rel`, `sandbox`, `part`, `blocking`). Exposing them as `DOMTokenList` with `.add()`, `.remove()`, `.toggle()`, and `.contains()` prevents agents from writing buggy string-splitting or regex glue code to mutate attribute lists at runtime. Similarly, using child elements like `<source>` or `<option>` gives each item explicit named attributes and clean line-by-line boundaries for surgical file-editing tools (`edit_file` / unified diffs).

However, the principle's framing around list length and human verbosity—along with its carve-outs—cuts against agent ergonomics in three ways. First, structure matters to agents, not list length or verbosity: coding agents have no trouble generating or editing long flat space-separated attributes (such as 25 Tailwind utility classes in `class`) or verbose `<picture>`/`<source>` element trees. What degrades agent accuracy is packing structured, multi-field items into a compact attribute microsyntax "to avoid verbosity." The principle's own exception, `srcset` (along with `sizes`), is a classic agent footgun where LLMs confuse width (`480w`) and pixel-density (`2x`) descriptors or corrupt commas vs. spaces when patching a single candidate.

Second, permitting different list delimiters across HTML attributes for external consistency (`class` and `sandbox` use spaces, `accept` and `srcset` use commas, `allow` Permissions Policy uses semicolons and spaces) forces agents to rely on memorized per-attribute syntax rather than a uniform rule, and using the wrong delimiter fails silently without parser errors. Third, while direct child elements (`<select>`/`<option>`) keep list items local in context, linking separate elements via string IDs (`<input list="id">` + `<datalist id="id">`) introduces cross-tree ID coordination that breaks across Shadow DOM boundaries and fails silently when an agent renames or duplicates a component.

## Value as a Slide Example

On its own, §3.2 is too narrow an HTML markup convention to serve as a headline slide example (`neither`, 2/5). The core guidance ("use space-separated attributes or child elements") is largely uncontroversial and does not demand a major shift in how specs are written.

Its main value for a TPAC slide is as a brief supporting example inside a broader point about **verbosity vs. compact microsyntaxes**: standards designed for humans sometimes invent dense attribute microsyntaxes like `srcset`/`sizes` to save keystrokes, whereas coding agents strongly prefer verbose, self-describing element trees (`<picture><source srcset="..." media="..."></picture>`) with named attributes and uniform delimiters that don't fail silently.
