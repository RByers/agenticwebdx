---
section: "1.2"
id: "safe-to-browse"
title: "It should be safe to visit a web page"
chapter: "1. Principles behind design of Web APIs"
url: "https://w3ctag.github.io/design-principles/#safe-to-browse"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 1
verdict: "Fundamental end-user security and privacy boundary that applies regardless of whether a human or an AI coding agent authored the web page."
---

# §1.2 It should be safe to visit a web page

GREP_SUMMARY: slide_example=neither | strength=1/5 | agent_fit=neutral | §1.2 safe-to-browse — It should be safe to visit a web page: Fundamental end-user security and privacy boundary that applies regardless of whether a human or an AI coding agent authored the web page.

- **URL:** https://w3ctag.github.io/design-principles/#safe-to-browse
- **Chapter:** 1. Principles behind design of Web APIs
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 1/5
- **Verdict:** Fundamental end-user security and privacy boundary that applies regardless of whether a human or an AI coding agent authored the web page.

## Principle Summary

W3C TAG Design Principle §1.2 (`safe-to-browse`) states that new web platform features must preserve the foundational user expectation that merely visiting a hyperlink is safe for their computer's security and their essential privacy. Because the Web is defined by its hyperlinked structure, users must be able to click links to unknown websites without fearing that loading a page will compromise their device or silently expose sensitive personal information, such as whether they use assistive technologies.

Even when adding a powerful capability to the web improves overall user safety by sparing users from installing a riskier native application (for instance, ordering food on a web page instead of installing a native app), that benefit must be weighed against maintaining the baseline expectation that visiting any URL is safe. Where technical reality and user expectations diverge, the platform should combine clearer browser UI with stronger technical privacy and security foundations.

## Fit for Coding Agents

This principle is neutral with respect to AI coding agents because it governs the security and privacy trust boundary between an untrusted web origin and the end user, rather than developer authoring ergonomics (DX). The web's threat model assumes that any website may be malicious or defective regardless of whether its code was written by a human developer or synthesized by an LLM. In fact, as coding agents drastically lower the cost of generating and deploying web applications—and as users increasingly open links to ephemeral, agent-generated web experiences—preserving the invariant that visiting a URL is safe becomes even more vital for the ecosystem, without changing how the design principle itself applies.

In day-to-day agent coding workflows, `safe-to-browse` manifests only indirectly through two secondary effects. First, the mechanisms browsers use to enforce safety on page visit—such as transient user activation (`navigator.userActivation`), permission prompts, and secure-context gates on APIs like `navigator.clipboard.readText()`, `getUserMedia()`, WebUSB, File System Access, and audio autoplay—often trip up coding agents when they generate code that invokes gated APIs on initial load or across an `await` boundary, or when they attempt to test permission-gated flows in automated headless browser feedback loops (where loud `NotAllowedError` exceptions are essential for the agent to self-correct). Second, the strict browser sandbox guaranteed by `safe-to-browse` makes executing and previewing untrusted, freshly generated web code in a browser tab vastly safer than running agent-generated native code on the host OS.

## Value as a Slide Example

This principle is neither a `clearly-useful` nor a `clearly-harmful` example for a TPAC slide (`example_strength: 1/5`). Because the breakout session examines how AI coding agents redefine developer experience (DX) and whether web standards principles designed around human coding constraints should adapt, an end-user security and privacy sandboxing principle is orthogonal to the core thesis.

At most, `safe-to-browse` could be mentioned in passing as part of a baseline framing point: end-user protection principles (security, privacy, accessibility) remain non-negotiable invariants regardless of whether a human or an agent writes the site, in contrast to API ergonomics principles elsewhere in the TAG document that are directly affected by agentic coding.
