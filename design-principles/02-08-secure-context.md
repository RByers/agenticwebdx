---
section: "2.8"
id: "secure-context"
title: "Consider limiting new features to secure contexts"
chapter: "2. API Design Across Languages"
url: "https://w3ctag.github.io/design-principles/#secure-context"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 2
verdict: "Primarily an end-user transport security policy and spec-authoring rule orthogonal to coding agents, though gating non-sensitive utilities behind [SecureContext] creates opaque missing-symbol errors in containerized non-localhost agent test environments."
---

# §2.8 Consider limiting new features to secure contexts

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=neutral | §2.8 secure-context — Consider limiting new features to secure contexts: Primarily an end-user transport security policy and spec-authoring rule orthogonal to coding agents, though gating non-sensitive utilities behind [SecureContext] creates opaque missing-symbol errors in containerized non-localhost agent test environments.

- **URL:** https://w3ctag.github.io/design-principles/#secure-context
- **Chapter:** 2. API Design Across Languages
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Primarily an end-user transport security policy and spec-authoring rule orthogonal to coding agents, though gating non-sensitive utilities behind [SecureContext] creates opaque missing-symbol errors in containerized non-localhost agent test environments.

## Principle Summary

This principle states that any web platform feature that poses a risk to the user without transport-level authentication, integrity, or confidentiality must be restricted to secure contexts (such as HTTPS or `localhost`). For features without a direct security or privacy impact, the principle explicitly notes a lack of TAG consensus: some favor restricting all new features to secure contexts to incentivize broader HTTPS adoption, while others favor restricting only security- or privacy-sensitive features to keep the barrier to entry low for web developers.

The principle also covers two practical mechanics: first, when a feature (such as dispatching an event) cannot use the WebIDL `[SecureContext]` extended attribute directly, the restriction should be specified in normative prose while considering future WebIDL extensions; second, spec authors should be cautious about restricting a feature to secure contexts if code (such as shared libraries) has no way to gracefully handle the feature's absence across both secure and non-secure environments.

## Fit for Coding Agents

At its core, this principle is largely orthogonal to AI coding agents (`neutral`). The mandate to require secure contexts for sensitive capabilities protects end users from network attackers and man-in-the-middle threats regardless of whether a human or an LLM authored the application. Similarly, the guidance on when to use WebIDL `[SecureContext]` versus normative specification prose is an internal spec-editing concern that does not change how agents write or consume web code.

However, the unresolved policy debate within the principle—whether to restrict non-sensitive utility features to secure contexts solely to encourage HTTPS adoption—has a concrete side effect on agentic development workflows. LLM coding agents strongly default to modern platform utilities prevalent in their training data, such as `crypto.randomUUID()` or `navigator.clipboard`, without emitting defensive `window.isSecureContext` checks. While local development on `http://localhost` counts as a secure context, agents frequently execute and verify code inside containerized CI pipelines, Docker Compose networks (e.g., Playwright testing against `http://app:3000`), LAN previews, or remote sandbox VMs accessed via non-localhost HTTP hostnames.

When a feature is gated via WebIDL `[SecureContext]`, browsers completely omit the interface or method from the global object or prototype in non-secure contexts rather than exposing the method and throwing a descriptive `SecurityError` explaining that HTTPS is required. Consequently, an agent testing against `http://app:3000` encounters a generic `TypeError: crypto.randomUUID is not a function` or `Cannot read properties of undefined`. In an automated feedback loop, this silent omission of the symbol mimics an outdated browser or missing polyfill rather than a transport-security configuration issue, frequently causing agents to misdiagnose the failure and hallucinate unnecessary polyfills or test mocks. Thus, in the debate §2.8 leaves open, agent ergonomics strongly favor restricting only features with genuine security or privacy impact, and favor loud, self-diagnosing runtime errors over hiding APIs on the prototype.

## Value as a Slide Example

This principle is neither a strong `clearly-useful` nor `clearly-harmful` headline example for the TPAC breakout slides (`example_strength: 2/5`). Its primary purpose is end-user transport security, and on the question of non-sensitive APIs, the principle itself deliberately takes no firm stance, merely documenting both sides of an older W3C policy debate.

If mentioned at all, its only value is as a brief supporting anecdote about diagnostic error quality in agent feedback loops: specifically, how the mechanism of `[SecureContext]` (hiding APIs so they fail with `undefined is not a function` instead of throwing an actionable error naming the secure-context requirement) and its application to benign utilities like `crypto.randomUUID()` can mislead agents running headless browser tests over internal Docker HTTP hostnames (`http://app:3000`). However, that critique is more tightly coupled to WebIDL's `[SecureContext]` mechanics and error-reporting design than to §2.8 itself.
