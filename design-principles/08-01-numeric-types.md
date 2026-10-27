---
section: "8.1"
id: "numeric-types"
title: "Use numeric types appropriately"
chapter: "8. Web IDL, Types, and Units"
url: "https://w3ctag.github.io/design-principles/#numeric-types"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Helps coding agents by replacing silent WebIDL modulo-wrapping with loud TypeErrors via [EnforceRange]—crucial because TypeScript erases all WebIDL numeric types into a single `number` type—and by avoiding unnecessary BigInt/Number mixing."
---

# §8.1 Use numeric types appropriately

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §8.1 numeric-types — Use numeric types appropriately: Helps coding agents by replacing silent WebIDL modulo-wrapping with loud TypeErrors via [EnforceRange]—crucial because TypeScript erases all WebIDL numeric types into a single `number` type—and by avoiding unnecessary BigInt/Number mixing.

- **URL:** https://w3ctag.github.io/design-principles/#numeric-types
- **Chapter:** 8. Web IDL, Types, and Units
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Helps coding agents by replacing silent WebIDL modulo-wrapping with loud TypeErrors via [EnforceRange]—crucial because TypeScript erases all WebIDL numeric types into a single `number` type—and by avoiding unnecessary BigInt/Number mixing.

## Principle Summary

JavaScript has only one standard floating-point numeric type (`Number`, an IEEE 754 double-precision float) alongside `BigInt`. In contrast, WebIDL defines many fixed-width C-style numeric types (`octet`, `short`, `unsigned long`, `long long`, `double`, `unrestricted double`) that act as coercion rules at the JS-to-browser binding boundary. Because bare WebIDL integer types default to silent modulo wrapping (e.g., converting `300` to `44` for an `octet`, or `-1` to `4294967295` for an `unsigned long`), §8.1 advises spec authors to default to `double` (rejecting `NaN`/`±Infinity`), `unrestricted double`, or `[EnforceRange] (unsigned) long long` (throwing a `TypeError` when out of range), and to always pair narrower integer types like `octet` or `short` with `[EnforceRange]` or `[Clamp]`. It also states that `bigint` should only be used when values outside ±2^53 are expected, and APIs should never support both `BigInt` and `Number` simultaneously.

## Fit for Coding Agents

This principle aligns strongly with how AI coding agents generate, type-check, and debug web code because it directly compensates for a blind spot in the JavaScript/TypeScript static toolchain. In `lib.dom.d.ts`, every WebIDL numeric type (`octet`, `unsigned short`, `long`, `[EnforceRange] unsigned long long`, `double`) is collapsed into a single TypeScript type: `number`. As a result, an agent running `tsc` or an LSP receives zero compile-time feedback about whether an API parameter is a bare unsigned 8-bit integer, a signed 32-bit integer, or an IEEE 754 float. When a spec uses a bare WebIDL integer type without `[EnforceRange]` or `[Clamp]`, an off-by-one negative number (`-1`) or an out-of-range value (`300`) passes `tsc` cleanly and silently wraps via modulo arithmetic (`ToUint32(-1) === 4294967295`, `ToUint8(300) === 44`). Silent data corruption is one of the hardest failure modes for an agentic feedback loop to localize. By requiring `double` (which throws a `TypeError` on `NaN`/`±Infinity`) or `[EnforceRange]` (which throws a `TypeError` on out-of-range values), the binding boundary fails loudly and immediately with a stack trace pointing to the offending call site.

Additionally, when clamping is the natural domain semantics (e.g., color channels or byte buffers), specifying `[Clamp]` in WebIDL removes the need for agents to emit repetitive `Math.max(0, Math.min(255, Math.round(x)))` boilerplate. Finally, the guidance to reserve `bigint` strictly for values exceeding ±2^53 and never mix `BigInt` and `Number` via polymorphism aligns with both LLM training priors and JavaScript runtime ergonomics: JS throws a `TypeError` if `BigInt` is mixed with `Number` in arithmetic (`1n + 1`), passed to `Math.*`, or serialized with `JSON.stringify()`, so keeping APIs consistently `number`-typed unless >53-bit precision is strictly required prevents frequent agent type-mixing errors.

## Value as a Slide Example

This principle is a solid supporting example (3/5) of a `clearly-useful` rule, particularly for illustrating why loud runtime boundary checks in WebIDL still matter even when coding agents rely heavily on TypeScript. Spec authors may see `octet` or `unsigned long` in WebIDL, but an agent's TypeScript compiler only sees `number` in `lib.dom.d.ts`. Contrasting bare `unsigned long` (where passing `-1` compiles cleanly in TypeScript and silently wraps to `4294967295` at runtime) against `[EnforceRange] unsigned long long` (which immediately throws a `TypeError` the agent can catch in its test loop) is a crisp, concrete illustration of designing for agentic feedback loops. However, because it is a low-level WebIDL binding detail rather than a high-level API architecture pattern, it works best as a supporting bullet under a broader "Fail Loudly / Bridge Static Type Erasure" slide rather than as a standalone headline slide.
