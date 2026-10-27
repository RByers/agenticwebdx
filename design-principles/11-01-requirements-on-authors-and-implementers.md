---
section: "11.1"
id: "requirements-on-authors-and-implementers"
title: "Identify the audience of each requirement in your specification"
chapter: "11. Writing good specifications"
url: "https://w3ctag.github.io/design-principles/#requirements-on-authors-and-implementers"
agent_fit: "mixed"
slide_example: "clearly-harmful"
example_strength: 4
verdict: "Defining a strict 'conforming language' for authors separately from the browser's forgiving 'supported language' enables the static validators and linters that coding agents need, even though the underlying web philosophy of silently accepting poorly-formed markup for a 'shallower learning curve' undermines agent feedback loops."
---

# §11.1 Identify the audience of each requirement in your specification

GREP_SUMMARY: slide_example=clearly-harmful | strength=4/5 | agent_fit=mixed | §11.1 requirements-on-authors-and-implementers — Identify the audience of each requirement in your specification: Defining a strict 'conforming language' for authors separately from the browser's forgiving 'supported language' enables the static validators and linters that coding agents need, even though the underlying web philosophy of silently accepting poorly-formed markup for a 'shallower learning curve' undermines agent feedback loops.

- **URL:** https://w3ctag.github.io/design-principles/#requirements-on-authors-and-implementers
- **Chapter:** 11. Writing good specifications
- **Agent-Fit:** mixed
- **Slide-Example:** clearly-harmful
- **Example-Strength:** 4/5
- **Verdict:** Defining a strict 'conforming language' for authors separately from the browser's forgiving 'supported language' enables the static validators and linters that coding agents need, even though the underlying web philosophy of silently accepting poorly-formed markup for a 'shallower learning curve' undermines agent feedback loops.

## Principle Summary

Section 11.1 ("Identify the audience of each requirement in your specification") instructs specification editors to clearly distinguish between normative requirements for web authors (how to write valid, well-formed code) and normative requirements for user agent implementers (how browsers must parse and recover from poorly-formed or legacy code). It characterizes this split as two distinct languages within a specification: the narrower "conforming language" that authors should write, and the larger "supported language" that browsers must implement.

This principle exists because the web platform prioritizes backward compatibility and fault tolerance over strict rejection of invalid input. By requiring specifications to define deterministic error-recovery rules for browsers alongside stricter authoring rules, the web ensures that older or malformed pages render consistently across engines and human beginners face a "shallower learning curve," while validators and educational resources still have an authoritative definition of valid code.

## Fit for Coding Agents

This principle cuts both ways (`mixed`) for AI coding agents because the specification hygiene it prescribes enables static validation tools, whereas the underlying platform philosophy it invokes—silently accepting poorly-formed markup so that "authors have a shallower learning curve"—actively undermines the agentic feedback loop.

On the negative side, the gap between the browser's forgiving "supported language" and the strict "conforming language" creates silent failures and training-data noise for LLMs. Unlike human beginners in the 1990s, coding agents do not benefit from a "shallower learning curve" where invalid code still renders something on screen; agents thrive on immediate, loud, machine-readable error signals. When a browser silently recovers from malformed HTML (such as auto-closing `<p>` tags before a `<div>`, foster-parenting invalid table children, or ignoring unknown attributes) or silently drops invalid CSS declarations and selectors inside forgiving selector lists (`:is()`, `:where()`), an agent checking the runtime console receives a false-positive "no errors" signal while leaving corrupted DOM structure, broken styles, or broken accessibility unfixed. Furthermore, because the "supported language" runs without error in browsers, the open web training corpus is saturated with non-conforming markup that LLMs internalize and reproduce.

On the positive side, precisely because browsers cannot break backward compatibility for end users, §11.1's requirement that specifications explicitly define a narrow "conforming language" for authors separately from the implementer's "supported language" is vital for agentic tooling. Normative author conformance requirements (such as HTML element content models, ARIA role/property constraints, and CSS grammar definitions) are what empower static validators, linters, language servers, and type definitions to flag invalid code before or during an agent's verification loop. Clearly labeling author requirements versus parser recovery rules in specs also helps documentation pipelines (like MDN and `@webref`) and spec-reading agents distinguish recommended idioms from legacy fallback behavior.

## Value as a Slide Example

As a literal rule ("Identify the audience of each requirement in your specification"), §11.1 is primarily a spec-editing convention rather than a web API design principle (`neither`), so it is a moderate (**3/5**) candidate rather than a headline slide example on its own. Nobody at TPAC would argue that specifications should stop distinguishing between author conformance rules and browser implementation rules.

However, the vocabulary and rationale introduced in §11.1—specifically the split between the **"conforming language"** and the **"supported language,"** and the claim that accepting poorly-formed markup gives authors a **"shallower learning curve"**—offer a sharp talking point for how standards should adapt to AI coding agents. On a slide contrasting human DX with agent DX, this principle highlights that while silent HTML/CSS error recovery lowered the barrier for human novices, it deprives agents of runtime error signals. That makes machine-checkable definitions of the "conforming language" (and potentially new browser DevTools or WebDriver BiDi diagnostics that loudly report when a page falls back from the "conforming language" to the "supported language") much more valuable in an agentic world.
