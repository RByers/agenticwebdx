---
section: "6.15"
id: "uint8array"
title: "Output an array of bytes with Uint8Array"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#uint8array"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 2
verdict: "Returning Uint8Array or a specific TypedArray instead of a raw ArrayBuffer helps coding agents by eliminating silent property-access footguns (like buffer[0] and buffer.length evaluating to undefined), encoding binary layout semantics directly in TypeScript/WebIDL return types, and removing repetitive wrapping ceremony."
---

# §6.15 Output an array of bytes with Uint8Array

GREP_SUMMARY: slide_example=clearly-useful | strength=2/5 | agent_fit=good | §6.15 uint8array — Output an array of bytes with Uint8Array: Returning Uint8Array or a specific TypedArray instead of a raw ArrayBuffer helps coding agents by eliminating silent property-access footguns (like buffer[0] and buffer.length evaluating to undefined), encoding binary layout semantics directly in TypeScript/WebIDL return types, and removing repetitive wrapping ceremony.

- **URL:** https://w3ctag.github.io/design-principles/#uint8array
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 2/5
- **Verdict:** Returning Uint8Array or a specific TypedArray instead of a raw ArrayBuffer helps coding agents by eliminating silent property-access footguns (like buffer[0] and buffer.length evaluating to undefined), encoding binary layout semantics directly in TypeScript/WebIDL return types, and removing repetitive wrapping ceremony.

## Principle Summary

W3C TAG §6.15 advises that web APIs returning a byte sequence should return a `Uint8Array` rather than a raw `ArrayBuffer`. Because an `ArrayBuffer` cannot be read or indexed directly, returning one forces developers to immediately instantiate a view such as `new Uint8Array(buffer)` before inspecting or manipulating the bytes.

The principle also specifies that if the bytes in the buffer have a natural domain interpretation as another `TypedArray` type—for instance, 32-bit floating-point numbers—the API should return that specific typed array (such as `Float32Array`) directly instead of a generic byte view or raw buffer.

## Fit for Coding Agents

This principle is a good fit for AI coding agents for three reasons that go beyond saving a human developer a few keystrokes. First, in untyped JavaScript, accidentally treating a raw `ArrayBuffer` as a byte array produces silent bugs rather than loud exceptions: `buffer.length` is `undefined` (the property is `buffer.byteLength`) and indexed access like `buffer[0]` also evaluates to `undefined` without throwing. If an agent writes a standard loop like `for (let i = 0; i < data.length; i++)` on an API return value it expects to be a byte array, a raw `ArrayBuffer` causes `0 < undefined` to evaluate to `false`, silently executing zero iterations and producing empty output with no stack trace in the agent's feedback loop. Returning `Uint8Array` ensures `.length`, `data[i]`, `.slice()`, and standard array-like methods work directly.

Second, the principle's guidance to return specific typed arrays like `Float32Array` when bytes have a natural interpretation encodes critical binary layout semantics directly in the WebIDL and TypeScript return type (such as Web Audio's `AudioBuffer.prototype.getChannelData()` returning `Float32Array`). When an API instead returns an opaque `ArrayBuffer`, an agent must rely on memorized prose documentation to know whether to wrap the buffer in `Uint8Array`, `Int16Array`, or `Float32Array`.

Third, standardizing binary outputs on `Uint8Array` matches the universal currency expected by modern web and WinterTC APIs (`TextDecoder`, `ReadableStream` byte chunks, `Blob`, and Fetch's newer `Response.prototype.bytes()`), while still exposing `.buffer` when the underlying store is needed. Although legacy APIs (`Response.prototype.arrayBuffer()`, `SubtleCrypto`, `FileReader`) are common enough in training data that agents readily write `new Uint8Array(await res.arrayBuffer())`, returning `Uint8Array` directly reduces adapter glue and avoids subtle `byteOffset`/`byteLength` slicing bugs.

## Value as a Slide Example

While §6.15 clearly aligns with agent ergonomics (`clearly-useful`), it rates a 2/5 in slide strength because it is a narrow, tactical JavaScript return-type convention rather than a high-level architectural principle. Its value for agents is mostly the same as for humans, with a modest extra benefit around avoiding silent `buffer.length`/`buffer[0]` `undefined` bugs in dynamic JS and preserving element types (`Float32Array` vs opaque `ArrayBuffer`) in TypeScript signatures.

If used in the TPAC deck, it works best as a compact row in a summary table rather than a featured slide, contrasting `await response.bytes()` (`Uint8Array`) against `new Uint8Array(await response.arrayBuffer())`, or `AudioBuffer.getChannelData()` (`Float32Array`) against an untyped `ArrayBuffer`.
