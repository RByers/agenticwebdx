---
section: "2.6"
id: "feature-detect"
title: "New features should be detectable"
chapter: "2. API Design Across Languages"
url: "https://w3ctag.github.io/design-principles/#feature-detect"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Standardized feature detection helps agents safely bridge training-data cutoffs and runtime context differences (like SecureContext) without brittle UA sniffing, though silent fallbacks can occasionally mask hallucinated identifiers."
---

# §2.6 New features should be detectable

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §2.6 feature-detect — New features should be detectable: Standardized feature detection helps agents safely bridge training-data cutoffs and runtime context differences (like SecureContext) without brittle UA sniffing, though silent fallbacks can occasionally mask hallucinated identifiers.

- **URL:** https://w3ctag.github.io/design-principles/#feature-detect
- **Chapter:** 2. API Design Across Languages
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Standardized feature detection helps agents safely bridge training-data cutoffs and runtime context differences (like SecureContext) without brittle UA sniffing, though silent fallbacks can occasionally mask hallucinated identifiers.

## Principle Summary

W3C TAG §2.6 states that new web platform features should be programmatically detectable—both from JavaScript and, where appropriate, in the host language such as `@supports` in CSS—so authors can gracefully handle environments where the feature is unavailable. Crucially, a feature may be unavailable for different reasons (such as not yet being implemented in the user's browser, or being restricted to `[SecureContext]`), and a single feature-detection check should handle all of them uniformly so developers do not have to write separate branching logic for each scenario.

The principle also establishes clear boundaries between *feature availability* (whether the platform capability is exposed in the current context), *device availability* (whether required hardware is physically connected), and *user authorization* (whether permission has been granted), requiring separate mechanisms for each so apps can guide users appropriately. Finally, it notes that feature detection must be withheld when exposing availability would violate user needs or privacy invariants, such as private browsing mode (§2.9) or assistive technology usage (§2.11).

## Fit for Coding Agents

This principle aligns well with the strengths and constraints of LLM coding agents (`agent_fit: good`). Coding agents constantly operate across a temporal gap between their static training weights (or newly injected documentation skills) and the heterogeneous browser environments where their code runs. When an agent is asked to use a newer capability—such as View Transitions (`document.startViewTransition`), the Popover API (`'popover' in HTMLElement.prototype`), or CSS Anchor Positioning (`@supports (anchor-name: --a)`)—uniform feature detection provides a high-probability, low-token syntactic pattern for progressive enhancement. Without straightforward feature detection, LLMs frequently fall back on legacy training-data anti-patterns like brittle `navigator.userAgent` regular expressions that misclassify modern browser versions.

Equally valuable for agents is the requirement that all reasons for unavailability—such as an unimplemented API versus a missing `[SecureContext]`—collapse into the same detection check. Agents frequently generate and test code in varied environments (local HTTP dev servers, sandboxed iframes, headless test runners) and rarely anticipate every environmental precondition unless prompted. Having `navigator.clipboard` or `crypto.subtle` simply be absent in insecure contexts allows a single `if (navigator.clipboard)` guard to prevent unhandled exceptions across both older runtimes and non-HTTPS contexts. Furthermore, when agents debug UI or behavioral failures inside an automated browser loop (e.g., Playwright), programmatic detectability via `CSS.supports()` or JS property checks lets the agent directly query the runtime's capabilities rather than guessing why a feature failed to take effect.

There are two notable nuances for coding agents. First, while detecting new interfaces, methods, and CSS properties is straightforward, the web platform has historically struggled to make *sub-features*—such as new members in WebIDL input dictionaries—cleanly detectable. When humans had to write clever getter-trap hacks (like passing `{ get passive() { ... } }` to `addEventListener` to see if the browser read the property), agents either omit detection entirely or reproduce cargo-culted boilerplate inaccurately; explicit static capability APIs (like `CSS.supports()` or `HTMLScriptElement.supports()`) are far more ergonomic for agents. Second, because feature detection is designed to degrade gracefully when a check returns `false`, wrapping a *hallucinated* property or CSS descriptor in `if ('hallucinatedApi' in window)` or `@supports` will silently execute the fallback branch rather than failing loudly in the agent's test suite.

## Value as a Slide Example

As a TPAC slide example, §2.6 is a solid supporting illustration (`clearly-useful`, strength `3/5`) of how classic defensive web patterns interact with AI coding agents. It is not a 5/5 headline slide because much of the section covers end-user privacy boundaries (private browsing, assistive tech) and hardware vs. permission state separation, which apply identically regardless of who writes the code.

However, it offers a very concrete takeaway if discussed alongside API ergonomics: simple, declarative capability queries (`CSS.supports()`, `HTMLScriptElement.supports()`, `'prop' in Interface.prototype`) work great for agents, whereas indirect "side-effect" feature detection (like WebIDL dictionary getter traps) breaks down. Highlighting how uniform detectability helps agents bridge training-data cutoffs safely—while noting the tension that silent `@supports` / `in` fallbacks can hide hallucinated identifiers unless paired with static typecheckers—makes for a thoughtful nuance in a discussion on agentic DX.
