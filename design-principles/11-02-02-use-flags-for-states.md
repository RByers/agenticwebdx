---
section: "11.2.2"
id: "use-flags-for-states"
title: "Use explicit flags for state"
chapter: "11. Writing good specifications"
url: "https://w3ctag.github.io/design-principles/#use-flags-for-states"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 1
verdict: "Internal specification-authoring mechanic for writing unambiguous algorithm state transitions; orthogonal to the web API surface coding agents consume, though beneficial when agents parse specs to generate tests or polyfills."
---

# §11.2.2 Use explicit flags for state

GREP_SUMMARY: slide_example=neither | strength=1/5 | agent_fit=neutral | §11.2.2 use-flags-for-states — Use explicit flags for state: Internal specification-authoring mechanic for writing unambiguous algorithm state transitions; orthogonal to the web API surface coding agents consume, though beneficial when agents parse specs to generate tests or polyfills.

- **URL:** https://w3ctag.github.io/design-principles/#use-flags-for-states
- **Chapter:** 11. Writing good specifications
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 1/5
- **Verdict:** Internal specification-authoring mechanic for writing unambiguous algorithm state transitions; orthogonal to the web API surface coding agents consume, though beneficial when agents parse specs to generate tests or polyfills.

## Principle Summary

Section §11.2.2 ("Use explicit flags for state") instructs specification editors to represent state in algorithms using explicit named flags or state variables rather than describing state informally with words.

This guideline exists to eliminate ambiguity for browser implementers and test writers. When state is only described in prose, specifications frequently leave edge cases underspecified—especially whether a state change persists when an algorithm aborts early due to an error condition, and exactly when or how that state is later reset. Explicit flags turn prose descriptions into deterministic, verifiable state machines.

## Fit for Coding Agents

For AI coding agents writing and maintaining web applications, §11.2.2 is largely neutral because it is an internal specification-editing mechanic rather than a web-developer-facing API design rule. It dictates how spec editors structure algorithmic steps inside a specification document, not the JavaScript, HTML, or CSS interfaces that coding agents call. Consequently, it has no direct impact on an application coding agent's token efficiency, API signature priors, argument-order hallucinations, or runtime error observability.

Indirectly, however, the principle supports coding agents in two ways. First, in web application development, ambiguous specification prose around whether state mutates before an error return or when state resets is a classic source of cross-browser interoperability bugs (for instance, in complex stateful APIs like media playback, WebRTC signaling, or Streams). By forcing spec authors to make state transitions and error resets explicit, browser engines behave consistently on edge cases, sparing coding agents from having to synthesize fragile browser-specific workarounds.

Second, if the scope is expanded from web application DX to standards-engineering agents—agents that read W3C/WHATWG specifications to generate Web Platform Tests (WPT), write polyfills, or assist with browser engine implementations—explicit state flags are a major advantage. LLMs trace explicit state variable mutations across step-by-step algorithms far more accurately than they infer implied state from conversational English prose, directly reducing hallucinated test assertions on error and reset paths.

## Value as a Slide Example

This principle is a weak slide candidate (1/5, `neither`) for a TPAC session focused on how web standards should adapt their Developer Experience (DX) for coding agents. Because §11.2.2 is an editorial guideline for writing internal specification algorithms rather than designing developer-facing Web APIs, featuring it on a slide would conflate spec-authoring mechanics with web developer ergonomics. While it is mildly relevant to using LLMs to generate Web Platform Tests (WPT) from spec prose, there are far more direct, high-impact principles in the TAG document that illustrate how API surfaces help or hinder coding agents.
