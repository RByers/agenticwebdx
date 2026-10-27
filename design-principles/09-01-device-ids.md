---
section: "9.1"
id: "device-ids"
title: "Don’t expose unnecessary information about capabilities"
chapter: "9. APIs that wrap access to device or browser capabilities"
url: "https://w3ctag.github.io/design-principles/#device-ids"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 1
verdict: "End-user privacy and anti-fingerprinting constraint that operates at the browser boundary regardless of whether site code is written by a human or an AI agent."
---

# §9.1 Don’t expose unnecessary information about capabilities

GREP_SUMMARY: slide_example=neither | strength=1/5 | agent_fit=neutral | §9.1 device-ids — Don’t expose unnecessary information about capabilities: End-user privacy and anti-fingerprinting constraint that operates at the browser boundary regardless of whether site code is written by a human or an AI agent.

- **URL:** https://w3ctag.github.io/design-principles/#device-ids
- **Chapter:** 9. APIs that wrap access to device or browser capabilities
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 1/5
- **Verdict:** End-user privacy and anti-fingerprinting constraint that operates at the browser boundary regardless of whether site code is written by a human or an AI agent.

## Principle Summary

This principle applies data minimization to Web APIs that expose hardware devices or browser capabilities. It directs spec authors to expose the minimum viable information—preferring less powerful APIs that do not reveal whether a capability exists at all, and ensuring that when a user denies access to a capability, the denial does not leak whether the underlying hardware or capability is present on the user's device.

When exposing device identifiers is unavoidable (for example, allowing a web app to remember a user's preferred microphone or camera across sessions via `MediaDeviceInfo.deviceId`), the principle mandates strict anti-fingerprinting rules: identifiers must be randomly generated and opaque rather than containing identifiable brand/make/model strings, scoped uniquely per origin, stable across requests and sessions within the same origin so sites do not duplicate devices, and cleared whenever the user clears browsing data.

## Fit for Coding Agents

At its core, this principle is neutral (orthogonal) to AI coding agents because it governs end-user privacy, unsanctioned tracking, and browser fingerprinting. The threat model—websites extracting entropy from hardware capabilities or device identifiers to track users across origins—is identical whether the JavaScript calling the API was written by a human developer or synthesized by an LLM. Browser vendors and spec authors cannot relax data minimization on the open web to improve developer or agent ergonomics.

There are two minor, contrasting secondary effects on how coding agents write and debug code against these APIs. First, on the positive side, forcing device identifiers (such as `MediaDeviceInfo.deviceId`) to be opaque, randomly generated per-origin tokens rather than raw brand/make/model strings prevents LLMs from hallucinating or copying brittle substring-matching heuristics from training data (e.g., matching `"FaceTime"` or `"Built-in"`), nudging agents to treat IDs strictly as opaque handles compared by equality and persisted in storage.

Second, on the friction side, the requirement that denying access must not reveal whether a capability exists intentionally suppresses diagnostic specificity in web-facing APIs (such as `navigator.mediaDevices.getUserMedia()`, `enumerateDevices()`, WebBluetooth, or WebUSB). When an AI coding agent runs an automated verification loop in a headless browser or CI container, collapsing missing virtual hardware and denied permissions can cause the agent to misdiagnose a missing test-harness device flag as a permission rejection (or vice versa) and spin in retry loops. However, the proper architectural response for agents is providing explicit, unambiguous diagnostics out-of-band via WebDriver BiDi and DevTools protocols rather than weakening privacy protections in web APIs.

## Value as a Slide Example

This principle is not useful as a slide example (`1/5`, `neither`) for a TPAC session on how web standards should adapt to coding agents. W3C TPAC attendees will immediately view §9.1 as a non-negotiable end-user privacy and anti-fingerprinting invariant that applies to the web platform boundary regardless of whether code is authored by humans or AI agents.

Its only tangential relevance is illustrating the boundary between in-band Web APIs—where privacy requires masking whether hardware is absent or permission was denied (`getUserMedia`, `enumerateDevices`)—and out-of-band automation/debugging protocols (WebDriver BiDi, CDP), where coding agents need clear diagnostic telemetry to avoid hallucinating fixes during headless browser testing. Beyond that footnote, it does not belong on a headline slide compared to principles that directly shape API ergonomics and developer experience.
