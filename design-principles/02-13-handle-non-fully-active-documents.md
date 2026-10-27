---
section: "2.13"
id: "handle-non-fully-active-documents"
title: "Handle non-fully-active documents"
chapter: "2. API Design Across Languages"
url: "https://w3ctag.github.io/design-principles/#handle-non-fully-active-documents"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Failing fast with InvalidStateError and aborting in-flight operations with AbortError prevents hung promises, stuck browser prompts, and GC-dependent flakiness in agent test loops, though the rule is too niche and spec-internal to feature on a TPAC slide."
---

# §2.13 Handle non-fully-active documents

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §2.13 handle-non-fully-active-documents — Handle non-fully-active documents: Failing fast with InvalidStateError and aborting in-flight operations with AbortError prevents hung promises, stuck browser prompts, and GC-dependent flakiness in agent test loops, though the rule is too niche and spec-internal to feature on a TPAC slide.

- **URL:** https://w3ctag.github.io/design-principles/#handle-non-fully-active-documents
- **Chapter:** 2. API Design Across Languages
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Failing fast with InvalidStateError and aborting in-flight operations with AbortError prevents hung promises, stuck browser prompts, and GC-dependent flakiness in agent test loops, though the rule is too niche and spec-internal to feature on a TPAC slide.

## Principle Summary

This principle directs specification authors to explicitly define how Web APIs behave when their relevant global object's associated `Document` ceases to be "fully active"—most commonly when an `<iframe>` is removed from the DOM or navigated away while another frame still holds references to its JS objects or while an asynchronous operation is in progress. Without explicit lifecycle rules, background tasks may keep running on dead documents, browser-mediated UI (such as payment sheets, WebAuthn prompts, or file pickers) may remain orphaned on screen, and engines may diverge based on when garbage collection happens to run.

To ensure predictable, interoperable behavior, the TAG establishes three concrete rules: (1) if the document is already non-fully active at call time, fail immediately with an `InvalidStateError` `DOMException`; (2) if the document becomes non-fully active during an asynchronous operation, abort the operation, dismiss any open browser-mediated UI, and reject with `AbortError`; and (3) when queued tasks execute (such as firing events or settling promises), perform an explicit early-exit check for document activity rather than relying on garbage collection to clean up pending work.

## Fit for Coding Agents

This principle is a good fit for coding agents because it turns some of the worst failure modes for automated agent feedback loops—indefinitely hanging promises, orphaned modal browser UI, and non-deterministic GC timing bugs—into loud, deterministic exceptions. When an LLM coding agent iterates on a web application using a headless browser (such as Playwright or WebDriver), an unsettled promise from an iframe teardown (e.g., an aborted OAuth flow, `navigator.credentials.get()`, `PaymentRequest.show()`, or `showOpenFilePicker()`) causes the test runner to stall until a generic timeout expires, providing zero diagnostic signal about which API call hung. By mandating that in-flight operations settle immediately with `AbortError` and dismiss browser UI when a frame detaches, the platform gives the agent an immediate, catchable rejection with a clear stack trace.

Similarly, requiring immediate `InvalidStateError` failures when invoking methods on objects belonging to a detached document aligns well with agent debugging ergonomics. Agents frequently generate SPA teardown logic, dynamic iframe sandboxes, or test harnesses where a callback retains a reference to a child frame's window or DOM object slightly longer than the frame stays mounted. Immediate failure with standardized `DOMException` names (`InvalidStateError` at call time, `AbortError` mid-flight) matches strong statistical priors in LLM training data and surfaces lifecycle bugs at the exact point of misuse. Finally, forbidding specifications from relying on garbage collection for task cancellation eliminates a notorious source of flaky tests that otherwise cause coding agents to hallucinate unrelated race-condition fixes.

That said, the day-to-day impact on application-level code generation is modest because most web code operates within a single active document. The principle primarily does its heavy lifting inside browser engine implementations and specification algorithms so that application developers—human or agent—do not have to write defensive frame-liveness polling around every asynchronous web API.

## Value as a Slide Example

Despite being helpful to agent test-and-debug loops, this principle is neither a strong positive nor negative headline example for a TPAC breakout slide (2/5). Its primary audience is spec editors writing algorithmic steps for cross-frame edge cases and browser-mediated UI dismissal (such as `PaymentRequest`, WebAuthn `navigator.credentials.get()`, or file pickers inside detached `<iframe>` elements), rather than web developers or agents choosing how to structure application code.

On a slide deck with limited space, explaining what a "non-fully-active document" is (`iframe` detachment or navigation while cross-realm object references persist) takes too much setup for a relatively specialized lifecycle guarantee. The core takeaway that does matter for agents—that APIs should fail loudly and deterministically rather than hanging promises or relying on garbage collection—is much more directly illustrated by broader error-handling and predictability principles.
