---
section: "1.7"
id: "new-features"
title: "Add new capabilities with care"
chapter: "1. Principles behind design of Web APIs"
url: "https://w3ctag.github.io/design-principles/#new-features"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Integrating new capabilities into existing extension points leverages agents' statistical priors and prevents fragmented API bloat, though it is too brief and high-level to be a headline slide example."
---

# §1.7 Add new capabilities with care

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §1.7 new-features — Add new capabilities with care: Integrating new capabilities into existing extension points leverages agents' statistical priors and prevents fragmented API bloat, though it is too brief and high-level to be a headline slide example.

- **URL:** https://w3ctag.github.io/design-principles/#new-features
- **Chapter:** 1. Principles behind design of Web APIs
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Integrating new capabilities into existing extension points leverages agents' statistical priors and prevents fragmented API bloat, though it is too brief and high-level to be a headline slide example.

## Principle Summary

W3C TAG §1.7 advises specification authors to introduce new web platform capabilities thoughtfully by considering how they fit alongside existing functionality and content. Rather than inventing isolated mechanisms from scratch, spec authors should take advantage of the Web's built-in extension points (such as HTML's extensibility hooks, CSS selectors/properties, or established DOM interfaces) and integrate new features with similar capabilities that already exist on the platform.

Crucially, the principle also pushes back against the reflex to treat every existing Web behavior as immutable. When the cleanest, most integrated design would require modifying or removing an existing behavior rather than purely bolting on additive workarounds, authors should not assume such a change is impossible—they should first investigate actual compatibility constraints (pointing forward to §1.8, *Prioritize compatibility when changing or removing features*).

## Fit for Coding Agents

This principle aligns well (`good`) with how LLM coding agents learn, generalize, and generate web code. Agents rely heavily on structural patterns and statistical priors learned across large codebases. When a new capability plugs into an established extension point—such as accepting an `AbortSignal` in an options dictionary (`fetch()`, `addEventListener()`), registering a new entry type on `PerformanceObserver`, or extending `Permissions.query()`—an agent can immediately transfer its existing mental model and boilerplate patterns (cleanup, error handling, TypeScript types) with minimal hallucination risk, even when the specific new feature has sparse coverage in its pre-training data.

Conversely, when spec authors fail to integrate with existing capabilities—either by creating a parallel, slightly different API silo or by assuming they can only make purely additive changes—the platform accumulates near-duplicate APIs and legacy workarounds (e.g., `substr` vs. `substring` vs. `slice`, or multiple overlapping observer/event patterns). Coding agents are notoriously susceptible to "API splitting" when multiple generations of an API coexist: they frequently blend options from one API into another or default to older, higher-frequency workarounds in their training corpus. Willingness to check whether an awkward existing behavior can be updated or removed in-place prevents the proliferation of additive "v2" flags and footguns.

There is one subtle nuance for agents: browsers evaluate whether a breaking change or removal is safe by measuring live runtime usage across the web (e.g., via UseCounters), whereas LLMs also have "training-corpus inertia" from historical tutorials, Stack Overflow threads, and archived repositories. Even so, when an existing edge case is obscure enough that live websites do not depend on it, changing it to match the intuitive, integrated design usually brings the platform closer to what an LLM's statistical priors would naturally predict. The main risk to avoid when applying this principle is overloading a single existing function with complex positional polymorphism rather than structured extension points (such as options objects or sub-interfaces).

## Value as a Slide Example

Despite being a positive fit for agents, §1.7 is rated `neither` (`2/5`) as a candidate slide example for TPAC. At just four sentences long, it functions primarily as a high-level framing section and a bridge to §1.8 (*Prioritize compatibility when changing or removing features*) and HTML's extensibility guidelines. On a slide, "Add new capabilities with care" reads as generic architectural advice that applies equally to any software ecosystem rather than a sharp, provocative insight about how AI coding agents change Web DX.

If the presentation touches on the tension between additive API sprawl (e.g., bolting on parallel APIs vs. extending `AbortSignal` or `PerformanceObserver`) and clean platform evolution, more specific principles—such as §1.8 on compatibility vs. breaking changes, or principles covering API consistency and naming conventions—provide much more concrete hooks and vivid Web API examples for the audience.
