---
section: "2.4"
id: "consistency"
title: "Be consistent"
chapter: "2. API Design Across Languages"
url: "https://w3ctag.github.io/design-principles/#consistency"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 5
verdict: "Consistency is the single strongest multiplier for LLM coding accuracy because models predict tokens from statistical precedent, enabling zero-shot generalization to new APIs and preventing hallucinated signatures."
---

# §2.4 Be consistent

GREP_SUMMARY: slide_example=clearly-useful | strength=5/5 | agent_fit=good | §2.4 consistency — Be consistent: Consistency is the single strongest multiplier for LLM coding accuracy because models predict tokens from statistical precedent, enabling zero-shot generalization to new APIs and preventing hallucinated signatures.

- **URL:** https://w3ctag.github.io/design-principles/#consistency
- **Chapter:** 2. API Design Across Languages
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 5/5
- **Verdict:** Consistency is the single strongest multiplier for LLM coding accuracy because models predict tokens from statistical precedent, enabling zero-shot generalization to new APIs and preventing hallucinated signatures.

## Principle Summary

W3C TAG §2.4 ("Be consistent") states that API designers should follow established precedent and only break consistency when the resulting usability improvement is very significant. Because the web platform has evolved over decades and contains multiple conflicting precedents, the principle advises weighing which precedent to follow using three criteria: prevalence (prefer the more popular precedent), API ergonomics (prefer the more usable precedent), and API age (prefer the newer precedent).

It also addresses the tension between internal consistency (consistency within the specific technology like CSS or JavaScript, and with the broader web platform) and external consistency (consistency with an outside specialized domain). Because most users of a web API are primarily familiar with the host web technology in which the API is defined, the principle advises erring on the side of internal consistency with that technology.

## Fit for Coding Agents

This principle is an exceptionally strong fit for AI coding agents—arguably even more critical for LLMs than for humans—because transformer models are fundamentally statistical precedent engines. When a newly standardized or less common Web API follows established platform idioms—such as `EventTarget` with `addEventListener(type, fn, { once, signal })`, `AbortSignal` in options bags, standard `Observer` lifecycle methods (`observe()`, `unobserve()`, `disconnect()`), or CSS property value conventions—an LLM can zero-shot or few-shot generalize to it even when the API is post-cutoff or sparsely represented in pre-training data. Conversely, the TAG rule that breaking consistency requires a *very significant* usability improvement applies with even greater force to coding agents: when an API makes a minor, bespoke "ergonomic" deviation from precedent (such as swapping parameter order, inventing a custom teardown method name instead of `.close()` or `.abort()`, or slightly altering an options dictionary shape), the model's strong statistical prior for the dominant platform pattern overwhelms the subtle exception and causes persistent hallucinations.

The principle's tie-breakers for conflicting precedents (prevalence, ergonomics, and age) and internal vs. external consistency also map directly onto LLM mechanics with revealing nuances. For an LLM, *prevalence* equals training-data frequency—the primary driver of next-token probabilities. When the web platform consistently applies the same *newer* precedent across all modern APIs (such as Promises paired with `{ signal }` options), that modern idiom accumulates massive aggregate cross-API weight in training corpora, allowing models to overcome the legacy gravity of older APIs. Similarly, on internal vs. external consistency, LLMs differ from human specialists because they are polyglots trained on all languages and outside domains simultaneously (POSIX, SQL, C++, Python). When a Web API borrows external domain concepts halfway—using external names with subtly different web semantics—the model suffers cross-domain interference and hallucinates methods from the external ecosystem; anchoring firmly to internal web-platform and host-language conventions keeps token generation grounded in the surrounding JS/CSS context.

## Value as a Slide Example

§2.4 is a top-tier (5/5) `clearly-useful` slide example because it captures the core thesis of how LLM coding agents interact with API design in a single memorable framing: "For humans, consistency reduces cognitive load; for LLMs, consistency *is* the prediction mechanism." It directly explains why "small ergonomic tweaks" that break platform conventions backfire with coding agents—models will stubbornly predict the dominant platform pattern rather than a bespoke one-off signature.

Concrete Web API examples make this immediately tangible for a W3C audience: on the positive side, converging on `{ signal: abortController.signal }` across `fetch()`, `addEventListener()`, Web Locks, Streams, and `scheduler.postTask()` allows agents to cancel any modern async Web API zero-shot without needing its specific docs in context. On the negative side, proliferating slightly different teardown/unsubscription idioms across platform generations (`removeEventListener`, `disconnect()`, `unobserve()`, `abort()`, `cancel()`, `close()`, `releaseLock()`) or subtle callback argument-order reversals (`(value, key)` vs. `(key, value)`) create classic hallucination traps that require runtime error loops to fix.
