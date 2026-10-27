---
section: "12.6"
id: "naming-unsafe"
title: "Warn about dangerous features"
chapter: "12. Naming principles"
url: "https://w3ctag.github.io/design-principles/#naming-unsafe"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Marking guarantee-weakening features with 'unsafe' embeds explicit security semantics into the token stream, activating LLM safety priors and enabling trivial deterministic gating in agent harnesses and review loops."
---

# §12.6 Warn about dangerous features

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §12.6 naming-unsafe — Warn about dangerous features: Marking guarantee-weakening features with 'unsafe' embeds explicit security semantics into the token stream, activating LLM safety priors and enabling trivial deterministic gating in agent harnesses and review loops.

- **URL:** https://w3ctag.github.io/design-principles/#naming-unsafe
- **Chapter:** 12. Naming principles
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Marking guarantee-weakening features with 'unsafe' embeds explicit security semantics into the token stream, activating LLM safety priors and enabling trivial deterministic gating in agent harnesses and review loops.

## Principle Summary

W3C TAG Design Principle §12.6 recommends that when a web platform feature weakens security, layout, or correctness guarantees normally provided to developers, its name should explicitly include `"unsafe"` so that the risk is immediately noticeable at the call site or configuration point. The principle cites Content Security Policy (CSP) keywords such as `'unsafe-inline'` (alongside `'unsafe-eval'` and `'unsafe-hashes'`), which weaken CSP's injection protections; other platform examples include `Element.prototype.setHTMLUnsafe()`, `Document.parseHTMLUnsafe()`, Referrer-Policy's `unsafe-url`, and CSS Box Alignment's `unsafe` overflow keyword.

For human developers, this naming convention acts as speed-bump ergonomics: typing or reading the word `unsafe` creates cognitive friction during authoring and makes security-sensitive escape hatches stand out during code review, discouraging casual copy-pasting of dangerous configurations.

## Fit for Coding Agents

This principle is a good fit for AI coding agents because LLMs are fundamentally lexical and statistical engines that rely heavily on identifier semantics in the token stream. Across the broader programming corpus—such as Rust's `unsafe` blocks, Go's `unsafe` package, C#'s `unsafe` keyword, and React's `dangerouslySetInnerHTML`—the token `"unsafe"` carries a strong statistical and post-training (RLHF/instruction-tuning) prior associated with security boundaries, XSS sinks, and audit scrutiny. When a web API follows §12.6—such as pairing `setHTML()` with `setHTMLUnsafe()`—that cross-language prior transfers directly: coding agents are primed to prefer the safe default, explain the risk when forced to use the `unsafe` variant, and flag `unsafe` occurrences when acting as code-review subagents.

By contrast, legacy web platform APIs that predate or violate this principle—most notably `element.innerHTML`—attach dangerous XSS sinks to the shortest, most innocuous-looking property names. Because `innerHTML` carries no lexical warning in the token stream and dominates historical training data, LLMs routinely emit it by default for DOM updates without triggering safety heuristics. Naming dangerous escape hatches explicitly (`setHTMLUnsafe`, `parseHTMLUnsafe`, `'unsafe-inline'`, `'unsafe-eval'`) makes code self-describing in context without requiring the model or review harness to infer hidden security side effects from surrounding data flow.

There is an important agentic nuance: unlike humans, an LLM agent does not experience psychological hesitation when typing `"unsafe"`. When an autonomous agent is iterating in a closed feedback loop trying to silence a browser console error or pass an end-to-end test, it may still reach for `'unsafe-inline'` or `'unsafe-eval'` in a CSP header because those tokens frequently co-occur with "fix CSP error" workarounds in pre-training data. Yet even in that failure mode, §12.6 proves its value for agentic workflows: because the bypass is lexically marked with `unsafe`, deterministic agent guardrails, pre-commit hooks, linters, and verification subagents can trivially detect and block the escape hatch with simple pattern or AST checks.

## Value as a Slide Example

§12.6 is a strong (`4/5`), `clearly-useful` slide example for TPAC because it connects familiar Web API evolution (`innerHTML` vs. `setHTML()` / `setHTMLUnsafe()`, and CSP's `'unsafe-inline'`) with how LLMs and agentic harnesses actually process code. Standardizing explicit lexical markers for dangerous operations directly counters a classic failure mode of AI code generation: models casually reproducing insecure legacy idioms (`innerHTML`) that look benign at the token level.

On a slide, it also offers a crisp takeaway on how the *mechanism* of a good design principle shifts from humans to agents. For humans, `unsafe` in an API name works through authoring friction—making a developer pause before typing it. For coding agents, `unsafe` works through token-space security priors during generation (steering the model toward `setHTML()` over `setHTMLUnsafe()`) and deterministic harness checkability, giving review agents and guardrails an unambiguous lexical hook to gate dangerous escape hatches before code ships.
