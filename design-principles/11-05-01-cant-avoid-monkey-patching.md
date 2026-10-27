---
section: "11.5.1"
id: "cant-avoid-monkey-patching"
title: "If you need to monkey patch"
chapter: "11. Writing good specifications"
url: "https://w3ctag.github.io/design-principles/#cant-avoid-monkey-patching"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 1
verdict: "Purely internal specification-editing mechanics and inter-working-group workflow for managing temporary cross-spec patches; orthogonal to the web APIs consumed by coding agents."
---

# §11.5.1 If you need to monkey patch

GREP_SUMMARY: slide_example=neither | strength=1/5 | agent_fit=neutral | §11.5.1 cant-avoid-monkey-patching — If you need to monkey patch: Purely internal specification-editing mechanics and inter-working-group workflow for managing temporary cross-spec patches; orthogonal to the web APIs consumed by coding agents.

- **URL:** https://w3ctag.github.io/design-principles/#cant-avoid-monkey-patching
- **Chapter:** 11. Writing good specifications
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 1/5
- **Verdict:** Purely internal specification-editing mechanics and inter-working-group workflow for managing temporary cross-spec patches; orthogonal to the web APIs consumed by coding agents.

## Principle Summary

W3C TAG Design Principle §11.5.1 ("If you need to monkey patch") provides editorial and procedural hygiene rules for specification authors who must temporarily modify another specification's algorithms or definitions ("spec monkey-patching") before upstream consensus is reached. Note that in the TAG document, "monkey patching" refers to one specification prose-patching another specification from afar (such as inserting steps into the WHATWG Fetch algorithm or overriding CSS 2.1 formatting rules), not runtime JavaScript monkey-patching by web developers.

The principle instructs spec editors to mark monkey patches explicitly with `<p class="issue">` blocks noting the intent to merge upstream, identify target locations using exact text quotes or linked terms alongside step numbers (which can shift), use `<blockquote>` with `<ins>`/`<del>` for multi-part edits, and keep patches short by delegating to self-contained algorithms written for verbatim upstream pasting. It also outlines the cross-community process: filing an upstream tracking issue once local consensus forms, collaborating with upstream maintainers to use or create proper extension points, and deleting the monkey patch once merged. Finally, it contrasts spec monkey-patching with clean modularization (e.g., CSS Modules) and standard WebIDL `partial interface` extensions.

## Fit for Coding Agents

This principle is neutral (`agent_fit: neutral`) with respect to AI coding agents writing and reading web application code because it governs internal specification authoring mechanics and W3C/WHATWG editorial workflows rather than the design, syntax, or runtime semantics of Web APIs. Whether a downstream specification temporarily patches the `HTTP fetch` prose with an `<ins>` block or merges those algorithm steps directly into the upstream Fetch specification does not change the JavaScript or CSS surface (`fetch()`, `URLSearchParams.prototype.delete()`, or `font-size-adjust`) that a human developer or LLM coding agent consumes.

There are only minor, indirect downstream effects on the tooling ecosystem that coding agents rely on. When specifications use structured WebIDL `partial interface` declarations (such as extending `URLSearchParams.delete(name, value)`) and merge changes cleanly into upstream specs instead of leaving prose monkey-patches scattered across incubating documents, automated pipelines (`@webref/idl`, TypeScript's `lib.dom.d.ts` generator, and MDN documentation scrapers) can reliably extract machine-checkable type definitions that reduce agent hallucinations and power typechecker feedback loops. Similarly, if an LLM is used by spec authors or browser engineers to read or verify specifications, quoting target text verbatim and delegating to self-contained algorithms is much more resilient in an LLM's context window than bare step numbers ("Before step 4.2") that silently drift. For web developer DX, however, this section is purely internal spec-editing plumbing.

## Value as a Slide Example

This principle is a poor candidate for a TPAC slide (`slide_example: neither`, `example_strength: 1`) on how web standards should adapt to AI coding agents. Putting "If you need to monkey patch" on a slide in a developer-experience talk would almost certainly mislead the audience into thinking of JavaScript runtime monkey-patching (such as overriding `window.fetch` or `Element.prototype.attachShadow`), whereas §11.5.1 is strictly a Bikeshed/ReSpec editorial guide on formatting `<p class="issue">` blocks, `<blockquote>` diffs, and filing upstream issues between specification repositories. Because it is orthogonal to web API ergonomics for coding agents, it should be omitted from the presentation.
