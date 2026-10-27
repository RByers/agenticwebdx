---
section: "9.2"
id: "device-enumeration"
title: "Use care when exposing APIs for selecting or enumerating devices"
chapter: "9. APIs that wrap access to device or browser capabilities"
url: "https://w3ctag.github.io/design-principles/#device-enumeration"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 2
verdict: "Primarily an end-user privacy and anti-fingerprinting principle that applies regardless of whether site code is written by a human or an AI agent, with minor secondary trade-offs between simpler single-call device pickers and harder headless browser automation."
---

# §9.2 Use care when exposing APIs for selecting or enumerating devices

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=neutral | §9.2 device-enumeration — Use care when exposing APIs for selecting or enumerating devices: Primarily an end-user privacy and anti-fingerprinting principle that applies regardless of whether site code is written by a human or an AI agent, with minor secondary trade-offs between simpler single-call device pickers and harder headless browser automation.

- **URL:** https://w3ctag.github.io/design-principles/#device-enumeration
- **Chapter:** 9. APIs that wrap access to device or browser capabilities
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Primarily an end-user privacy and anti-fingerprinting principle that applies regardless of whether site code is written by a human or an AI agent, with minor secondary trade-offs between simpler single-call device pickers and harder headless browser automation.

## Principle Summary

W3C TAG §9.2 advises spec authors to avoid exposing APIs that enumerate connected or available hardware devices, and to expose the minimum possible information when enumeration cannot be avoided. Because each device's existence, capabilities, and identifiers contribute entropy, enumerating multiple devices multiplies browser fingerprinting and user privacy risks. When the user's goal is simply to pick a device, the TAG recommends delegating selection to a User-Agent-provided device picker (such as `navigator.bluetooth.requestDevice()`, `navigator.usb.requestDevice()`, or `navigator.mediaDevices.selectAudioOutput()`) so the site only learns about the single device the user explicitly grants access to.

The principle also notes practical UI compromises and fallback mitigations: exposing a single boolean bit indicating whether any device is available (such as `RemotePlayback.watchAvailability()`) so sites can conditionally render a picker button; allowing constrained or filtered queries; and, if full enumeration is unavoidable, rigorously specifying the sort order of returned devices to prevent implementation-defined ordering from leaking additional fingerprinting bits or causing interop bugs.

## Fit for Coding Agents

This principle is fundamentally `neutral` with respect to AI coding agents because its threat model is the untrusted website origin versus the end user's privacy. Whether a web application is authored by a human developer or synthesized by an LLM, exposing a list of connected cameras, microphones, USB peripherals, or cast targets leaks sensitive hardware entropy to the origin and third-party scripts. The browser's responsibility to minimize passive fingerprinting surface does not relax when an agent writes the client code.

On a secondary developer-experience level, the API patterns favored by §9.2 cut both ways for coding agents. On the positive side, UA-mediated picker APIs (`requestDevice()`, `selectAudioOutput()`) replace a notorious legacy footgun in `navigator.mediaDevices.enumerateDevices()`, where privacy retrofits cause `enumerateDevices()` to return blank device labels and anonymized IDs until `getUserMedia()` permission is already granted. LLMs frequently hallucinate naive `enumerateDevices()` dropdown code that renders empty labels on first load, or else have to generate brittle multi-step permission-priming boilerplate; a single-call UA picker eliminates that state machine and UI ceremony. On the negative side, native browser-modal device pickers require transient user activation and sit outside the DOM, which makes autonomous verification harder in an agent's headless browser test loop (e.g., Playwright/CDP) unless specialized WebDriver BiDi commands or fake-UI browser flags are configured.

## Value as a Slide Example

This principle is `neither` a strong example of a rule that specifically helps coding agents nor one that is invalidated by them (`2/5`). At TPAC, it belongs in the baseline category of end-user security, privacy, and anti-fingerprinting invariants that remain just as necessary in an agentic web development world as in a human-authored one.

If mentioned briefly in passing, its most interesting angle is the tension between privacy-preserving native UA pickers (like `navigator.bluetooth.requestDevice()` or `selectAudioOutput()`) and agentic testability: while moving device selection into browser chrome saves the coding agent from writing complex in-page picker UI and tripping over `enumerateDevices()` empty-label privacy restrictions, it makes end-to-end verification in automated headless environments dependent on first-class WebDriver/CDP virtual-device and permission-automation hooks.
