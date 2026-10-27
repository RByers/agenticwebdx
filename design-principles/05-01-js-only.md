---
section: "5.1"
id: "js-only"
title: "Use JavaScript for Web APIs"
chapter: "5. JavaScript Language"
url: "https://w3ctag.github.io/design-principles/#js-only"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Designing Web APIs around native JavaScript conventions aligns with LLM training priors and avoids alien IDL host-object footguns, provided APIs remain statically describable in TypeScript."
---

# §5.1 Use JavaScript for Web APIs

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §5.1 js-only — Use JavaScript for Web APIs: Designing Web APIs around native JavaScript conventions aligns with LLM training priors and avoids alien IDL host-object footguns, provided APIs remain statically describable in TypeScript.

- **URL:** https://w3ctag.github.io/design-principles/#js-only
- **Chapter:** 5. JavaScript Language
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Designing Web APIs around native JavaScript conventions aligns with LLM training priors and avoids alien IDL host-object footguns, provided APIs remain statically describable in TypeScript.

## Principle Summary

This brief introductory principle for Chapter 5 ("JavaScript Language") states that imperative Web APIs should be designed specifically for JavaScript rather than kept generalized for multi-language bindings. Spec authors are encouraged to rely freely on JavaScript-specific semantics and conventions—such as classes, constructors, and first-class method/function references—rather than designing lowest-common-denominator interfaces.

Historically, early W3C DOM specifications (DOM Levels 1–3) used language-neutral OMG IDL so the same interfaces could map to Java, C++, and CORBA alongside ECMAScript. That produced un-idiomatic, high-ceremony APIs in the browser: collections like `HTMLCollection` and `NodeList` that looked like arrays but lacked `Array.prototype` methods and required `.item(i)`, factory ceremonies like `document.createEvent("MouseEvents")` followed by 15-argument `initMouseEvent(...)` calls instead of constructors, and verbose getter/setter methods instead of properties and dictionaries. §5.1 codifies the shift toward treating JavaScript as the primary host language of the Web Platform.

## Fit for Coding Agents

This principle is a good fit for AI coding agents because LLMs form strong statistical priors over general JavaScript and TypeScript idioms across their entire training corpus. When Web Platform APIs behave like ordinary JavaScript objects—using `new` class constructors (`new CustomEvent()`, `new IntersectionObserver()`), standard `Promise` returns, iterable protocols (`for...of`), first-class callbacks, and options dictionaries—agents can transfer their general JS patterns directly to DOM and Web APIs with minimal token overhead and high first-try accuracy.

Conversely, historical violations of this principle (where DOM objects act as alien, language-neutral host objects rather than true JavaScript constructs) are among the most persistent hallucination traps for coding agents. A classic example is an LLM calling `.map()`, `.filter()`, or `.find()` directly on `document.getElementsByClassName(...)` (`HTMLCollection`) or `element.attributes` (`NamedNodeMap`) because its JavaScript priors strongly associate bracket-indexed collections with `Array.prototype` methods—resulting in runtime `TypeError: ...map is not a function` failures. Similarly, legacy multi-step initialization ceremonies (`createEvent` / `initEvent`) waste tokens and invite ordering bugs compared to idiomatic JS constructors and options objects.

There is, however, an important modern caveat for coding agents: "freely rely upon language-specific semantics" should not mean relying on untyped dynamic JS cleverness. In agentic workflows, the de facto language of the web is TypeScript, and the TypeScript compiler (`tsc` backed by WebIDL-generated `lib.dom.d.ts`) is the agent's fastest, highest-signal verification loop before running a browser. When an API leans too heavily into dynamic JS quirks—such as untyped expando properties, highly overloaded signatures whose return types depend on runtime values, or implicit `this` binding magic—it weakens static type checkability. Thus, while embracing standard JS classes, iterables, Promises, and callbacks helps agents enormously, pairing JS idioms with crisp WebIDL/TypeScript type definitions is what makes them truly agent-friendly.

## Value as a Slide Example

As a TPAC slide example, §5.1 is moderately useful (3/5). It frames a clear historical contrast and a forward-looking twist: whenever the Web Platform deviates from standard JS conventions (e.g., `HTMLCollection` lacking `Array.prototype.map` because of legacy language-neutral DOM Level 1 IDL), coding agents reliably hallucinate standard JS methods onto DOM host objects. Furthermore, it sets up a sharp TPAC 2026 provocation: while the TAG told spec authors to design for JavaScript instead of Java/C++, coding agents overwhelmingly write and verify TypeScript—meaning Web APIs must not only feel like idiomatic JS, but also remain statically describable in `lib.dom.d.ts`.

However, it is a 3/5 rather than a 5/5 headline example on its own because §5.1 is a brief two-sentence chapter introduction settling a 2000s-era debate over language-neutral OMG IDL bindings, while the specific, high-impact API mechanics (options dictionaries, Promises, constructors, live vs. static collections) are covered by the more concrete principles later in Chapter 5.
