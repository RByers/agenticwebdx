---
section: "9.5"
id: "wrapper-apis"
title: "Adapt native APIs using web platform principles"
chapter: "9. APIs that wrap access to device or browser capabilities"
url: "https://w3ctag.github.io/design-principles/#wrapper-apis"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Unifying OS-specific native APIs behind consistent, feature-detectable web idioms helps coding agents—which typically verify code in a single headless Linux environment rather than across physical OS devices—though much of the section covers orthogonal open-web and privacy policy."
---

# §9.5 Adapt native APIs using web platform principles

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §9.5 wrapper-apis — Adapt native APIs using web platform principles: Unifying OS-specific native APIs behind consistent, feature-detectable web idioms helps coding agents—which typically verify code in a single headless Linux environment rather than across physical OS devices—though much of the section covers orthogonal open-web and privacy policy.

- **URL:** https://w3ctag.github.io/design-principles/#wrapper-apis
- **Chapter:** 9. APIs that wrap access to device or browser capabilities
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Unifying OS-specific native APIs behind consistent, feature-detectable web idioms helps coding agents—which typically verify code in a single headless Linux environment rather than across physical OS devices—though much of the section covers orthogonal open-web and privacy policy.

## Principle Summary

This principle advises spec authors that when exposing native operating system or hardware capabilities to the web, they should not simply copy a single platform's native API surface verbatim. Instead, wrapper APIs should follow established web platform conventions, account for how different operating systems provide the underlying capability, and strive for identical behavior across all implementations. Where platform-specific options cannot be avoided, the specification must make those capabilities detectable (referencing §2.6) and document how authors can write portable code across all platforms.

The principle also bundles three broader web platform requirements for wrapper APIs: they must not depend on closed or proprietary protocols to communicate with external hardware or services; they must degrade gracefully when any required remote backend service is unreachable; and they must guard against expanding the browser's fingerprinting surface. Together, these rules protect the portability, openness, offline resilience, and privacy of the web when bridging into native OS capabilities.

## Fit for Coding Agents

The core developer-experience guidance in this principle—abstracting divergent OS APIs into uniform, web-idiomatic interfaces and making platform-specific options detectable—is a strong positive for AI coding agents. Unlike human teams that may test on physical macOS, Windows, iOS, and Android devices, coding agents almost always execute their edit-run-verify loop inside a single sandboxed environment (typically headless Chromium on Linux). When a web wrapper API leaks OS-specific quirks or silently ignores options on certain platforms—such as Notification options (actions, image, renotify) or navigator.share() payloads that behave differently across desktop and mobile OSes—an agent has no runtime signal in its Linux test environment that the code will fail on a user's phone or Mac. Uniform cross-platform behavior and programmatic feature detection allow agents to write defensive, portable code without needing multi-OS hardware-in-the-loop verification.

Adapting native capabilities to standard web idioms (such as Promises, EventTarget, AbortSignal, and dictionary option bags) also aligns new device APIs with the statistical priors agents have learned across the rest of the web platform, reducing hallucinations of platform-native C++/Objective-C/Kotlin conventions. Additionally, the requirement that remote-service-backed APIs function gracefully when the remote server is unreachable helps prevent unexplained hangs or crashes when agents run automated browser tests in network-restricted CI sandboxes.

The remaining parts of the principle—avoiding closed or proprietary hardware protocols and minimizing user fingerprinting surfaces—are largely neutral to whether code is written by a human or an LLM. They are essential architectural safeguards for end-user privacy and the open web ecosystem, rather than factors that alter how coding agents read, generate, or debug application code.

## Value as a Slide Example

This principle is a poor headline slide candidate (neither, strength 2/5) because it functions primarily as a broad umbrella reminder ("use web platform principles") combined with general policy goals around open protocols and anti-fingerprinting. On a slide at W3C TPAC, telling standards authors to "adapt native APIs using web platform principles" is too meta and self-referential to spark a concrete architectural discussion about agentic DX.

The one genuinely interesting agent-specific angle here—that leaky OS wrappers with undetectable per-platform differences break the agent verification loop because agents only test in headless Linux containers—is much better illustrated through more specific principles such as §2.6 ("New features should be detectable") or concrete API case studies like Web Notification options and Web Bluetooth/USB capability probing.
