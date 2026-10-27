---
section: "8.5"
id: "error-types"
title: "Use Error or DOMException for errors"
chapter: "8. Web IDL, Types, and Units"
url: "https://w3ctag.github.io/design-principles/#error-types"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Standardizing on Error and DOMException aligns directly with LLM error-handling priors (such as `instanceof Error` narrowing) and ensures rich stack traces and messages in automated agent feedback loops."
---

# §8.5 Use Error or DOMException for errors

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §8.5 error-types — Use Error or DOMException for errors: Standardizing on Error and DOMException aligns directly with LLM error-handling priors (such as `instanceof Error` narrowing) and ensures rich stack traces and messages in automated agent feedback loops.

- **URL:** https://w3ctag.github.io/design-principles/#error-types
- **Chapter:** 8. Web IDL, Types, and Units
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Standardizing on Error and DOMException aligns directly with LLM error-handling priors (such as `instanceof Error` narrowing) and ensures rich stack traces and messages in automated agent feedback loops.

## Principle Summary

W3C TAG Design Principle §8.5 ("Use Error or DOMException for errors") states that web APIs must represent errors as standard ECMAScript `Error` objects (such as `TypeError` or `RangeError`) or `DOMException` instances, regardless of whether the error is surfaced as a thrown synchronous exception, a Promise rejection reason, or a property on an object or event (such as `IDBRequest.error` or `ErrorEvent.error`).

The principle exists to prevent specifications from inventing bespoke, non-standard error interfaces or opaque numeric error codes (as older APIs like Geolocation's `GeolocationPositionError` or `<video>`'s `MediaError` did), ensuring that developers and tooling always get `instanceof Error` compatibility, standard `.name` and `.message` properties, and stack traces.

## Fit for Coding Agents

This principle is a strong, unambiguous fit (`good`) for AI coding agents because it aligns web platform failure surfaces with the universal error-handling idioms ingrained in LLM training data. In modern JavaScript and TypeScript (especially with `useUnknownInCatchVariables` enabled by default in strict TypeScript), coding agents almost universally narrow caught exceptions and rejected promises using `if (err instanceof Error) { ... }`. Because `DOMException` inherits from `Error` in modern Web IDL, any API that follows §8.5 works seamlessly with this default agent-generated guard across synchronous throws, `await` rejections, and `.error` properties. By contrast, legacy web APIs that invented bespoke non-`Error` interfaces—such as `GeolocationPositionError` or `HTMLMediaElement.error` (`MediaError`)—cause `err instanceof Error` to evaluate to `false`, leading agent-written code to silently bypass error-handling branches or swallow diagnostic details into generic fallback strings.

Furthermore, standardizing on `Error` and `DOMException` reduces hallucination and improves the automated test/debug feedback loop. When legacy APIs rely on bespoke interfaces with numeric `.code` constants (e.g., `MediaError.MEDIA_ERR_SRC_NOT_SUPPORTED = 4` or `GeolocationPositionError.PERMISSION_DENIED = 1`), agents frequently hallucinate `.name` properties that do not exist or mix up numeric constants. Even worse, in headless browser test runners (Playwright, Vitest) and console log capture, standard `Error` and `DOMException` objects automatically format with `.name`, `.message`, and `.stack` traces, whereas non-`Error` Web IDL interfaces often stringify as `[object GeolocationPositionError]` or serialize via `JSON.stringify` as `{}` (because Web IDL getter attributes live on the prototype), starving the agent of actionable error feedback and requiring extra debugging turns.

## Value as a Slide Example

§8.5 is a solid `clearly-useful` example (`3/5` strength) because it offers an immediately recognizable, concrete failure mode in agent-written TypeScript: wrapping `navigator.geolocation.getCurrentPosition` in a Promise and catching it with the standard LLM-generated `if (err instanceof Error)` guard, which fails at runtime because `GeolocationPositionError` is not an `Error` instance and serializes as `{}` or `[object GeolocationPositionError]` in test logs.

It rates a `3/5` rather than a `5/5` headline example because requiring errors to be `Error` instances is baseline language hygiene where human DX and agent DX are already completely aligned without surprising tension. On a slide, it works best paired with §8.6 (`complex-error-information`) to show how agents benefit from standard `Error`/`DOMException` hierarchies with machine-readable properties during autonomous test-and-fix loops.
