---
section: "6.9"
id: "constructors"
title: "Classes should have constructors when possible"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#constructors"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Constructible WebIDL classes align with LLM priors for `new ClassName()`, prevent `TypeError: Illegal constructor` hallucinations, and unblock the automated unit-testing and mocking loops that coding agents depend on."
---

# §6.9 Classes should have constructors when possible

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §6.9 constructors — Classes should have constructors when possible: Constructible WebIDL classes align with LLM priors for `new ClassName()`, prevent `TypeError: Illegal constructor` hallucinations, and unblock the automated unit-testing and mocking loops that coding agents depend on.

- **URL:** https://w3ctag.github.io/design-principles/#constructors
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Constructible WebIDL classes align with LLM priors for `new ClassName()`, prevent `TypeError: Illegal constructor` hallucinations, and unblock the automated unit-testing and mocking loops that coding agents depend on.

## Principle Summary

By default, WebIDL interfaces generate non-constructible JavaScript classes where calling `new X()` throws a `TypeError: Illegal constructor`. Principle §6.9 advises specification authors to explicitly add `constructor` operations to WebIDL interfaces whenever possible—unless creating the object requires privileged access with significant side effects (such as `Window` via `window.open()`), asynchronous preparation (such as `ImageBitmap` via `createImageBitmap()`), or an abstract base class. Even where factory methods add value (for example, selecting among specialized subclasses), they should complement constructors rather than replace them.

For human developers, constructible classes enable two important capabilities: creating genuine instances of platform classes (like `new Event()`, `new MouseEvent()`, or `new Request()`) for unit testing, mocking, and passing to third-party libraries, and subclassing platform interfaces via standard JavaScript `class MyClass extends PlatformClass` syntax. Conversely, when interfaces like `DOMTokenList` lack constructors, developers cannot reuse or subclass those primitives in their own custom elements.

## Fit for Coding Agents

This principle is a strong positive fit (`good`) for AI coding agents because it directly supports the primary mechanism agents use to ensure correctness: automated self-testing and verification loops. Unlike human developers who often verify UI behavior manually in a live browser, coding agents rely heavily on writing unit and integration tests (in Vitest, Jest, or Web Test Runner) to validate their code autonomously. When a function consumes a platform object—such as `Event`, `Request`, `Response`, `File`, `Headers`, or `CSSStyleSheet`—constructibility allows the agent to synthesize genuine instances directly (`new MouseEvent('click', { clientX: 10 })` or `new Response(body, { status: 200 })`). These real instances satisfy TypeScript's type checker, pass `instanceof` checks, and carry the internal WebIDL slots needed to pass native brand checks when handed to browser APIs.

When WebIDL interfaces omit constructors, they trigger three systematic failure modes in coding agents. First, because WebIDL exposes global interface objects (`window.FileList`, `window.DOMTokenList`, `window.GeolocationPosition`) and TypeScript models them as classes, an LLM's strongest statistical prior when it needs an instance of `T` is to call `new T(...)`, resulting in immediate runtime `TypeError: Illegal constructor` failures. Second, when an agent attempts to work around `Illegal constructor` by generating a duck-typed mock (`{ 0: file, length: 1 } as unknown as FileList`) or `Object.create(DOMTokenList.prototype)`, the fake object lacks WebIDL internal slots and throws `TypeError: Illegal invocation` or fails WebIDL parameter brand checks at runtime. Third, non-constructible classes force agents either to rely on obscure indirect hacks (like instantiating `new DataTransfer()` just to populate `input.files` with a real `FileList`) or, in the case of `DOMTokenList` on custom elements, to reimplement the entire token-list parsing specification from scratch in userland JavaScript, wasting tokens and introducing edge-case bugs.

Finally, constructors unify the type name and the instantiation syntax (`const x: Foo = new Foo(...)`), which is maximally token-efficient and self-describing in the agent's context window. When object creation is hidden behind an external factory on an unrelated interface (e.g., legacy `document.createEvent('MouseEvents')` + 15-argument `initMouseEvent()` vs. `new MouseEvent(type, initDict)`, or `audioCtx.createBuffer()` vs. `new AudioBuffer()`), the agent cannot derive how to construct the value solely from the type signature it sees in context.

## Value as a Slide Example

This principle makes a strong (`4/5`), concrete `clearly-useful` slide example for TPAC because it elevates a principle originally framed around human convenience ("useful when testing, mocking, or subclassing") into a foundational requirement for agentic verification loops. Every browser engineer and web developer at TPAC recognizes `TypeError: Illegal constructor`, and contrasting modern constructible interfaces (`new Request()`, `new MouseEvent()`, `new CSSStyleSheet()`) against non-constructible holdouts (`FileList`, `DOMTokenList`, `GeolocationPosition`) creates an immediately relatable visual.

On a slide, you can contrast two real agent testing trajectories side by side: with constructible APIs (`new Request(url, init)` or `new CustomEvent(name, { detail })`), the agent writes a two-line unit test that passes both TypeScript and WebIDL brand checks on the first turn; with non-constructible APIs (`new FileList([file])` or `new DOMTokenList()`), the agent hits `TypeError: Illegal constructor`, falls back to a TypeScript-cast mock `{ 0: file, length: 1 } as unknown as FileList`, crashes again on WebIDL's native brand check (`Failed to set the 'files' property on 'HTMLInputElement'`), and wastes multiple turns before stumbling onto the obscure `new DataTransfer().files` workaround.
