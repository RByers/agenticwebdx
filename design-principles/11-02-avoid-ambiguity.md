---
section: "11.2"
id: "avoid-ambiguity"
title: "Specify completely and avoid ambiguity"
chapter: "11. Writing good specifications"
url: "https://w3ctag.github.io/design-principles/#avoid-ambiguity"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Unambiguous specifications remain vital for coding agents because behavioral divergence across engines breaks single-browser agent verification loops and pollutes training data with fragile workarounds, though this is foundational spec hygiene rather than a distinctive API design insight."
---

# §11.2 Specify completely and avoid ambiguity

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §11.2 avoid-ambiguity — Specify completely and avoid ambiguity: Unambiguous specifications remain vital for coding agents because behavioral divergence across engines breaks single-browser agent verification loops and pollutes training data with fragile workarounds, though this is foundational spec hygiene rather than a distinctive API design insight.

- **URL:** https://w3ctag.github.io/design-principles/#avoid-ambiguity
- **Chapter:** 11. Writing good specifications
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Unambiguous specifications remain vital for coding agents because behavioral divergence across engines breaks single-browser agent verification loops and pollutes training data with fragile workarounds, though this is foundational spec hygiene rather than a distinctive API design insight.

## Principle Summary

W3C TAG Design Principle §11.2 instructs specification authors to define feature behavior completely and unambiguously so that browser implementers do not make divergent choices that force web developers to write browser-specific workarounds. Furthermore, a specification should stand on its own as a complete reference rather than forcing implementers to reverse-engineer other browsers to achieve interoperability (while still allowing variation in rendering details or browser UI like permission prompts).

For human developers and browser vendors, this principle reflects the core lesson of the WHATWG/HTML5 era: underspecified edge cases inevitably turn into cross-browser interoperability hazards, forcing every web author to learn obscure engine quirks and maintain defensive branching code.

## Fit for Coding Agents

This principle is a good fit for AI coding agents, and in practice cross-engine behavioral ambiguity is even harder for agents to catch than for experienced human developers. One might superficially assume that because LLMs can generate extra adapter or fallback boilerplate cheaply, they suffer less when implementations diverge. That only holds when differences are explicit in the API surface (where feature detection or TypeScript types can guide the agent). When a specification is ambiguous, the API signature looks identical across browsers, yet runtime behavior diverges silently on edge cases—such as non-ISO strings in `Date.parse()`, `contenteditable` editing behaviors, or historically underspecified CSS layout and focus order rules.

Coding agents rely heavily on automated feedback loops that almost always execute against a single environment—typically headless Chromium via Playwright or a synthetic DOM shim like `jsdom` or `happy-dom`. If a spec leaves behavior ambiguous and WebKit or Gecko diverges from Chromium, an agent will see its test suite pass in Chromium and confidently ship broken code. Worse, historical spec ambiguities pollute the training corpus with conflicting StackOverflow workarounds, brittle User-Agent sniffing, and obsolete engine-specific hacks that agents frequently hallucinate into modern codebases.

Additionally, outside of web-app authoring, coding agents are increasingly used within standards and browser engineering workflows—generating Web Platform Tests (WPT), checking spec compliance, and drafting implementation patches. Complete, deterministic, algorithmic specification prose (in the style of WHATWG specs) is vastly easier for agents to translate accurately into tests and code than prose that leaves edge cases implicit.

## Value as a Slide Example

Despite aligning well with agent needs, this principle is neither a strong `clearly-useful` nor `clearly-harmful` headline example for a TPAC slide (`example_strength: 2`). "Write complete, unambiguous specs so browsers interoperate" has been consensus web standards orthodoxy for two decades. Nobody is proposing that specs become more ambiguous for agents, and the principle operates at the level of specification authorship rather than concrete Web API ergonomics.

If mentioned at all, its best role is as a brief supporting observation: agents amplify the cost of spec ambiguity (such as historical `Date.parse()` or `contenteditable` divergences) because they typically verify code in a single headless browser engine (usually Chromium) and cannot rely on human intuition to suspect a Safari- or Firefox-specific edge case when the spec left behavior underspecified.
