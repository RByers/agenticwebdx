---
section: "11.2.1"
id: "algorithms"
title: "Define algorithms clearly"
chapter: "11. Writing good specifications"
url: "https://w3ctag.github.io/design-principles/#algorithms"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 2
verdict: "Primarily internal spec-editing guidance for browser implementers; orthogonal to web-app coding agents except indirectly via cross-browser consistency and when agents read specs to generate WPTs or polyfills."
---

# §11.2.1 Define algorithms clearly

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=neutral | §11.2.1 algorithms — Define algorithms clearly: Primarily internal spec-editing guidance for browser implementers; orthogonal to web-app coding agents except indirectly via cross-browser consistency and when agents read specs to generate WPTs or polyfills.

- **URL:** https://w3ctag.github.io/design-principles/#algorithms
- **Chapter:** 11. Writing good specifications
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Primarily internal spec-editing guidance for browser implementers; orthogonal to web-app coding agents except indirectly via cross-browser consistency and when agents read specs to generate WPTs or polyfills.

## Principle Summary

Section 11.2.1 ("Define algorithms clearly") guides specification editors on how to write normative algorithms in web standards. It recommends writing algorithms as clear, concise sequences of pseudo-code steps structured like functional code—explicitly stating inputs, outputs, well-named variables, and return or error points while avoiding side effects—or using formal grammars and state machines where appropriate. It also advises summarizing an algorithm's purpose up front so readers can decide whether to read or skip the detailed steps.

Crucially, the principle instructs editors to write algorithms as closely as possible to how browser engines actually implement them, even when that differs from how web authors mentally read a feature (for instance, specifying CSS selector matching from right to left rather than left to right). This prevents different browser implementers from making divergent architectural decisions when translating spec text into engine code.

## Fit for Coding Agents

For AI coding agents building web applications (writing HTML, CSS, and JavaScript), this principle is largely neutral because it governs internal specification prose rather than the developer-facing shape of Web APIs. Whether a specification writes its internal processing model as a state machine, a grammar, or a right-to-left step sequence does not alter the API surface, parameter ergonomics, or runtime feedback loop that an application-level coding agent interacts with. Its primary benefit to web-app coding agents is indirect: when specs explicitly enumerate return/error branches and align with real engine architectures, browser implementations converge on identical edge-case behavior, reducing cross-browser quirks that cause agent-generated code to fail unpredictably across engines.

However, if we also consider coding agents used within the standards and browser engineering workflow—such as agents reading specs via RAG/MCP to verify edge-case behavior, generate Web Platform Tests (WPT), write polyfills, or draft browser engine code—this principle is quite aligned with LLM strengths, with one notable tension. Functional pseudo-code with explicit inputs, outputs, return/error points, and minimal hidden side effects maps directly onto how LLMs trace control flow and synthesize test cases for each branch. Moreover, the instruction to summarize an algorithm's purpose before the step list acts as progressive disclosure, allowing an agent scanning a large specification to decide whether to read or skip the detailed steps and conserve context tokens. On the other hand, writing algorithms to match engine implementation mechanics (such as right-to-left CSS selector matching) rather than author mental models helps browser-engine agents but can confuse a web-developer agent consulting the spec to understand author-facing behavior.

## Value as a Slide Example

This principle is neither a strong 'clearly-useful' nor 'clearly-harmful' headline slide example for a TPAC session on how web standards should adapt to AI coding agents redefining Web DX (2/5). Because §11.2.1 is directed at specification editors rather than governing the ergonomics of Web APIs exposed to developers, putting it on a main slide would distract from concrete API-design rules (such as loud vs. silent errors, naming consistency, or high-level vs. low-level APIs).

If referenced at all, it serves best as a brief aside on machine-readable specifications: as agents are increasingly used by spec editors and browser engineers to generate Web Platform Tests (WPT), polyfills, and engine implementations directly from spec prose, the TAG's guidance to use side-effect-free functional pseudo-code, formal grammars, state machines, and upfront purpose summaries makes specifications much easier for LLMs to parse and translate accurately.
