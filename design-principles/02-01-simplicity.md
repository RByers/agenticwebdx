---
section: "2.1"
id: "simplicity"
title: "Prefer simple solutions"
chapter: "2. API Design Across Languages"
url: "https://w3ctag.github.io/design-principles/#simplicity"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Making common use cases simple remains vital for coding agents—not to save typing keystrokes, but to minimize multi-step state bugs, reduce context-window token bloat, improve cross-browser interop, and keep agents from defaulting to third-party wrappers."
---

# §2.1 Prefer simple solutions

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §2.1 simplicity — Prefer simple solutions: Making common use cases simple remains vital for coding agents—not to save typing keystrokes, but to minimize multi-step state bugs, reduce context-window token bloat, improve cross-browser interop, and keep agents from defaulting to third-party wrappers.

- **URL:** https://w3ctag.github.io/design-principles/#simplicity
- **Chapter:** 2. API Design Across Languages
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Making common use cases simple remains vital for coding agents—not to save typing keystrokes, but to minimize multi-step state bugs, reduce context-window token bloat, improve cross-browser interop, and keep agents from defaulting to third-party wrappers.

## Principle Summary

W3C TAG Design Principle §2.1 ("Prefer simple solutions") advises specification authors to look hard for simple designs that address well-defined user needs without scope creep. It notes that simpler features are easier for browsers to implement and test, more likely to be interoperable across user agents, and easier for web authors to understand.

Crucially, the principle emphasizes progressive disclosure of complexity: "It is especially important to design your feature so that the most common use cases are easy to accomplish," citing Alan Kay's maxim that "simple things should be simple, complex things should be possible." While rare or advanced use cases may legitimately require more involved APIs, everyday tasks should not force authors through complex ceremony.

## Fit for Coding Agents

At first glance, it is tempting to argue that coding agents make API simplicity less important: because LLMs can generate dozens of lines of boilerplate in milliseconds, the human cost of typing or memorizing a complex API disappears. In practice, however, §2.1 aligns strongly with agent ergonomics (`good`), because conceptual and stateful simplicity matters just as much to an LLM as it does to a human developer—just for different reasons. When a common task requires orchestrating multiple low-level objects, lifecycle callbacks, and state transitions (such as wiring up raw `XMLHttpRequest` events, manual `ReadableStream` readers, or custom modal focus/light-dismiss traps), every extra step is a surface where an agent can drop an error handler, misorder state updates, or leak resources. High-level, simple APIs for the common case—such as `fetch()`, `structuredClone()`, `<dialog>`, or `popover`—collapse fragile imperative glue into a single declarative or atomic operation that an agent gets right on the first pass.

Furthermore, while generating tokens is relatively cheap, reading and maintaining verbose boilerplate across many turns in an agentic coding loop consumes valuable context window budget and makes diffs harder for both humans and verification agents to audit. When the web platform fails to make common things simple, coding agents rarely write clean, canonical low-level Web API code from scratch; instead, their training priors steer them toward pulling in third-party npm packages or copy-pasting inconsistent helper functions into every project. The principle's point that simpler specs yield better cross-browser interoperability also directly helps agents, which otherwise struggle with subtle engine divergences that are poorly represented in training data.

The key nuance for standards design is distinguishing conceptual simplicity from syntactic terseness. Humans often equate simplicity with fewer characters to type (sometimes leading to overloaded positional arguments or implicit magic defaults), whereas agents thrive on explicit, self-describing option dictionaries and predictable state models. And for the second half of Alan Kay's quote ("complex things should be possible"), agents genuinely do lower the barrier to adopting complex, lower-level escape hatches when needed—provided those complex APIs are regular, strongly typed, and fail loudly when misused.

## Value as a Slide Example

This principle is a strong (4/5), `clearly-useful` slide candidate because it directly confronts one of the biggest misconceptions in the "Agents and Web DX" conversation: the claim that "we only need low-level primitives now because AI can write the boilerplate." Featuring §2.1—and specifically Alan Kay's "simple things should be simple, complex things should be possible"—gives a memorable framework for explaining how agents shift the curve without overturning the rule: agents make "complex things should be possible" much more accessible (e.g., synthesizing verbose WebGPU pipeline setup or Web Audio graphs), but "simple things should be simple" remains non-negotiable for reliability and context efficiency.

Concrete Web API contrasts—such as `<button popovertarget="...">` or `<dialog>` vs. 80 lines of agent-generated JS/ARIA light-dismiss and focus-management code, `fetch()` vs. `XMLHttpRequest`, or `structuredClone()` vs. custom recursive cloning—vividly illustrate why high-level simplicity prevents hallucinated edge-case bugs, saves context tokens, and keeps agent-authored apps free of unnecessary third-party dependencies. It scores a 4/5 rather than a 5/5 only because "Prefer simple solutions" is a broad umbrella principle that works best on a slide when explicitly contrasting human simplicity (fewer keystrokes) with agent simplicity (fewer stateful steps and explicit, local intent).
