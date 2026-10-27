---
section: "1.1"
id: "priority-of-constituencies"
title: "Put user needs first (Priority of Constituencies)"
chapter: "1. Principles behind design of Web APIs"
url: "https://w3ctag.github.io/design-principles/#priority-of-constituencies"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "The Priority of Constituencies remains the foundational justification for caring about agentic DX—because 'ease of authoring affects how content reaches users' and putting authors ahead of implementors and theoretical purity prevents offloading fragile boilerplate onto LLM-generated userland code."
---

# §1.1 Put user needs first (Priority of Constituencies)

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §1.1 priority-of-constituencies — Put user needs first (Priority of Constituencies): The Priority of Constituencies remains the foundational justification for caring about agentic DX—because 'ease of authoring affects how content reaches users' and putting authors ahead of implementors and theoretical purity prevents offloading fragile boilerplate onto LLM-generated userland code.

- **URL:** https://w3ctag.github.io/design-principles/#priority-of-constituencies
- **Chapter:** 1. Principles behind design of Web APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** The Priority of Constituencies remains the foundational justification for caring about agentic DX—because 'ease of authoring affects how content reaches users' and putting authors ahead of implementors and theoretical purity prevents offloading fragile boilerplate onto LLM-generated userland code.

## Principle Summary

The Priority of Constituencies is the W3C's foundational decision-making hierarchy for resolving design trade-offs on the web platform: end-user needs come before web page authors, which come before user agent implementors, which come before specification writers, which come before theoretical purity. Grounded in RFC 8890 (The Internet is for End Users), it requires API designers to identify and document the concrete end-user need before designing any feature, ensuring that platform evolution serves human agency, safety, accessibility, and privacy above downstream convenience.

Crucially, the principle also notes that this hierarchy is not a rigid excuse to ignore developer ergonomics: "Ease of authoring affects how content reaches users." Because user agents and spec writers have finite engineering resources and authors mediate what actually gets built and shipped, making the right thing easy for authors is recognized as an essential mechanism for delivering good outcomes to end users.

## Fit for Coding Agents

This principle aligns strongly with AI coding agents and becomes even more important as agents mediate a growing share of web development, though it shifts what "ease of authoring" looks like in practice. First, the rule that author needs come before implementor needs, spec writers, and theoretical purity directly counters a dangerous misconception in the LLM era: the temptation for browser vendors to say "we don't need high-level platform primitives because coding agents can generate the JavaScript boilerplate for free." When the platform forces agents to synthesize complex low-level glue—such as custom modal focus trapping, scroll locking, floating-element positioning math, or verbose ReadableStream byte plumbing—every agent invocation burns context tokens and risks stochastic hallucinations. Worse, those errors are often non-visual (e.g., broken screen-reader navigation, subtle memory leaks, or race conditions) and pass a quick screenshot check in the agent's feedback loop. High-level, browser-managed primitives like <dialog>, popover, CSS Anchor Positioning, and fetch() put implementor effort at the service of authors and agents, collapsing hundreds of error-prone tokens into declarative semantics where the browser guarantees end-user invariants.

Second, the principle's explicit link—"Ease of authoring affects how content reaches users"—is the single strongest standards-level argument for why Agent DX is a User Need. When a Web API is poorly suited to coding agents (for instance, relying on ambiguous positional booleans, failing silently instead of throwing actionable errors in the tool-use loop, or exposing overly abstract "theoretically pure" interfaces that diverge from statistical training priors), the agent's failure directly harms the end user through broken accessibility, main-thread jank, or bloated legacy dependencies pulled from training data.

Third, the top tier of the hierarchy (user needs > author needs) actually becomes easier to uphold when agents write the code. Historically, standards bodies often compromised on strictness—allowing silent HTML/JS failure modes, implicit type coercion, or optional accessibility/security annotations—because human authors resisted typing ceremony and boilerplate. Coding agents do not suffer from keystroke fatigue; they can effortlessly generate verbose, explicit, user-protective code (such as full ARIA semantics, responsive <picture> source sets, or strict Content Security Policy / Trusted Types wiring) provided the platform makes violations fail loudly and deterministically during the agent's verification loop. Thus, putting user needs first in an agentic world means trading away forgiving "human typing shortcuts" in favor of explicit, machine-verifiable contracts that protect the end user.

## Value as a Slide Example

This is a top-tier (5/5) slide example for a W3C TPAC audience. Every standards participant knows the Priority of Constituencies by heart (Users > Authors > Implementors > Spec writers > Theoretical purity), and skeptics in the room will naturally ask where AI coding agents fit in that hierarchy—or argue that standards shouldn't cater to LLMs at all. Putting §1.1 on a slide immediately bridges that gap using the TAG's own words: "Ease of authoring affects how content reaches users." When agents write the code, agent ergonomics directly determines the quality, accessibility, and performance of what reaches end users.

It also provides a crisp, memorable framework for concrete Web API comparisons on the slide: (1) Authors & Users > Implementors (<dialog>, popover, and CSS Anchor Positioning vs. custom JS glue), showing why offloading UI mechanics onto "let the agent write 200 lines of JS" violates Priority of Constituencies by introducing hallucinated focus traps and accessibility bugs; (2) Authors > Theoretical Purity (fetch() vs. raw Web Streams or WebGPU ceremony), showing how pragmatic high-level APIs reduce token waste and hallucination; and (3) Users > Human Keystroke Convenience, showing how agents remove the need to compromise user safety or strict validation just to save human keystrokes.
