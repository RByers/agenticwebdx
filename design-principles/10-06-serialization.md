---
section: "10.6"
id: "serialization"
title: "Consider consumers when serializing"
chapter: "10. Other API Design Considerations"
url: "https://w3ctag.github.io/design-principles/#serialization"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Helps coding agents by ensuring serialized DOM/CSSOM/URL outputs match authored syntax priors, round-trip cleanly across APIs, and support reliable inspection and test assertions in agent feedback loops."
---

# §10.6 Consider consumers when serializing

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §10.6 serialization — Consider consumers when serializing: Helps coding agents by ensuring serialized DOM/CSSOM/URL outputs match authored syntax priors, round-trip cleanly across APIs, and support reliable inspection and test assertions in agent feedback loops.

- **URL:** https://w3ctag.github.io/design-principles/#serialization
- **Chapter:** 10. Other API Design Considerations
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Helps coding agents by ensuring serialized DOM/CSSOM/URL outputs match authored syntax priors, round-trip cleanly across APIs, and support reliable inspection and test assertions in agent feedback loops.

## Principle Summary

W3C TAG Design Principle §10.6 ("Consider consumers when serializing") advises spec authors to design serialization algorithms with three distinct consumers in mind: end users (who may see serialized values in UI), developer tools (which inspect serialized output, for instance to detect whether a parser had to correct errors in the input), and other Web APIs (which accept serialized strings as input). It also reminds spec authors to account for language-specific expectations such as significant whitespace and floating-point precision.

To serve these consumers, the principle specifies three requirements for serialized output: it should match developer expectations (e.g., serialized CSS should look like what a CSS author would write), it should be idempotent (parsing and re-serializing a serialized string produces itself), and it should not accumulate errors when serialized output is fed back into the same API in a loop.

## Fit for Coding Agents

This principle is a good fit for AI coding agents and becomes even more important when the agent acts as both the code author and an automated tool inspecting the browser in a closed feedback loop. First, "matching developer expectations" directly maps to matching LLM training-data priors. Coding agents frequently generate Playwright or unit test assertions against serialized browser state (`element.style.color`, `getComputedStyle(el).transform`, `CSSRule.cssText`, `URL.href`, `element.innerHTML`). Because an agent's priors are heavily weighted toward how values are authored in source code, serialization formats that diverge sharply from authored syntax—such as `#ff0000` serializing to `rgb(255, 0, 0)` or `transform: translateX(10px)` serializing in `getComputedStyle` to `matrix(1, 0, 0, 1, 10, 0)`—routinely cause agents to hallucinate failing test assertions on the first pass and waste turns debugging the mismatch.

Second, the principle explicitly identifies "Tools" as a key consumer of serialization, specifically noting that tools rely on serialized output to detect whether a parser had to recover from errors in the input. Because core web languages like HTML and CSS fail silently when given invalid syntax, coding agents operating via DevTools or Playwright MCP bridges rely on reading back serialized DOM/CSSOM state to verify whether their generated code was actually accepted by the browser. Predictable, canonical serialization turns silent parse drops into observable feedback in the agent loop.

Third, idempotence and the absence of error accumulation protect agent-written glue code from subtle state-drift bugs. Agents commonly write naive read-modify-write loops or pipe the serialized output of one Web API directly into another (for example, round-tripping URLs, `DOMMatrix` transforms, SVG paths, or `CSSStyleDeclaration` strings). Guaranteeing that `serialize(parse(x))` is idempotent and does not accumulate floating-point or canonicalization drift prevents compounding errors across iterative agent edits and runtime state updates.

## Value as a Slide Example

§10.6 is a solid supporting example (`clearly-useful`, 3/5 strength) for a TPAC talk because it already names "Tools" as a first-class consumer of serialization—and in 2026, "Tools" increasingly means LLM coding agents and their automated test harnesses inspecting live DOM/CSSOM state. While it is narrower in scope than overarching API design principles (making it a 3/5 supporting point rather than a 5/5 headline slide), it provides an immediately recognizable, concrete pain point that standards authors have wrestled with for years.

Specifically, CSS serialization quirks where the serialized output diverges from what the author wrote—such as `getComputedStyle(el).transform` serializing `translateX(10px)` into `matrix(1, 0, 0, 1, 10, 0)` or CSS colors serializing hex/named values into `rgb(...)` or `color(srgb ...)`—are a notorious source of first-turn failures in agent-generated Playwright and DOM tests. Highlighting §10.6 shows how a principle originally written for human expectations and linters directly reduces friction in the agentic write-test-inspect loop.
