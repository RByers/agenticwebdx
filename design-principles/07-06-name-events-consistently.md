---
section: "7.6"
id: "name-events-consistently"
title: "Name events in a consistent pattern"
chapter: "7. Event Design"
url: "https://w3ctag.github.io/design-principles/#name-events-consistently"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Consistent present-tense event naming aligns with LLM analogical priors on new APIs and prevents silent runtime failures in string-based addEventListener calls."
---

# §7.6 Name events in a consistent pattern

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §7.6 name-events-consistently — Name events in a consistent pattern: Consistent present-tense event naming aligns with LLM analogical priors on new APIs and prevents silent runtime failures in string-based addEventListener calls.

- **URL:** https://w3ctag.github.io/design-principles/#name-events-consistently
- **Chapter:** 7. Event Design
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Consistent present-tense event naming aligns with LLM analogical priors on new APIs and prevents silent runtime failures in string-based addEventListener calls.

## Principle Summary

This principle specifies that new web platform event names should always use verbs in the present tense rather than the past tense, explicitly calling out `DOMContentLoaded` as an antipattern that new specifications must not emulate. It complements the broader naming principles in §12 (which mandate lowercase, unseparated event names like `beforeunload` or `toggle` rather than mixed-case or past-tense forms).

For human developers, this reduces cognitive load and guesswork when wiring up event listeners across different APIs. Without a consistent grammatical convention, developers constantly have to look up whether an event is named `close` or `closed`, `navigate` or `navigated`, or `toggle` or `toggled`.

## Fit for Coding Agents

This principle is a good fit for AI coding agents because LLMs rely heavily on pattern completion and analogical transfer when generating code for newer or less common Web APIs. While an LLM will never misspell `DOMContentLoaded`—because that specific antipattern appears millions of times in pre-training corpora—design principles govern new features that sit near or beyond an agent's training cutoff, or in the long tail of low-frequency APIs (such as `CloseWatcher`, the Navigation API, Popover, or View Transitions). When a platform strictly follows a present-tense convention (`close`, `cancel`, `navigate`, `toggle`), an agent inferring an event name from minimal context or a brief API summary will predict the right token with high probability.

Consistency in event naming is especially critical for agents because `EventTarget.prototype.addEventListener` fails silently at runtime when given an invalid event name. If an agent hallucinates a past-tense event name—such as `watcher.addEventListener('closed', ...)` instead of `'close'`, or `navigation.addEventListener('navigated', ...)` instead of `'navigate'` (often influenced by framework conventions like React's `onClosed` or legacy media/storage events like `loadeddata`, `ended`, and `upgradeneeded`)—the browser throws no exception and logs no warning. The listener simply never fires. In an agentic coding loop, silent no-ops are far harder to diagnose and self-correct than loud syntax or TypeError failures, unless an end-to-end test happens to exercise that exact event path and fail on a missing side effect.

Even in TypeScript codebases where `HTMLElementEventMap` can catch mistyped event strings at compile time, many newer APIs, custom `EventTarget` subclasses, or plain JavaScript projects lack exhaustive mapped string literal types in the agent's environment. Upholding strict present-tense consistency across all specs reduces hallucination pressure before a typechecker or test runner even enters the loop.

## Value as a Slide Example

This principle is a `clearly-useful` candidate example (`3/5` strength) because it counters a common misconception at standards bodies: the assumption that "LLMs can just memorize platform quirks, so naming consistency matters less for agents than for humans." While that holds true for famous historical quirks like `DOMContentLoaded` (which is baked deeply into model weights), it fails completely for newly standardized APIs where agents generalize from platform-wide statistical priors.

On a TPAC slide, it works well as a concise supporting point pairing naming consistency with silent failure modes: because `addEventListener("toggled", fn)` is a silent runtime no-op rather than a loud error, inconsistent verb tenses across web specs (e.g., `load`/`toggle`/`close` vs `DOMContentLoaded`/`ended`/`loadedmetadata`/`upgradeneeded`) bait agents into plausible-looking hallucinations that silently break application logic. However, because it is a narrow micro-level naming rule rather than a broader architectural pattern, it is best grouped with other naming/consistency principles rather than featured as a standalone headline slide.
