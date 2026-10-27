---
section: "10.3"
id: "expose-everywhere"
title: "Only purely computational features should be exposed everywhere"
chapter: "10. Other API Design Considerations"
url: "https://w3ctag.github.io/design-principles/#expose-everywhere"
agent_fit: "mixed"
slide_example: "neither"
example_strength: 2
verdict: "Mostly governed by hard runtime constraints in non-event-loop realms like Worklets, though universal console/TextEncoder exposure helps agents while partial interface splits (AbortSignal.timeout) and conservative withholding of computational types (Blob) invite cross-realm hallucinations."
---

# §10.3 Only purely computational features should be exposed everywhere

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=mixed | §10.3 expose-everywhere — Only purely computational features should be exposed everywhere: Mostly governed by hard runtime constraints in non-event-loop realms like Worklets, though universal console/TextEncoder exposure helps agents while partial interface splits (AbortSignal.timeout) and conservative withholding of computational types (Blob) invite cross-realm hallucinations.

- **URL:** https://w3ctag.github.io/design-principles/#expose-everywhere
- **Chapter:** 10. Other API Design Considerations
- **Agent-Fit:** mixed
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Mostly governed by hard runtime constraints in non-event-loop realms like Worklets, though universal console/TextEncoder exposure helps agents while partial interface splits (AbortSignal.timeout) and conservative withholding of computational types (Blob) invite cross-realm hallucinations.

## Principle Summary

This principle guides specification authors on when to mark Web IDL interfaces or members with [Exposed=*], which makes a feature available across every JavaScript global environment (Window, Dedicated/Shared/Service Worker, AudioWorklet, PaintWorklet, ShadowRealm, etc.). It states that only purely computational features—those that perform no I/O, do not mutate user agent or device state, and do not depend on an event loop—should be exposed everywhere. For example, TextEncoder is purely computational and exposed everywhere, whereas localStorage mutates browser state and AbortSignal.timeout() requires an event loop, so neither is exposed in all scopes.

The principle also carves out two opposing nuances: a pragmatic relaxation for console (which technically performs side-effecting logging, but is exposed everywhere because universal debugging utility outweighs purity) and a conservative restriction for interfaces like Blob (which is purely computational in memory, but is withheld from [Exposed=*] because Blob objects are primarily useful alongside I/O APIs that do not exist in restricted scopes).

## Fit for Coding Agents

The principle has a mixed fit for AI coding agents. Much of it simply reflects physical browser engine constraints—real-time AudioWorklet or synchronous PaintWorklet threads lack an event loop and cannot block on I/O or localStorage, regardless of whether code is authored by a human or an LLM. Where the principle encourages universal exposure of foundational computational utilities (TextEncoder, TextDecoder, core AbortSignal) and makes a pragmatic exception for console, it directly helps coding agents. Agents rely heavily on console.log and console.error across every execution context to observe runtime behavior in their feedback loops, and having standard byte/string primitives available across Window, Worker, Worklet, and server/edge runtimes lets agents reuse idiomatic code without realm-specific branching.

However, the discretionary parts of this principle pull against how LLMs generalize across JavaScript environments. Because over 95% of web training data targets Window, Worker, or Node.js scopes (which all have event loops and standard globals), coding agents have weak statistical priors about what is missing in restricted realms like Worklet or ShadowRealm. First, partial interface exposure (exposing AbortSignal everywhere via [Exposed=*] while omitting AbortSignal.timeout() in non-event-loop scopes) splits a single conceptual API surface; when an agent knows AbortSignal is available in a scope, it strongly associates AbortSignal.timeout() as part of that class, leading to TypeError hallucinations unless strict per-realm TypeScript lib configurations are active. Second, advising spec authors to "conservatively" withhold purely computational interfaces like Blob from [Exposed=*] simply because they are usually paired with I/O breaks portability when agents generate or import shared in-memory data-handling helpers in restricted scopes.

Fortunately, when an agent does hallucinate an unexposed API in a restricted scope, the failure mode is loud and deterministic (ReferenceError or TypeError on the missing global or static method), allowing an agent with a runtime test or TypeScript check in its feedback loop to self-correct quickly.

## Value as a Slide Example

This principle is not a strong headline slide example (neither, 2/5) for the TPAC breakout session. The distinction between [Exposed=(Window,Worker)] and [Exposed=*] primarily affects niche execution environments without event loops—such as AudioWorklet, PaintWorklet, and ShadowRealm—rather than everyday web application development. Moreover, most of the rule is dictated by hard thread-safety and event-loop architecture rather than developer ergonomics.

If mentioned at all, its best use is as a brief supporting point on a broader slide about cross-context API consistency: specifically, how splitting an interface across scopes (AbortSignal without AbortSignal.timeout()) or conservatively hiding purely computational types (Blob) trips up LLM priors trained predominantly on main-thread Window code, whereas pragmatic universal exceptions like console are vital for agent debugging loops.
