---
section: "6.17"
id: "prefer-existing-task-sources"
title: "Prefer existing task sources"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#prefer-existing-task-sources"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 1
verdict: "Purely internal specification-authoring and browser event-loop scheduling guidance that is invisible on the JavaScript API surface, with only a minor indirect benefit of reducing cross-browser task-ordering race conditions."
---

# §6.17 Prefer existing task sources

GREP_SUMMARY: slide_example=neither | strength=1/5 | agent_fit=neutral | §6.17 prefer-existing-task-sources — Prefer existing task sources: Purely internal specification-authoring and browser event-loop scheduling guidance that is invisible on the JavaScript API surface, with only a minor indirect benefit of reducing cross-browser task-ordering race conditions.

- **URL:** https://w3ctag.github.io/design-principles/#prefer-existing-task-sources
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 1/5
- **Verdict:** Purely internal specification-authoring and browser event-loop scheduling guidance that is invisible on the JavaScript API surface, with only a minor indirect benefit of reducing cross-browser task-ordering race conditions.

## Principle Summary

In the HTML event loop specification model, asynchronous work is queued as tasks onto conceptual "task sources" (such as the DOM manipulation, user interaction, or networking task sources), each associated with a task queue. Execution order is strictly guaranteed within a single task source, whereas the browser can choose which task queue to service next on each turn of the event loop.

§6.17 instructs specification authors to reuse HTML's generic or preexisting task sources and standard wrapper algorithms ("queue a global task", "queue an element task") rather than minting new spec-specific task sources, unless a feature's timing model genuinely requires isolation (such as the media element event task source aligning with media decoder timelines). Reusing existing task sources avoids imposing extra scheduling complexity and performance costs on browser engines while ensuring predictable, interoperable ordering of related tasks across implementations.

## Fit for Coding Agents

This principle is fundamentally neutral with respect to AI coding agents writing web application code because HTML task sources are an internal specification and browser-engine abstraction that is completely invisible on the JavaScript API surface. Neither human web developers nor LLM coding agents ever reference, import, or pass a specification task source (such as the DOM manipulation task source or networking task source) when invoking Web APIs. Instead, the principle regulates how specification editors write normative algorithms ("queue a global task" / "queue an element task") and keeps browser engine event-loop schedulers from accumulating unnecessary queue management overhead.

To the limited extent that this principle indirectly touches web code at runtime, it provides a minor, second-order benefit by improving deterministic event ordering across browsers. Because the HTML event loop guarantees FIFO ordering within a single task source but leaves ordering across different task sources up to each browser's scheduler, minting unnecessary task sources introduces implementation-defined ordering between related asynchronous callbacks. Coding agents rely heavily on statistical priors about callback execution order and typically validate their code in a single headless browser (or without a live browser at all), making cross-browser event-loop race conditions particularly difficult for an agent to anticipate or debug. Reusing existing task sources reduces these subtle cross-engine timing divergences, and also simplifies normative patterns for agents assisting spec editors or writing Web Platform Tests (WPT), though this remains internal spec hygiene rather than a developer experience concern.

## Value as a Slide Example

§6.17 is not suitable for a TPAC slide (1/5 strength) and falls squarely into `neither`. Discussing it in a session about how web standards DX should adapt to AI coding agents would require explaining internal HTML spec-editing mechanics ("queue a global task" vs. minting a new task source) that do not appear in any JavaScript API signature, developer documentation, or agent prompt. Even if contrasted with developer-facing scheduling APIs like `scheduler.postTask()`, HTML task sources are purely specification prose and browser scheduling plumbing, offering no actionable insight into how API ergonomics differ between human developers and coding agents.
