---
section: "2.3"
id: "name-thoughtfully"
title: "Name things thoughtfully"
chapter: "2. API Design Across Languages"
url: "https://w3ctag.github.io/design-principles/#name-thoughtfully"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Thoughtful, semantically accurate API names directly align with LLM subword tokenization and natural-language priors, reducing hallucinations—though §2.3 itself is only a brief pointer to the detailed naming rules."
---

# §2.3 Name things thoughtfully

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §2.3 name-thoughtfully — Name things thoughtfully: Thoughtful, semantically accurate API names directly align with LLM subword tokenization and natural-language priors, reducing hallucinations—though §2.3 itself is only a brief pointer to the detailed naming rules.

- **URL:** https://w3ctag.github.io/design-principles/#name-thoughtfully
- **Chapter:** 2. API Design Across Languages
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Thoughtful, semantically accurate API names directly align with LLM subword tokenization and natural-language priors, reducing hallucinations—though §2.3 itself is only a brief pointer to the detailed naming rules.

## Principle Summary

Section 2.3 ("Name things thoughtfully") states a foundational rule for web platform API design: name APIs with care because good names make it much easier for web authors to use APIs correctly. Rather than enumerating detailed rules inline, this two-sentence section acts as a high-level entry point in Chapter 2 ("API Design Across Languages") that forwards readers to the dedicated "Naming principles" chapter for concrete guidance.

For human developers and spec authors, the principle exists because API identifiers are the primary user interface of the web platform. Clear, predictable names reduce cognitive load, improve code readability during maintenance, and prevent bugs caused by misunderstanding what a method, property, or event actually does.

## Fit for Coding Agents

Thoughtful naming is an exceptionally good fit for AI coding agents—arguably even more critical to how LLMs operate mechanically than it is for humans using IDE autocomplete. To a compiler or browser engine, an identifier is an arbitrary symbol; to an LLM, an identifier is decomposed into subword tokens whose embeddings are deeply intertwined with natural-language semantics and cross-language programming conventions learned during pre-training. When a web API is named accurately and predictably (such as `AbortController.abort()`, `Element.scrollIntoView()`, or `Array.prototype.includes()`), the model's statistical priors naturally guide it toward the right call site, argument types, return value, and side effects without needing to spend context-window tokens retrieving external documentation.

Conversely, poorly or deceptively named APIs create persistent statistical traps for coding agents. When an identifier's natural-language meaning diverges from its runtime behavior or neighboring APIs—such as the classic confusion between `Array.prototype.slice` (non-mutating subarray) and `Array.prototype.splice` (in-place mutation), `Node.contains()` vs. `DOMTokenList.contains()` vs. `Array.prototype.includes()`, or `history.pushState(state, unusedTitle, url)` where the second parameter misleads models into passing meaningful titles—LLMs frequently hallucinate wrong arguments or misuse the return value. Furthermore, when agents read existing code in a repository, self-describing API names compress semantic intent directly into the local token context, improving multi-step reasoning and refactoring accuracy.

For newly shipped Web APIs that appear post-cutoff or have sparse representation in pre-training corpora, thoughtful naming is the difference between zero-shot usability and guaranteed hallucination. An agent asked to use a newer capability will guess method and property names based on established platform patterns and English semantics (`Popover`, `ViewTransition`, `scheduler.yield()`); when the spec's chosen names match those priors, agents often succeed with minimal or no in-context documentation.

## Value as a Slide Example

This principle is a `clearly-useful` example for a TPAC presentation on agentic DX, earning a moderate `example_strength` of 3/5. The underlying thesis—that "naming is prompt engineering built into the platform" because LLMs reason directly through subword tokens—is a compelling, high-level takeaway for standards authors who might otherwise assume that agents don't care about ergonomics or can memorize any arbitrary symbol table. Concrete contrasts like `Array.prototype.includes()` (clear, zero-shot predictable) vs. `splice`/`slice` or `XMLHttpRequest` (confusing or archaic naming) immediately resonate with a technical audience.

However, §2.3 itself rates a 3/5 rather than a 5/5 because its text is just a two-sentence umbrella pointer to the detailed Naming Principles chapter (Chapter 5). On a slide, "Name things thoughtfully" is too generic on its own unless paired with the specific, actionable naming rules it references—such as consistency across the platform, using common words, or aligning verb/noun conventions with mutability and return types.
