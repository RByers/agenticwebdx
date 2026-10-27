---
section: "10.9"
id: "client-hints"
title: "Do not expose new information through Client Hints"
chapter: "10. Other API Design Considerations"
url: "https://w3ctag.github.io/design-principles/#client-hints"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Directionally helpful for coding agents by guaranteeing that device and user-agent state is always accessible via typed, locally testable JS/CSS APIs rather than trapped behind fragile, multi-round-trip HTTP header negotiation, though too narrow to be a TPAC slide example."
---

# §10.9 Do not expose new information through Client Hints

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §10.9 client-hints — Do not expose new information through Client Hints: Directionally helpful for coding agents by guaranteeing that device and user-agent state is always accessible via typed, locally testable JS/CSS APIs rather than trapped behind fragile, multi-round-trip HTTP header negotiation, though too narrow to be a TPAC slide example.

- **URL:** https://w3ctag.github.io/design-principles/#client-hints
- **Chapter:** 10. Other API Design Considerations
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Directionally helpful for coding agents by guaranteeing that device and user-agent state is always accessible via typed, locally testable JS/CSS APIs rather than trapped behind fragile, multi-round-trip HTTP header negotiation, though too narrow to be a TPAC slide example.

## Principle Summary

This principle, echoing RFC 8942 §4.1, states that HTTP Client Hints (`Sec-CH-*` and related request headers) must strictly serve as a network-level optimization for proactive content negotiation and must never be the sole mechanism by which a capability or piece of client state is exposed to a web application. Any information delivered via a Client Hint must first (or simultaneously) be exposed to the page via standard client-side surfaces—HTML, CSS (such as media queries), or JavaScript APIs.

For human developers and browser architects, this rule ensures architectural parity across deployment models and runtime lifecycles. Static sites, single-page applications, and client-side components often cannot inspect HTTP request headers or configure server-side `Accept-CH` opt-in handshakes. Furthermore, client state can change dynamically after the initial navigation (for example, a user toggling dark mode or dragging a window to a different display), which requires reactive client-side CSS or JavaScript APIs rather than one-shot request headers. It also prevents specification authors from using HTTP headers as a backdoor to expose new fingerprinting surfaces without going through standard DOM API privacy and security review.

## Fit for Coding Agents

This principle aligns well with the ergonomics and verification loops of AI coding agents (`agent_fit: good`), even though it was designed as a general architectural constraint. Client Hints are notoriously difficult for coding agents to implement and verify reliably because they span multiple infrastructure layers and require stateful protocol handshakes: the server must first send an `Accept-CH` response header over a secure context (HTTPS), optionally coordinate `Critical-CH` for first-navigation delivery or `Permissions-Policy` for cross-origin subresources, and set appropriate `Vary` headers for CDN caching. When any part of that handshake is misconfigured—or when an agent is working only inside frontend application code—Client Hints fail completely silently: the browser simply omits the `Sec-CH-*` header on subsequent requests with no console warning or exception.

By guaranteeing that every Client Hint has a corresponding client-side API (for example, `Sec-CH-Prefers-Color-Scheme` pairing with CSS `@media (prefers-color-scheme)` and `window.matchMedia`, `Sec-CH-UA-*` pairing with `navigator.userAgentData`, and `Device-Memory` pairing with `navigator.deviceMemory`), this principle ensures agents can always access the same information inside a single code boundary. Client-side JS and CSS surfaces benefit from static type definitions (`lib.dom.d.ts`), work out of the box in local dev servers and static sandbox previews without HTTPS or custom server middleware, and can be directly inspected by an agent in a headless browser test (`page.evaluate()`) to verify behavior or cross-check server-rendered output.

At the same time, the existence of dual surfaces (both a client-side API and an HTTP Client Hint) still leaves a minor footgun when agents generate server-side rendering (SSR) or edge middleware code: agents frequently hallucinate that high-entropy `Sec-CH-*` headers are sent by default on the initial HTTP request (like the legacy `User-Agent` header), forgetting that the server must first emit `Accept-CH` and handle the unhinted first load. Having the client-side API available provides a reliable fallback and reconciliation path when SSR hints are missing on initial page load.

## Value as a Slide Example

Despite being directionally beneficial for coding agents, this principle is a poor candidate for a headline slide at W3C TPAC (`slide_example: neither`, `example_strength: 2/5`). It is a narrow, RFC-derived guardrail aimed at specification authors proposing new HTTP Client Hints rather than a general-purpose API design pattern that illustrates how AI agents change developer experience.

Furthermore, the reasons this principle helps coding agents—avoiding mandatory server header configuration, supporting static/client-only deployments, and enabling runtime reactivity—are virtually identical to the reasons it helps human web developers. If Client Hints are mentioned at all in a discussion of agentic DX, the more interesting observation is not §10.9 itself, but rather how multi-step, silent-failing HTTP header opt-in handshakes (`Accept-CH` + `Critical-CH` + `Permissions-Policy` + `Vary`) are much harder for agents to debug than explicit, typed, in-band APIs.
