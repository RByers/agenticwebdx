---
section: "2.5"
id: "specs-include-guidance"
title: "Follow guidance from feature specifications"
chapter: "2. API Design Across Languages"
url: "https://w3ctag.github.io/design-principles/#specs-include-guidance"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 1
verdict: "An internal spec-editing and inter-working-group coordination rule about how specifications reference foundational primitives (Fetch, URL, Encoding, Time, HTTP); its downstream consistency is mildly helpful, but the principle itself is orthogonal to AI coding agent ergonomics."
---

# §2.5 Follow guidance from feature specifications

GREP_SUMMARY: slide_example=neither | strength=1/5 | agent_fit=neutral | §2.5 specs-include-guidance — Follow guidance from feature specifications: An internal spec-editing and inter-working-group coordination rule about how specifications reference foundational primitives (Fetch, URL, Encoding, Time, HTTP); its downstream consistency is mildly helpful, but the principle itself is orthogonal to AI coding agent ergonomics.

- **URL:** https://w3ctag.github.io/design-principles/#specs-include-guidance
- **Chapter:** 2. API Design Across Languages
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 1/5
- **Verdict:** An internal spec-editing and inter-working-group coordination rule about how specifications reference foundational primitives (Fetch, URL, Encoding, Time, HTTP); its downstream consistency is mildly helpful, but the principle itself is orthogonal to AI coding agent ergonomics.

## Principle Summary

W3C TAG Design Principle §2.5 ("Follow guidance from feature specifications") directs specification authors to follow the integration rules and usage guidance established by foundational specifications whenever building on top of them, and conversely requires foundational specs to document how other specifications should hook into them. It also instructs editors to consult with the community responsible for the underlying specification so both specs can evolve together.

It specifically calls out five foundational specifications and areas: character encodings (WHATWG Encoding), network requests (WHATWG Fetch), HTTP protocol conventions and header syntax (RFC 9105 / IETF HTTP Working Group style guide), timestamps and durations (Time), and URL parsing/resolution (WHATWG URL). The goal is to prevent individual web specs from inventing incompatible, ad-hoc dialects of core platform primitives or bypassing shared browser plumbing like CORS and Service Workers.

## Fit for Coding Agents

This principle is primarily about internal specification-authoring mechanics and inter-working-group coordination rather than developer-facing API ergonomics, making it largely neutral with respect to AI coding agents. Whether a web application is written by a human developer or an LLM coding agent has no direct bearing on how a W3C specification editor references WHATWG Fetch algorithms or consults the IETF HTTP Working Group when defining a new HTTP header.

Indirectly, the downstream platform consistency that results from following this principle provides a modest second-order benefit to coding agents. LLMs rely heavily on transferable statistical priors across APIs: when every web specification resolves URLs via the same WHATWG URL parser, mandates UTF-8 per the Encoding specification, uses standard high-resolution time primitives (`DOMHighResTimeStamp` / `EpochTimeStamp`), formats new HTTP headers with Structured Fields (RFC 8941/9651), and routes network requests through the Fetch pipeline (ensuring uniform CORS, CSP, Service Worker, and DevTools behavior), agents encounter fewer silent per-feature discrepancies or special-case parsing bugs.

However, that benefit is a downstream effect of general platform uniformity rather than a direct consequence of §2.5. The rule itself governs spec-to-spec modularity and standards-body collaboration, neither specifically helping nor pulling against agent-written code.

## Value as a Slide Example

§2.5 is not useful as a slide example (`neither`, 1/5) for a TPAC breakout session on how AI coding agents affect web standards and developer experience. Because the rule is an editorial and procedural directive aimed at specification writers ("follow guidance in the specification for that feature... consult with the relevant community"), featuring it on a slide would focus the audience on internal standards-process plumbing rather than concrete API design trade-offs for coding agents.

While uniform behavior for URLs, encodings, HTTP headers, timestamps, and Fetch across Web APIs is mildly helpful to agents, that point is much better represented by developer-facing consistency principles than by an inter-spec referencing guideline.
