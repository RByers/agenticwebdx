---
section: "5.2"
id: "js-rtc"
title: "Preserve run-to-completion semantics"
chapter: "5. JavaScript Language"
url: "https://w3ctag.github.io/design-principles/#js-rtc"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Run-to-completion guarantees match LLM training priors for synchronous JavaScript invariants and protect agentic test-and-fix loops from non-deterministic race conditions."
---

# §5.2 Preserve run-to-completion semantics

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §5.2 js-rtc — Preserve run-to-completion semantics: Run-to-completion guarantees match LLM training priors for synchronous JavaScript invariants and protect agentic test-and-fix loops from non-deterministic race conditions.

- **URL:** https://w3ctag.github.io/design-principles/#js-rtc
- **Chapter:** 5. JavaScript Language
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Run-to-completion guarantees match LLM training priors for synchronous JavaScript invariants and protect agentic test-and-fix loops from non-deterministic race conditions.

## Principle Summary

W3C TAG Principle §5.2 ("Preserve run-to-completion semantics") requires that whenever state changes originate outside the currently running JavaScript execution context—such as the HTML parser receiving network chunks, `img.width` updating as image data loads, Gamepad button states changing, `scrollTop` updating during visual scrolling, or concurrent state changes across windows in APIs like `LockManager`—those changes must only be propagated to JavaScript between tasks (by queuing a task or as part of updating the rendering), never in the middle of a synchronous task or between microtasks.

Unlike lower-level multithreaded languages like C++ or Rust, JavaScript provides a single-threaded illusion where authors can assume data accessible to a running function will not change unexpectedly unless mutated synchronously by developer code. The principle allows only narrow, well-justified exceptions where observing live external progression is the whole point of the API—such as wall-clock or performance timers (`Date.now()`, `performance.now()`), cooperative work-slicing deadlines (`IdleDeadline.timeRemaining()`), and user-protection states like transient user activation (`navigator.userActivation.isActive`).

## Fit for Coding Agents

This principle is a strong, positive fit (`good`) for AI coding agents because it upholds two properties that LLMs depend on heavily when writing and debugging web applications: local invariant stability within a context window and deterministic behavior in automated test loops.

First, LLM coding agents have an overwhelmingly strong statistical prior, learned from billions of lines of single-threaded JavaScript in their training corpora, that observable properties do not change mid-function unless mutated by the running script itself. When an agent writes code that checks `if (img.width > 0)` before using `img.width` in an aspect-ratio calculation, reads `element.scrollTop` across several lines, or inspects `navigator.getGamepads()`, it assumes sequential consistency without defensive snapshotting or locking. If a new Web API violated run-to-completion by exposing live mutations from a background network, parser, or compositor thread in the middle of a task or between microtasks, coding agents would systematically generate race-prone code because mid-task external mutation contradicts the fundamental JavaScript execution model encoded in their weights.

Second, preserving run-to-completion is critical for the agentic feedback loop. Autonomous coding agents rely on iterative test-and-repair cycles using headless browsers (such as Playwright or WebDriver) to verify their work. While agents excel at fixing loud, deterministic failures with clear stack traces, they struggle with timing-dependent race conditions ("Heisenbugs") that depend on background thread scheduling and only fail intermittently. By requiring external state updates (network loads, DOM parsing, compositor scrolling, cross-window lock state) to be queued as discrete tasks or applied during rendering updates, `js-rtc` keeps state transitions reproducible and prevents flaky failures from Sending agents into unproductive debugging spirals.

## Value as a Slide Example

This principle is a `clearly-useful` slide candidate with a moderate strength of `3/5`. On a slide about TAG principles that benefit coding agents, it provides concrete, relatable examples—such as `img.width` not changing mid-function when network image data arrives, `scrollTop` staying constant during a synchronous block even while smooth scrolling occurs on the compositor thread, and `LockManager` avoiding synchronous cross-window state queries—to show how browser task boundaries shield generated code from C++/Rust-style data races. Emphasizing how non-deterministic race conditions poison autonomous test-and-fix loops gives a fresh agentic angle to a classic principle.

However, it earns a `3/5` rather than a `5/5` because run-to-completion is already an uncontroversial, foundational guarantee of the JavaScript event loop that benefits human developers and coding agents for largely the same reasons. Unlike API surface design principles where human typing ergonomics and LLM token/hallucination dynamics pull in different directions, no spec author is considering abandoning run-to-completion because of AI agents; thus it works best as a supporting point illustrating why strict platform invariants remain essential for reliable agentic engineering rather than a standalone headline debate.
