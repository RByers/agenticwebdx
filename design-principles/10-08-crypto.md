---
section: "10.8"
id: "crypto"
title: "Use the best crypto, and expect it to evolve"
chapter: "10. Other API Design Considerations"
url: "https://w3ctag.github.io/design-principles/#crypto"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 2
verdict: "Primarily a security and protocol-architecture mandate orthogonal to who writes the code, though fast-evolving cryptography clashes with frozen LLM training priors whenever specs push algorithm selection onto callers instead of defaulting it in the platform."
---

# §10.8 Use the best crypto, and expect it to evolve

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=neutral | §10.8 crypto — Use the best crypto, and expect it to evolve: Primarily a security and protocol-architecture mandate orthogonal to who writes the code, though fast-evolving cryptography clashes with frozen LLM training priors whenever specs push algorithm selection onto callers instead of defaulting it in the platform.

- **URL:** https://w3ctag.github.io/design-principles/#crypto
- **Chapter:** 10. Other API Design Considerations
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Primarily a security and protocol-architecture mandate orthogonal to who writes the code, though fast-evolving cryptography clashes with frozen LLM training priors whenever specs push algorithm selection onto callers instead of defaulting it in the platform.

## Principle Summary

W3C TAG Principle §10.8 (`crypto`) instructs specification authors to rely solely on cryptographic algorithms that have been impartially reviewed by security experts and proven in practice, and to design web platform features with cryptographic agility from the start. Because cryptographic primitives and protocols evolve rapidly—and older algorithms routinely become obsolete or broken—specifications must neither invent bespoke cryptography nor hardcode fixed primitives without a migration path.

For browsers and human developers, this principle exists to protect end users from catastrophic security failures embedded in standards (such as early specs baking in MD5 or SHA-1 without algorithm negotiation or upgrade mechanisms) and to ensure the web platform can transition smoothly to stronger primitives (for example, from SHA-1 to SHA-256/384/512, or toward post-quantum cryptography) without breaking the web.

## Fit for Coding Agents

At its core, this principle is neutral (orthogonal) to AI coding agents because it governs the cryptographic soundness and protocol longevity of the web platform itself. Whether a web application is written by a human developer or an LLM coding agent, underlying browser protocols and platform primitives must use peer-reviewed, up-to-date cryptography to protect end users.

However, the second half of the principle—"expect it to evolve"—has an important secondary implication for API design in an era of agent-authored code: cryptography evolves quickly, but LLM weights and training corpora have strong historical inertia. When a specification implements cryptographic agility by forcing application code to explicitly name algorithms, curves, or parameters, coding agents actively pull against cryptographic evolution. In APIs like Web Crypto (`crypto.subtle`), agents frequently reproduce dominant historical patterns from training data—such as using `SHA-1` for digests, choosing `AES-CBC` without authentication over `AES-GCM`, or copying outdated `PBKDF2` iteration counts (`1000` or `10000`)—because legacy tutorials outnumber recent ones in pretraining corpora. Similarly, in WebAuthn (`navigator.credentials.create`), early versions required callers to specify `pubKeyCredParams` with explicit COSE algorithm IDs, causing agents to overwhelmingly hardcode `[{ type: "public-key", alg: -7 }]` (ES256) and omit newer algorithms like EdDSA (`-8`).

Furthermore, because outdated cryptographic choices still execute without throwing runtime errors, an agent's test-and-fix feedback loop receives a green signal even when the generated cryptography is obsolete. Consequently, while the principle's security goal is universal, applying "expect it to evolve" in an agentic world strongly favors platform-managed negotiation and evolving safe defaults (such as WebAuthn later making `pubKeyCredParams` optional with browser-managed defaults) over forcing callers to hardcode algorithm identifiers in JavaScript.

## Value as a Slide Example

This principle is neither a strong `clearly-useful` nor `clearly-harmful` headline example for the TPAC breakout deck (`2/5`), because on its face "Use the best crypto" reads as basic security hygiene rather than a developer-experience (DX) tradeoff. Featuring it as a primary slide example would require too much explanation that the issue is not the security mandate itself, but where cryptographic agility is handled (in the browser vs. in application code).

However, the contrast between `crypto.subtle` (or early WebAuthn `pubKeyCredParams: [{ type: "public-key", alg: -7 }]`) and WebAuthn's later optional default algorithm list is a useful supporting example under a broader point about high-level defaults vs. low-level configuration: whenever a standard expects best practices to evolve over time, putting the current best choice into a browser-managed default upgrades agent-written code automatically, whereas requiring callers to pass explicit algorithm identifiers locks agent-generated code into the cryptographic past of its training data.
