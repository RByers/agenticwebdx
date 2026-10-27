---
section: "9.4"
id: "hardware-is-scary"
title: "Be proactive about safety"
chapter: "9. APIs that wrap access to device or browser capabilities"
url: "https://w3ctag.github.io/design-principles/#hardware-is-scary"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 1
verdict: "Primarily an end-user security and origin-isolation principle that applies regardless of whether code is written by a human or an AI agent, with only secondary implications for error handling and automated testing."
---

# §9.4 Be proactive about safety

GREP_SUMMARY: slide_example=neither | strength=1/5 | agent_fit=neutral | §9.4 hardware-is-scary — Be proactive about safety: Primarily an end-user security and origin-isolation principle that applies regardless of whether code is written by a human or an AI agent, with only secondary implications for error handling and automated testing.

- **URL:** https://w3ctag.github.io/design-principles/#hardware-is-scary
- **Chapter:** 9. APIs that wrap access to device or browser capabilities
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 1/5
- **Verdict:** Primarily an end-user security and origin-isolation principle that applies regardless of whether code is written by a human or an AI agent, with only secondary implications for error handling and automated testing.

## Principle Summary

W3C TAG Design Principle §9.4 ("Be proactive about safety", `#hardware-is-scary`) directs spec authors to design defensively when exposing native device or hardware capabilities to the web platform. Because simply detecting whether a user's machine has specific hardware leaks fingerprinting data, access outside the logical origin boundary must be gated by user permissions. Furthermore, because physical devices often hold mutable state that could be read and written by multiple origins—creating a cross-origin side-channel that bypasses the Same-Origin Policy—APIs should consider enforcing exclusive access per origin or restricting access to the currently active tab. Finally, hardware APIs should be designed so applications can gracefully handle physical disruptions such as a device being unplugged.

## Fit for Coding Agents

This principle is primarily neutral (orthogonal) to AI coding agents because its core purpose is protecting end-user privacy, hardware safety, and the web's Same-Origin Policy from untrusted web origins—guarantees that must be enforced by the browser regardless of whether the site's code was written by a human developer or an LLM. If anything, as coding agents make it trivially fast to generate and run web apps that interface with local hardware (such as WebUSB, WebSerial, or WebBluetooth utilities), browser-enforced origin boundaries, permission gates, and active-tab exclusivity remain vital platform-level guardrails.

Where §9.4 does intersect with developer ergonomics—designing APIs to gracefully handle physical disruption (like unplugging a device) and exclusive access revocation—it has two secondary implications for coding agents. First, LLM coding agents overwhelmingly generate "happy-path" hardware code on their first pass (`requestDevice` -> `open` -> `transferIn`) and routinely omit recovery logic for sudden device disconnection or background-tab lock revocation unless the API makes those state transitions explicit and loud (e.g., rejecting pending promises or closing Web Streams with descriptive `DOMException`s like `NetworkError` or `InvalidStateError` rather than hanging silently). Second, permission gates and active-tab restrictions block coding agents from verifying their code in headless browser loops (Playwright/Puppeteer) unless the spec pairs those safety restrictions with WebDriver BiDi virtual-device and permission-granting automation hooks.

## Value as a Slide Example

This principle is not useful as a slide example (`neither`, strength 1/5) for a TPAC session on adapting web standards to AI coding agents. Hardware permission gating and cross-origin side-channel prevention (in APIs like WebUSB, WebHID, WebSerial, and WebBluetooth) are non-negotiable end-user security and privacy boundaries, not developer-experience trade-offs that standards bodies would reconsider for agents. The only relevant agentic DX angle—that permission-gated and hardware-backed APIs must ship with virtual device automation hooks so agents can test disconnect and permission flows in headless browsers—is better illustrated by principles specifically focused on testability and automation.
