---
section: "10.1"
id: "polyfills"
title: "Enable polyfills for new features"
chapter: "10. Other API Design Considerations"
url: "https://w3ctag.github.io/design-principles/#polyfills"
agent_fit: "mixed"
slide_example: "neither"
example_strength: 2
verdict: "Polyfillability and canonical reference polyfills help coding agents target modern standard APIs across browser rollout gaps, but polyfills also cut against agent ergonomics via stale polyfill bloat in training data and agents' tendency to hallucinate fragile inline monkey-patches."
---

# §10.1 Enable polyfills for new features

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=mixed | §10.1 polyfills — Enable polyfills for new features: Polyfillability and canonical reference polyfills help coding agents target modern standard APIs across browser rollout gaps, but polyfills also cut against agent ergonomics via stale polyfill bloat in training data and agents' tendency to hallucinate fragile inline monkey-patches.

- **URL:** https://w3ctag.github.io/design-principles/#polyfills
- **Chapter:** 10. Other API Design Considerations
- **Agent-Fit:** mixed
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Polyfillability and canonical reference polyfills help coding agents target modern standard APIs across browser rollout gaps, but polyfills also cut against agent ergonomics via stale polyfill bloat in training data and agents' tendency to hallucinate fragile inline monkey-patches.

## Principle Summary

Section 10.1 ("Enable polyfills for new features") summarizes the W3C TAG Finding on Polyfills and the Evolution of the Web. It advises specification authors that while being polyfillable is not strictly required for every web platform feature (since some depend on low-level browser or OS capabilities), designing features so they can be polyfilled in userland code is highly beneficial, new features must be deterministically detectable at runtime (§2.6), and polyfill development should be actively encouraged alongside new specifications.

For human developers and browser vendors, this principle exists to bridge the multi-year adoption gap between initial specification incubation and universal browser support. When a new API can be faithfully shimmed and cleanly detected, web developers can write standard-conformant code against the future API immediately, giving standards bodies early real-world feedback while preventing cross-browser fragmentation.

## Fit for Coding Agents

This principle is a mixed fit for AI coding agents because polyfills both solve and create acute failure modes in LLM-assisted web development. On the positive side, coding agents face a dual lag: their pre-training weights trail behind newly shipped web standards, and even when grounded via documentation or skills to use a modern standard API (such as `Temporal`, `URLPattern`, the `Sanitizer` API, or Invoker Commands with `command`/`commandfor`), target browsers or headless test environments may not yet support it universally. When a feature is cleanly detectable (`'URLPattern' in globalThis`, `CSS.supports(...)`) and backed by an official, spec-compliant polyfill (e.g., `@js-temporal/polyfill`, `urlpattern-polyfill`), an agent can emit clean, standard-conformant code against a single canonical API shape rather than generating tangled cross-browser fallback branches. Furthermore, encouraging official polyfill development alongside specs gives agents an executable reference implementation and type definitions they can inspect or bundle, and spec authors themselves can use coding agents to synthesize and maintain spec-compliant polyfills directly from specification algorithms and Web Platform Tests (WPT).

On the negative side, because generating JavaScript glue is nearly zero-cost for an LLM, agents that encounter a missing or unsupported browser API in their execution feedback loop frequently attempt to "polyfill" it inline by monkey-patching globals (`window`, `Element.prototype`, `Navigator.prototype`). These ad-hoc agent-generated shims typically implement only the superficial happy path and silently violate spec edge cases, security boundaries, accessibility semantics, or layout/timing invariants—particularly when a feature is only partially polyfillable (such as CSS Anchor Positioning, View Transitions, or top-layer rendering).

Additionally, LLM training corpora are heavily polluted with historical "zombie polyfills" (`core-js`, `regenerator-runtime`, `whatwg-fetch`, `intersection-observer`, vendor-prefixed shims) for features that have been universally supported in Baseline browsers for years. Without explicit Baseline grounding, agents routinely over-inject obsolete polyfill dependencies or unnecessary feature-detection branches. Finally, if "enable polyfills" is used as an excuse to ship only low-level imperative primitives ("let userland polyfill it") rather than high-level declarative HTML/CSS features, agents end up repeatedly synthesizing verbose, inconsistent JavaScript glue across projects instead of emitting concise, checkable native APIs.

## Value as a Slide Example

Section 10.1 is neither a strong `clearly-useful` nor `clearly-harmful` headline slide example (2/5). In the TAG Design Principles document, §10.1 is a brief three-bullet pointer section whose most concrete API design requirement—making features deterministically detectable—is already covered directly in §2.6 ("New features should be detectable"), while its primary purpose is managing cross-browser rollout skew across end-user devices regardless of whether a human or an agent authored the code.

While it does not belong on a headline slide of API design rules to keep or discard for agents, the surrounding polyfill lifecycle offers a nuanced side observation: standards groups can use coding agents to co-develop official, WPT-verified reference polyfills (like `@js-temporal/polyfill` or `urlpattern-polyfill`) so agents never try to invent broken inline monkey-patches, while machine-readable Baseline metadata is critical to stop agents from perpetuating obsolete polyfill bloat from their training data.
