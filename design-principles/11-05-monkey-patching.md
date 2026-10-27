---
section: "11.5"
id: "monkey-patching"
title: "Avoid monkey patching"
chapter: "11. Writing good specifications"
url: "https://w3ctag.github.io/design-principles/#monkey-patching"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 1
verdict: "Purely about cross-specification editorial mechanics (Spec B overriding Spec A's prose algorithms), making it orthogonal to Web API ergonomics for coding agents writing web applications."
---

# §11.5 Avoid monkey patching

GREP_SUMMARY: slide_example=neither | strength=1/5 | agent_fit=neutral | §11.5 monkey-patching — Avoid monkey patching: Purely about cross-specification editorial mechanics (Spec B overriding Spec A's prose algorithms), making it orthogonal to Web API ergonomics for coding agents writing web applications.

- **URL:** https://w3ctag.github.io/design-principles/#monkey-patching
- **Chapter:** 11. Writing good specifications
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 1/5
- **Verdict:** Purely about cross-specification editorial mechanics (Spec B overriding Spec A's prose algorithms), making it orthogonal to Web API ergonomics for coding agents writing web applications.

## Principle Summary

Despite sharing a name with the JavaScript runtime practice of mutating built-in prototypes or globals, §11.5 ("Avoid monkey patching") is strictly about specification authoring mechanics. It warns specification editors against having Specification B directly override or modify an internal algorithm defined in Specification A without using explicit, publicly defined extension points in Specification A.

This rule exists to keep the web platform's specification corpus maintainable and coherent for spec editors and browser implementers. When one spec monkey-patches another spec's algorithms from afar, upstream edits to the base spec can silently invalidate the patch, multiple specs patching the same algorithm create undefined ordering conflicts, the base spec's maintainers miss the chance to review the architectural interaction, and browser engineers reading the base spec can easily overlook or inadvertently revert the external behavior.

## Fit for Coding Agents

For AI coding agents authoring and debugging web application code, this principle is neutral (orthogonal). How specification editors organize algorithm hooks across W3C and WHATWG documents does not directly alter the syntax, token footprint, type checkability, or error-reporting semantics of the Web APIs that coding agents consume. Whether a lifecycle step is defined directly inside the HTML or Fetch living standard or via a well-defined extension point only matters to web developers and coding agents indirectly, insofar as avoiding spec monkey-patching prevents subtle cross-feature browser inconsistencies and spec bugs.

If the scope were expanded from web developer DX to agents assisting browser engineers and spec editors (e.g., agents reading specs to generate Web Platform Tests or implement browser features), avoiding spec monkey-patching is strongly beneficial. Retrieval-augmented or context-limited agents reading a base specification's algorithm (such as Fetch or DOM event dispatch) will only see the text in that document; they cannot reliably discover that a separate, unlinked specification reaches in and alters step 4 of that algorithm unless the base specification explicitly exposes an extension hook or integrates the logic directly. However, for the core topic of web developer DX for coding agents, it remains an internal spec-editing concern.

## Value as a Slide Example

This principle is not suitable (neither, strength 1/5) for a TPAC slide on how web standards should adapt to AI coding agents redefining developer experience. Because it governs editorial hygiene between specification documents rather than Web API design, it offers no insight into how platform APIs should evolve for LLM ergonomics.

Furthermore, featuring "Avoid monkey patching" on a slide about developer experience would actively confuse the audience: most web developers and standards participants glancing at a slide will assume it refers to runtime JavaScript monkey-patching (such as polyfills, Zone.js, or wrapping window.fetch and History.prototype.pushState), rather than Spec B patching Spec A's prose algorithms.
