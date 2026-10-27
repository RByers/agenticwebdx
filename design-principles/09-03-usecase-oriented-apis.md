---
section: "9.3"
id: "usecase-oriented-apis"
title: "Design based on user needs, not the underlying capability"
chapter: "9. APIs that wrap access to device or browser capabilities"
url: "https://w3ctag.github.io/design-principles/#usecase-oriented-apis"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Use-case-oriented APIs align directly with natural-language prompt intent and shield agents from synthesizing fragile, hardware-specific lifecycle code that they cannot verify in headless test environments."
---

# §9.3 Design based on user needs, not the underlying capability

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §9.3 usecase-oriented-apis — Design based on user needs, not the underlying capability: Use-case-oriented APIs align directly with natural-language prompt intent and shield agents from synthesizing fragile, hardware-specific lifecycle code that they cannot verify in headless test environments.

- **URL:** https://w3ctag.github.io/design-principles/#usecase-oriented-apis
- **Chapter:** 9. APIs that wrap access to device or browser capabilities
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Use-case-oriented APIs align directly with natural-language prompt intent and shield agents from synthesizing fragile, hardware-specific lifecycle code that they cannot verify in headless test environments.

## Principle Summary

When exposing native OS or hardware capabilities to the web, §9.3 advises against directly translating an existing native API, its exact lifecycle, or its underlying data structures into Web IDL. Instead, specification authors should identify the user needs that the underlying capability serves and design a web API around how it is intended to be used, even if the browser's implementation wraps a specific native API under the hood.

For human developers, browsers, and end users, this principle protects cross-platform portability and forward compatibility with new hardware. A 1:1 port of an OS-specific API (such as Win32, Android, or CoreBluetooth primitives) leaks hardware assumptions that may not hold on other operating systems or future form factors, and forces web developers to manage low-level state machines and platform-specific data representations rather than expressing high-level application goals.

## Fit for Coding Agents

This principle is a good fit (`good`) for AI coding agents for two primary reasons: prompt-to-API semantic alignment and the inability of agents to test physical hardware lifecycles in closed-loop sandboxes. Coding agents operate on user prompts that are inherently phrased in terms of user needs and use cases—for example, "let the user share this link," "copy the token to the clipboard," or "sample a color from the screen." When a web API is designed around the use case (`navigator.share()`, `navigator.clipboard.writeText()`, `new EyeDropper().open()`), the mapping from the prompt's intent to the API call is direct, compact, and self-describing in context. By contrast, when an API mirrors the raw lifecycle and data structures of an underlying native subsystem, the agent must synthesize multi-step state machines, handle allocation/cleanup, and buffer marshaling just to accomplish a simple user task—dramatically increasing token overhead and the surface area for subtle state-management bugs.

Second, device and native capability APIs suffer from a unique feedback-loop gap for coding agents: agents almost always verify their code in headless browsers or sandboxed CI environments without physical hardware attached. An agent cannot plug in a Bluetooth peripheral, tap an NFC tag, or test across Windows, macOS, iOS, and Android hardware drivers during its iteration loop. If a web API exposes the exact lifecycle, timing quirks, and data structures of an underlying native API, the agent is forced to write complex hardware-interaction code open-loop. Any hallucinated lifecycle transition, missing teardown call on an error branch, or struct layout mismatch will silently pass mocks and fail only on real user devices. Having the browser absorb the native lifecycle and expose a higher-level, intent-driven interface keeps the agent's code declarative and reliable.

There is one minor nuance: when an agent is specifically tasked with porting existing native code (e.g., C/POSIX or a well-known native SDK heavily represented in pretraining data) to the web, a bespoke web abstraction requires translating idioms rather than copying native calls 1:1. However, for the vast majority of web development tasks, hiding native lifecycle ceremony in favor of use-case-oriented APIs strongly benefits agent reliability.

## Value as a Slide Example

This principle is a solid supporting candidate (`clearly-useful`, 3/5) for a TPAC slide, particularly when discussing how agents interact with device capabilities and why open-loop hardware APIs are uniquely treacherous for LLMs.

A concrete contrast for a slide is comparing high-level use-case APIs like `navigator.share()`, `EyeDropper`, or `navigator.clipboard.writeText()` against low-level capability wrappers like WebBluetooth GATT characteristic byte manipulation or WebUSB transfer lifecycles. When prompted to "let the user share this article," an agent calling `navigator.share({ title, text, url })` writes three lines of declarative code that works across mobile and desktop share sheets. By contrast, when an API exposes raw device lifecycles and native data structures, the agent must generate fragile connection state machines and `DataView` byte-packing without any physical device in its headless test loop to verify that the code works. While §9.3 is also heavily motivated by hardware evolution and OS portability (making it a 3/5 rather than a 5/5 headline example), its lesson for the agentic era is clear: APIs shaped like user intent match how humans prompt agents and keep untestable hardware lifecycles inside the browser engine.
