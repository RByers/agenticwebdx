---
section: "8.4"
id: "times-and-dates"
title: "Use the appropriate type to represent times and dates"
chapter: "8. Web IDL, Types, and Units"
url: "https://w3ctag.github.io/design-principles/#times-and-dates"
agent_fit: "mixed"
slide_example: "clearly-harmful"
example_strength: 3
verdict: "Banning mutable JS Date objects avoids classic reference-mutation and equality footguns, but representing timestamps as bare numeric DOMHighResTimeStamp values erases time-origin and unit metadata, inviting silent monotonic-vs-epoch bugs that nominal Temporal types would catch."
---

# §8.4 Use the appropriate type to represent times and dates

GREP_SUMMARY: slide_example=clearly-harmful | strength=3/5 | agent_fit=mixed | §8.4 times-and-dates — Use the appropriate type to represent times and dates: Banning mutable JS Date objects avoids classic reference-mutation and equality footguns, but representing timestamps as bare numeric DOMHighResTimeStamp values erases time-origin and unit metadata, inviting silent monotonic-vs-epoch bugs that nominal Temporal types would catch.

- **URL:** https://w3ctag.github.io/design-principles/#times-and-dates
- **Chapter:** 8. Web IDL, Types, and Units
- **Agent-Fit:** mixed
- **Slide-Example:** clearly-harmful
- **Example-Strength:** 3/5
- **Verdict:** Banning mutable JS Date objects avoids classic reference-mutation and equality footguns, but representing timestamps as bare numeric DOMHighResTimeStamp values erases time-origin and unit metadata, inviting silent monotonic-vs-epoch bugs that nominal Temporal types would catch.

## Principle Summary

W3C TAG Design Principle §8.4 instructs specification authors to use `DOMHighResTimeStamp` (a floating-point millisecond value) when representing date-times on the web platform, and explicitly forbids using the JavaScript `Date` class in Web IDL interfaces.

The principle exists because JavaScript `Date` objects are inherently mutable (`date.setTime(...)`, `date.setHours(...)`) and cannot be frozen to prevent in-place modification of their internal timestamp value, making them unsafe for browser objects to expose as properties without defensive copying. Additionally, `DOMHighResTimeStamp` provides sub-millisecond precision and monotonic comparison independent of user clock adjustments or system timezone changes.

## Fit for Coding Agents

This principle is a mixed fit for AI coding agents because its negative guidance (avoiding `Date`) helps agents, while its positive guidance (using `DOMHighResTimeStamp` for date-times) introduces silent primitive-obsession bugs.

On the positive side, steering Web APIs away from JavaScript `Date` eliminates a notorious source of bugs in LLM-generated code. Because `Date` objects are mutable reference types, agents frequently introduce bugs by mutating a `Date` in place across function boundaries or comparing two `Date` instances with `===` (which checks reference identity rather than timestamp equality). Standardizing on millisecond numeric values allows straightforward value comparison (`<`, `>`, `===`), trivial JSON serialization, and consistency across timing APIs (`performance.now()`, `requestAnimationFrame`, `Event.timeStamp`, `Animation.currentTime`).

On the negative side, `DOMHighResTimeStamp` is a Web IDL `typedef double` that erases to a bare `number` in both JavaScript at runtime and TypeScript's type definitions (`type DOMHighResTimeStamp = number`). A bare number carries no machine-checkable metadata about its time origin or unit. Most `DOMHighResTimeStamp` values (`performance.now()`, `event.timeStamp`, `PerformanceEntry.startTime`) measure monotonic milliseconds since `timeOrigin` (page navigation), whereas `Date.now()` and `EpochTimeStamp` measure wall-clock milliseconds since the 1970 Unix epoch—and §8.4 itself blurs this boundary by telling spec authors to use `DOMHighResTimeStamp` for "representing date-times." Coding agents routinely hallucinate mixing the two (e.g., `Date.now() - event.timeStamp` or `new Date(entry.startTime)`, which yields a date in January 1970) or mixing millisecond APIs with second-based APIs (`AudioContext.currentTime`, `HTMLMediaElement.currentTime`, Unix timestamps). Because both are plain `number`s, neither TypeScript nor the JS runtime raises an error, resulting in silent logic bugs in the agent feedback loop, whereas modern nominal `Temporal` types (`Temporal.Instant`, `Temporal.ZonedDateTime`, `Temporal.Duration`) are immutable, self-describing, and throw loud `TypeError` or `RangeError` exceptions when misused.

## Value as a Slide Example

This principle is rated `neither` (`example_strength: 3/5`) as a headline slide example because it is internally split: nobody would argue for bringing back mutable `Date` objects, so it is not a rule to overturn (`clearly-harmful`), yet recommending an untyped `double` (`DOMHighResTimeStamp`) for date-times is dated and error-prone for agents (`clearly-useful` does not fit either).

However, if the presentation includes a supporting discussion on nominal types vs. primitive aliases, §8.4 offers a concrete, relatable code example. Showing an agent writing `const ageMs = Date.now() - event.timeStamp` or `new Date(performance.now())`—code that compiles cleanly in TypeScript because `DOMHighResTimeStamp` and `EpochTimeStamp` are both erased to `number`, and runs without throwing—vividly illustrates why agents benefit from evolving Web IDL guidance away from raw numeric typedefs toward immutable, nominal `Temporal` types (`Temporal.Instant`, `Temporal.Duration`) that fail loudly when origins or units are mismatched.
