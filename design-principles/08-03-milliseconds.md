---
section: "8.3"
id: "milliseconds"
title: "Use milliseconds for time measurement"
chapter: "8. Web IDL, Types, and Units"
url: "https://w3ctag.github.io/design-principles/#milliseconds"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Enforcing a single time unit across Web APIs aligns with LLM statistical priors and prevents silent 1000x unit-mismatch bugs that neither TypeScript nor runtime exceptions can catch."
---

# §8.3 Use milliseconds for time measurement

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §8.3 milliseconds — Use milliseconds for time measurement: Enforcing a single time unit across Web APIs aligns with LLM statistical priors and prevents silent 1000x unit-mismatch bugs that neither TypeScript nor runtime exceptions can catch.

- **URL:** https://w3ctag.github.io/design-principles/#milliseconds
- **Chapter:** 8. Web IDL, Types, and Units
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Enforcing a single time unit across Web APIs aligns with LLM statistical priors and prevents silent 1000x unit-mismatch bugs that neither TypeScript nor runtime exceptions can catch.

## Principle Summary

This principle states that Web APIs accepting or returning a time measurement should always express that value in milliseconds, following the convention established by `setTimeout()` and `Date`. Even when another unit (such as seconds or nanoseconds) might feel more natural for a specific domain, using milliseconds everywhere ensures interoperability across APIs so developers do not have to remember per-API units or write unit-conversion glue code. For high-resolution measurements, the principle specifies using fractional milliseconds as a floating-point number (`DOMHighResTimeStamp`) rather than integer nanoseconds.

For human developers and browser engines, this establishes a single mental model for time across the platform. A timestamp or duration produced by one API can be compared with or passed directly into another without mental bookkeeping or off-by-1000 conversion errors.

## Fit for Coding Agents

This principle is a strong fit (`good`) for AI coding agents because it eliminates a particularly insidious failure mode in LLM-generated code: silent unit mismatches on bare numeric types. In JavaScript and TypeScript, a duration or timestamp is typed simply as `number` (`double` or `unsigned long` in Web IDL). Because the type system carries no unit dimension, passing `5` (intending 5 seconds) to an API that expects `5000` (milliseconds)—or vice versa—produces no TypeScript compilation error, no linter warning, and no runtime `TypeError`. In an agentic feedback loop, the code compiles cleanly and executes without throwing, causing silent behavioral bugs (such as an animation finishing in 0.3ms instead of 300ms, or an `AbortSignal.timeout(10)` aborting almost immediately) that automated tests frequently miss.

By holding the line on milliseconds across the platform—spanning `setTimeout()`, `Date.now()`, `performance.now()`, `requestAnimationFrame()`, `AbortSignal.timeout()`, and the Web Animations API (`element.animate(keyframes, 300)`)—the web platform gives LLMs a reliable statistical prior. Conversely, the handful of Web APIs that deviate from this principle and use seconds—most notably `HTMLMediaElement.currentTime` / `duration` and the Web Audio API's `AudioContext.currentTime`—are notorious traps where coding agents routinely hallucinate `* 1000` or omit it when bridging media playback with timers or UI animations.

The note favoring floating-point fractional milliseconds (`DOMHighResTimeStamp`) over integer nanoseconds also benefits coding agents. Introducing integer nanoseconds in Web IDL would require `BigInt` in JavaScript, creating friction and runtime `TypeError: Cannot mix BigInt and other types` exceptions whenever an agent combines high-resolution deltas with standard millisecond timestamps or math helpers (`Math.min`, `Math.max`). Keeping all time measurements in the same `number` space and unit minimizes glue code and token overhead.

## Value as a Slide Example

This principle is a strong (`4/5`), `clearly-useful` slide example for a TPAC session on agentic DX because it cleanly illustrates why platform-wide consistency rules matter even more when errors fail silently in an agent's verification loop. While agents can easily recover from hallucinated method names or incompatible object shapes as soon as TypeScript or the browser console reports an error, a 1000x unit error on an untyped `number` sails past static checks and headless browser runs.

On a slide, it offers a crisp, relatable comparison between APIs that follow §8.3 (`AbortSignal.timeout(5000)`, `element.animate(..., { duration: 300 })`, `performance.now()`) and the platform's famous exceptions (`video.currentTime = 5`, `audioCtx.currentTime + 0.5`, CSS `animation-duration: 0.3s`), while also teeing up a constructive standards discussion: when bare numbers are used, strict unit uniformity is essential, and where multiple units are unavoidable, standards should prefer self-describing types like `Temporal.Duration` or explicit unit suffixes in dictionary keys.
