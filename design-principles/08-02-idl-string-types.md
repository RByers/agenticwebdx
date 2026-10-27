---
section: "8.2"
id: "idl-string-types"
title: "Represent strings appropriately"
chapter: "8. Web IDL, Types, and Units"
url: "https://w3ctag.github.io/design-principles/#idl-string-types"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 1
verdict: "Mostly internal Web IDL spec plumbing since DOMString, USVString, and ByteString all erase to string in JavaScript and TypeScript, though preferring Uint8Array over ByteString avoids hidden Latin-1 runtime errors."
---

# §8.2 Represent strings appropriately

GREP_SUMMARY: slide_example=neither | strength=1/5 | agent_fit=neutral | §8.2 idl-string-types — Represent strings appropriately: Mostly internal Web IDL spec plumbing since DOMString, USVString, and ByteString all erase to string in JavaScript and TypeScript, though preferring Uint8Array over ByteString avoids hidden Latin-1 runtime errors.

- **URL:** https://w3ctag.github.io/design-principles/#idl-string-types
- **Chapter:** 8. Web IDL, Types, and Units
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 1/5
- **Verdict:** Mostly internal Web IDL spec plumbing since DOMString, USVString, and ByteString all erase to string in JavaScript and TypeScript, though preferring Uint8Array over ByteString avoids hidden Latin-1 runtime errors.

## Principle Summary

This principle guides specification authors on choosing among Web IDL's three string types: `DOMString`, `USVString`, and `ByteString`. It instructs spec editors to default to `DOMString` (a sequence of 16-bit UTF-16 code units matching JavaScript's internal string representation) because most string operations do not need to inspect or normalize individual code units.

It reserves `USVString` (Unicode scalar values, where unpaired UTF-16 surrogates are replaced with `U+FFFD`) for APIs that process scalar values—such as URL parsing, percent-encoding, and reflected URL attributes like `href`—or that pass strings directly to native OS APIs that reject lone surrogates. Finally, it restricts `ByteString` strictly to legacy or protocol-level data (such as HTTP headers) where bytes and strings are conflated, directing spec authors to use `Uint8Array` whenever representing an actual sequence of bytes.

## Fit for Coding Agents

For AI coding agents reading and generating web application code, this principle is largely neutral because it governs internal Web IDL binding mechanics rather than developer-facing API ergonomics. In both JavaScript at runtime and TypeScript (`lib.dom.d.ts`) at compile time, `DOMString`, `USVString`, and `ByteString` all collapse to the exact same primitive type: `string`. An agent inspecting TypeScript definitions or generating API calls cannot see whether an attribute or parameter is specified as `DOMString` or `USVString`, and the behavioral difference between the two only manifests when a string contains unpaired UTF-16 surrogates. Because LLM tokenizers operate over valid UTF-8 text, agents never emit lone surrogates in string literals unless deliberately synthesizing `\uD800`-style escape sequences for edge-case conformance tests.

The one clause with a tangible (if secondary) benefit for coding agents is the rule against using `ByteString` as a general-purpose binary type in favor of `Uint8Array`. Because `ByteString` is typed as a plain `string` in TypeScript (`lib.dom.d.ts`), its `<= 0xFF` code-unit constraint is invisible to static type checking. Where legacy or protocol APIs rely on `ByteString` or Latin-1 string semantics (such as HTTP header values in `fetch()`/`Headers` or `btoa()`), coding agents frequently pass arbitrary UTF-8 strings containing non-ASCII characters or emoji, triggering runtime `TypeError` or `InvalidCharacterError` exceptions that the type checker could not catch. By steering new binary APIs to `Uint8Array` and keeping normal string APIs on `DOMString` or `USVString`, the principle keeps the static type signature aligned with actual runtime invariants.

Overall, however, the choice between `DOMString` and `USVString` is an engine-level interoperability concern between specifications (e.g., aligning with the WHATWG Infra, URL, and HTML standards) that operates beneath the abstraction layer where coding agents work.

## Value as a Slide Example

This principle is not suitable (`1/5`, `neither`) as a slide example for the TPAC breakout session. The distinction between `DOMString` and `USVString` is esoteric Web IDL specification plumbing that is completely erased in JavaScript and TypeScript type definitions, so it neither illustrates how coding agents benefit from good web API design nor highlights a place where human-centric design assumptions backfire for agents. While the `ByteString` vs. `Uint8Array` distinction touches on type-system expressiveness (why hiding byte constraints inside `string` causes runtime surprises in APIs like `Headers` or `btoa()`), other principles in Chapter 8 address explicit typing and structured representations far more directly.
