---
section: "10.7"
id: "debuggability"
title: "Ensure features are developer-friendly"
chapter: "10. Other API Design Considerations"
url: "https://w3ctag.github.io/design-principles/#debuggability"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 5
verdict: "Specific, localizing error messages and spec-defined introspection for declarative features (like Web Animations) are essential to closing the autonomous agent feedback loop, though agents need debuggability exposed programmatically rather than only in visual DevTools panels."
---

# §10.7 Ensure features are developer-friendly

GREP_SUMMARY: slide_example=clearly-useful | strength=5/5 | agent_fit=good | §10.7 debuggability — Ensure features are developer-friendly: Specific, localizing error messages and spec-defined introspection for declarative features (like Web Animations) are essential to closing the autonomous agent feedback loop, though agents need debuggability exposed programmatically rather than only in visual DevTools panels.

- **URL:** https://w3ctag.github.io/design-principles/#debuggability
- **Chapter:** 10. Other API Design Considerations
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 5/5
- **Verdict:** Specific, localizing error messages and spec-defined introspection for declarative features (like Web Animations) are essential to closing the autonomous agent feedback loop, though agents need debuggability exposed programmatically rather than only in visual DevTools panels.

## Principle Summary

Despite its broad title ("Ensure features are developer-friendly"), §10.7 (`#debuggability`) focuses specifically on diagnostic error messages and debuggability. It states that even when JavaScript exception text is kept generic, developer-oriented error messages (such as those logged to the developer console) must be meaningful, specific to the error case, and detailed enough to help developers pinpoint the source of the problem.

It further notes that declarative features such as CSS require explicit specification effort to support debuggability. Defining debuggability hooks directly in the specification—citing the Web Animations spec as a model example—makes declarative features easier to diagnose and guarantees a consistent debugging experience across browsers.

## Fit for Coding Agents

This principle is a strong fit (`good`) for AI coding agents because diagnostic observability is the foundation of the agentic edit-run-verify feedback loop. When an agent writes or modifies web code and evaluates it via Playwright, WebDriver BiDi, or a Chrome DevTools MCP server, vague errors or silent no-ops force the agent to guess blindly across multiple turns, burning tokens and hallucinating workarounds. Specific console diagnostics that pinpoint the exact failure case, offending selector, or invalid parameter allow an LLM agent to self-correct deterministically in a single turn.

Furthermore, the principle's insistence on defining debuggability in the specification for declarative features like CSS is even more vital for coding agents than for human developers. Because CSS fails silently by design—ignoring invalid declarations, broken anchor references, or inactive scroll timelines without throwing exceptions—agents cannot easily verify or debug declarative features without expensive and brittle multi-modal screenshot loops. By following the Web Animations precedent (`Element.getAnimations()`, `AnimationEffect.getComputedTiming()`, `Animation.ready`), specifications turn opaque visual state into programmatic, machine-checkable DOM/CSSOM state that an agent can assert against directly in a headless test.

However, the principle also highlights where "developer-friendliness" must evolve for agentic DX. First, §10.7 accepts that JavaScript exception text should remain generic as long as developer console messages are detailed; for agents running automated test suites that catch thrown `DOMException` objects, generic exception messages obscure the failure unless the harness also streams CDP/BiDi console logs. Second, while humans often equate CSS debuggability with visual badges and overlays in browser DevTools, coding agents require debuggability to be exposed programmatically via standard JS introspection APIs or structured WebDriver BiDi diagnostics.

## Value as a Slide Example

§10.7 (`#debuggability` — "Ensure features are developer-friendly") is a top-tier (`5/5`, `clearly-useful`) slide example because both its title and its concrete example go straight to the thesis of "Agents are redefining DX. [How] should web standards adapt?". It allows the presenter to ask: when the developer is an AI agent, what makes a web standard "developer-friendly" and "debuggable"?

The principle's own canonical example—Web Animations—provides a compelling, concrete contrast on a slide. Because Web Animations specified programmatic introspection (`element.getAnimations()`, `effect.getComputedTiming()`) directly in the standard rather than leaving debugging entirely to browser-specific DevTools GUIs, an AI agent can deterministically verify and debug CSS animations and transitions in a headless Playwright test (`el.getAnimations()[0].playState`). Contrasting Web Animations with silent declarative CSS failures (such as broken CSS Anchor Positioning references or Scroll-Driven Animation timelines that fail without console errors or JS introspection APIs) gives W3C spec authors an actionable takeaway: build programmatic introspection and specific diagnostic messages into every declarative spec so agents can close their feedback loop without relying on pixel screenshots.
