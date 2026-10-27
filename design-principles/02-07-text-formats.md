---
section: "2.7"
id: "text-formats"
title: "Design textual formats for humans"
chapter: "2. API Design Across Languages"
url: "https://w3ctag.github.io/design-principles/#text-formats"
agent_fit: "poor"
slide_example: "clearly-harmful"
example_strength: 5
verdict: "LLMs strongly benefit from readable, self-describing textual formats over compact microsyntaxes or binary formats (which tooling can compress), but the principle's push for loose syntax and silent error containment to help unassisted human text editing obscures errors in an agent's validation loop."
---

# §2.7 Design textual formats for humans

GREP_SUMMARY: slide_example=clearly-harmful | strength=5/5 | agent_fit=poor | §2.7 text-formats — Design textual formats for humans: LLMs strongly benefit from readable, self-describing textual formats over compact microsyntaxes or binary formats (which tooling can compress), but the principle's push for loose syntax and silent error containment to help unassisted human text editing obscures errors in an agent's validation loop.

- **URL:** https://w3ctag.github.io/design-principles/#text-formats
- **Chapter:** 2. API Design Across Languages
- **Agent-Fit:** poor
- **Slide-Example:** clearly-harmful
- **Example-Strength:** 5/5
- **Verdict:** LLMs strongly benefit from readable, self-describing textual formats over compact microsyntaxes or binary formats (which tooling can compress), but the principle's push for loose syntax and silent error containment to help unassisted human text editing obscures errors in an agent's validation loop.

## Principle Summary

W3C TAG Principle §2.7 (`text-formats`) advises specification authors to design textual formats so they can be easily read, written, and edited by people in a standard text editor. It argues for prioritizing human readability over compactness—noting that wire size can be optimized by build and compression tooling—while reserving binary formats for purely machine-to-machine use cases where direct human authoring is undesirable.

Because humans editing raw text inevitably introduce typos and syntax mistakes and can struggle to locate and fix them, the principle also recommends defining syntactic flexibility (around whitespace, quoting, and delimiters) and containing the blast radius of syntax errors through well-defined error recovery rules so that a single mistake does not break an entire document.

## Fit for Coding Agents

This principle cuts strongly in both directions for AI coding agents (`mixed`), because it bundles together two distinct design choices—semantic readability and forgiving, unassisted text-editor ergonomics—while relying on a pre-LLM dichotomy between "people (text)" and "machines (binary)".

First, favoring readability over compactness and relying on tooling to optimize file size strongly benefits coding agents. The principle's closing claim—"If your format is intended to be used only by machines, a binary format is likely to be more efficient"—breaks down for LLM coding agents, which are machines that operate natively over text tokens and natural-language statistical priors rather than binary streams. When web formats favor self-describing readability over dense compactness (leaving wire size to minifiers and Brotli), agents hallucinate far less. For example, LLMs frequently hallucinate positional numbers and unnamed `0`/`1` boolean arc flags in SVG's compact `<path d="M 10 20 A 30 30 0 0 1 50 60">` microsyntax or `matrix3d(...)` transforms, whereas readable, keyword-anchored syntax like CSS `shape(from 10px 20px, arc to 50px 60px of 30px cw small)` or structured JSON formats (`importmap`, `speculationrules`, Web App Manifest) align directly with token-level attention and semantic priors.

Second, however, the principle's push for syntactic flexibility and error-scope containment optimizes for a human editing raw files in a basic text editor without validation tooling ("People who edit text will introduce a range of errors, but could struggle to identify and fix those errors... Containing the scope of a format that is affected by a syntax error"). On the web platform, this philosophy produced HTML's forgiving parser and CSS's forward-compatible error recovery, where an invalid property, hallucinated value, or malformed selector is silently ignored at the next `;` or `}` without throwing an error. Unlike unassisted humans in a plain text editor, coding agents excel at fixing syntax errors once notified, but silent error containment blinds their automated feedback loop—causing the agent to assume a broken CSS rule or malformed HTML attribute succeeded unless it performs expensive visual or computed-style inspection.

## Value as a Slide Example

Because the principle pulls in opposite directions, it does not fit cleanly as a one-sided headline example of a rule that is purely `clearly-useful` or purely `clearly-harmful` (`neither`, strength 3/5). Putting "Design textual formats for humans" in a "Harmful to Agents" bucket would mislead an audience because LLMs still fundamentally require human-readable textual formats rather than binary ones; putting it uncritically in a "Useful to Agents" bucket would ignore its endorsement of loose syntax and silent error absorption.

However, if the talk includes a nuanced point on how existing TAG principles need to be split or reframed for an agentic era, §2.7 is a memorable example because its title ("for humans") and binary-for-machines assumption directly confront the nature of LLMs. It illustrates a sharp takeaway for web standards: keep human-readable, self-describing syntax (like CSS `shape()` over SVG `path()`, since LLMs are text-native "machines") and keep delegating compactness to tooling, but pair runtime error containment with loud, machine-checkable validation diagnostics so agents are not trapped by silent recovery.
