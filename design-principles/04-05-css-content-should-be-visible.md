---
section: "4.5"
id: "css-content-should-be-visible"
title: "Content should be viewable and accessible by default"
chapter: "4. Cascading Style Sheets (CSS)"
url: "https://w3ctag.github.io/design-principles/#css-content-should-be-visible"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Safe CSS defaults that keep content visible, scrollable, and in the accessibility tree protect coding agents from silent visual and accessibility data loss that passes DOM and console checks."
---

# §4.5 Content should be viewable and accessible by default

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §4.5 css-content-should-be-visible — Content should be viewable and accessible by default: Safe CSS defaults that keep content visible, scrollable, and in the accessibility tree protect coding agents from silent visual and accessibility data loss that passes DOM and console checks.

- **URL:** https://w3ctag.github.io/design-principles/#css-content-should-be-visible
- **Chapter:** 4. Cascading Style Sheets (CSS)
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Safe CSS defaults that keep content visible, scrollable, and in the accessibility tree protect coding agents from silent visual and accessibility data loss that passes DOM and console checks.

## Principle Summary

This principle states that CSS properties and layout systems (typically values of the `display` property) must be designed so that content remains viewable, accessible, and usable by default. In CSS design, this is often framed as preventing accidental "data loss": applying a layout mode or styling property should not silently clip content, push it into unscrollable regions, collapse boxes to zero size, or strip elements from the accessibility tree unless the author explicitly opts into hiding or clipping behavior.

For human developers and end users, this guarantees resilience across unpredictable viewport sizes, zoom levels, localization string lengths, and assistive technologies. Concrete examples include `overflow` defaulting to `visible`, Flexbox and Grid items defaulting to `min-width: auto` / `min-height: auto` so text does not shrink into illegibility, `safe` alignment fallback that keeps overflowing content within scrollable bounds, and ensuring `display: contents` removes only the visual box without stripping the element's subtree from the accessibility tree.

## Fit for Coding Agents

This principle is a good fit for AI coding agents because visual clipping and accessibility regressions are among the hardest failure modes for an agent to detect in its feedback loop. CSS does not throw runtime exceptions or log console errors when content is clipped off-screen, overlapped, or pushed into an unscrollable overflow region. Moreover, if an agent verifies its work using unit tests or basic DOM queries (such as asserting that a node exists in the DOM and contains expected text), those tests pass even when the element is visually unreachable to a human user. By ensuring CSS layout systems keep content viewable and scrollable by default, the platform prevents agents from shipping silent UI data loss when they omit defensive sizing or overflow rules.

Furthermore, "accessible by default" directly affects how modern coding and testing agents perceive the web. Agents frequently inspect pages using accessibility tree snapshots (such as Playwright ARIA snapshots or DevTools accessibility trees) rather than expensive, high-variance pixel screenshots across every viewport. When a CSS property or `display` value inadvertently drops elements from the accessibility tree (as historically happened with `display: contents` or mishandled visibility rules), the content becomes invisible not only to screen reader users, but also to the agent's own verification harness.

There is one instructive nuance where this principle creates a secondary friction point for agents: to keep content viewable by default, Flexbox and CSS Grid specify `min-width: auto` and `min-height: auto` on items so they refuse to shrink smaller than their minimum content size. While this prevents silent clipping, it causes the notorious flex/grid blowout bug when long unbroken text, code blocks, or nested scroll containers expand a track unexpectedly unless the author adds `min-width: 0`. Coding agents frequently fall into this trap and have to add `min-width: 0` on follow-up iterations. Even so, failing via visible layout expansion is far easier for a visual or bounding-box check to catch than silently hiding content.

## Value as a Slide Example

As a TPAC slide example, this principle is `clearly-useful` with a moderate strength (3/5). Its single-sentence text in the TAG document is brief and high-level, making it less self-explanatory as a standalone headline slide than principles about concrete JS/HTML API shapes, but it provides strong supporting evidence for two key agentic DX themes.

First, CSS "data loss" is a silent failure in DOM-based agent loops: unlike JavaScript errors that fail loudly in the console, CSS layout clipping leaves the DOM intact while hiding content from the user, and the `min-width: auto` default in Flexbox/Grid illustrates how CSS chooses a visible layout blowout over silent content truncation. Second, accessibility trees are now agent perception trees: keeping content accessible by default (avoiding pitfalls like historical `display: contents` accessibility tree bugs) preserves the exact ARIA/accessibility snapshot representation that coding and browser agents rely on to inspect, test, and interact with web pages.
