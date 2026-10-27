---
section: "1.8"
id: "removing-features"
title: "Prioritize compatibility when changing or removing features"
chapter: "1. Principles behind design of Web APIs"
url: "https://w3ctag.github.io/design-principles/#removing-features"
agent_fit: "mixed"
slide_example: "clearly-harmful"
example_strength: 4
verdict: "Primarily an end-user protection rule for the unversioned web that shields agents from training-cutoff breakage, though it also immortalizes legacy footguns in agent feedback loops and relies on an 'only in examples' heuristic that LLM training corpora can invalidate."
---

# §1.8 Prioritize compatibility when changing or removing features

GREP_SUMMARY: slide_example=clearly-harmful | strength=4/5 | agent_fit=mixed | §1.8 removing-features — Prioritize compatibility when changing or removing features: Primarily an end-user protection rule for the unversioned web that shields agents from training-cutoff breakage, though it also immortalizes legacy footguns in agent feedback loops and relies on an 'only in examples' heuristic that LLM training corpora can invalidate.

- **URL:** https://w3ctag.github.io/design-principles/#removing-features
- **Chapter:** 1. Principles behind design of Web APIs
- **Agent-Fit:** mixed
- **Slide-Example:** clearly-harmful
- **Example-Strength:** 4/5
- **Verdict:** Primarily an end-user protection rule for the unversioned web that shields agents from training-cutoff breakage, though it also immortalizes legacy footguns in agent feedback loops and relies on an 'only in examples' heuristic that LLM training corpora can invalidate.

## Principle Summary

This principle states that before changing how a web feature behaves or removing it, spec authors and browser vendors must research how existing websites use it—for example, via user-agent metrics (UseCounters) or HTTP Archive queries. Because the web is unversioned, breaking existing content directly harms end users, so the benefit of any incompatible change must significantly outweigh that harm. This obligation extends beyond formal standards to include unspecified behaviors, vendor-proprietary features, and even implementation bugs that deployed sites rely upon.

The principle outlines narrow conditions under which breaking content is acceptable: when only a tiny fraction of content or users is affected, when usage appears only in test cases or examples, when the content is already broken in other major browsers (or the change improves interoperability), or when the user benefit is overwhelming—such as removing obsolete SSL and TLS versions to prevent security breaches.

## Fit for Coding Agents

While this principle is fundamentally an end-user protection policy for already-deployed websites rather than a developer ergonomics rule, its downstream effects on AI coding agents are mixed. On the positive side, strict backwards compatibility strongly protects coding agents from training-cutoff obsolescence. LLMs compress decades of public web code into static weights with a strong statistical bias toward older, high-frequency patterns. In ecosystems that frequently introduce breaking changes (such as fast-moving JavaScript frameworks or major library version bumps), coding agents routinely hallucinate removed APIs or mix incompatible version idioms. Because the web platform almost never breaks existing features, code generated from an agent's pre-training priors continues to execute reliably across browsers years later.

On the negative side, refusing to remove superseded features or fix historical quirks means legacy footguns remain permanently valid inside the agent's verification loop. When an agent writes code using outdated or error-prone APIs (such as `XMLHttpRequest`, `document.write`, legacy `Date` quirks, `-webkit-` prefixes, or `innerHTML` instead of `setHTML`), a headless browser test passes without error because compatibility preserved the behavior. Without a loud runtime failure or built-in deprecation gate, the agent receives positive reinforcement for generating legacy patterns.

Furthermore, one of the principle's explicit heuristics—that breakage is acceptable if "the content appears only in test cases or examples"—becomes hazardous in an agentic world. While HTTP Archive and browser UseCounters measure live production traffic, LLMs train directly on documentation examples, StackOverflow snippets, and test suites. Consequently, coding agents can actively resurrect "dead" example-only API patterns into brand-new production sites unless removals are accompanied by clear, machine-actionable console errors that guide the agent's test-and-repair loop to the modern replacement.

## Value as a Slide Example

As a headline TPAC slide example for how API design principles help or hurt coding agents, this principle is neither clearly useful nor clearly harmful (2/5). Its primary purpose is protecting end users browsing unmaintained sites on an unversioned web—a constraint that remains non-negotiable regardless of whether new websites are authored by humans or AI agents. Standards bodies will not start breaking existing websites just because agents can refactor maintained codebases more cheaply.

However, as a secondary talking point, the clause stating that features are safe to break when they "appear only in test cases or examples" offers a memorable observation for browser vendors: HTTP Archive and UseCounters measure what is currently deployed in production, whereas LLMs learn from source repositories, tutorials, and tests. Additionally, when browsers do deprecate or remove features (such as legacy TLS, old DOM quirks, or deprecated events), emitting loud, structured DevTools console diagnostics with explicit replacement APIs becomes critical so agents whose training weights predate the removal can self-correct in their execution loop.
