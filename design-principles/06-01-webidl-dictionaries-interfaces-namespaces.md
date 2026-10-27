---
section: "6.1"
id: "webidl-dictionaries-interfaces-namespaces"
title: "Use WebIDL dictionaries, interfaces, and namespaces appropriately"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#webidl-dictionaries-interfaces-namespaces"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Matching WebIDL constructs to their actual semantics—plain dictionaries for data bags, interfaces for stateful objects, and namespaces for static utilities—aligns APIs with LLM JavaScript/TypeScript priors and prevents 'Illegal constructor' and serialization hallucinations."
---

# §6.1 Use WebIDL dictionaries, interfaces, and namespaces appropriately

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §6.1 webidl-dictionaries-interfaces-namespaces — Use WebIDL dictionaries, interfaces, and namespaces appropriately: Matching WebIDL constructs to their actual semantics—plain dictionaries for data bags, interfaces for stateful objects, and namespaces for static utilities—aligns APIs with LLM JavaScript/TypeScript priors and prevents 'Illegal constructor' and serialization hallucinations.

- **URL:** https://w3ctag.github.io/design-principles/#webidl-dictionaries-interfaces-namespaces
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Matching WebIDL constructs to their actual semantics—plain dictionaries for data bags, interfaces for stateful objects, and namespaces for static utilities—aligns APIs with LLM JavaScript/TypeScript priors and prevents 'Illegal constructor' and serialization hallucinations.

## Principle Summary

Section 6.1 ("Use WebIDL dictionaries, interfaces, and namespaces appropriately") is the introductory principle for structuring JavaScript APIs in WebIDL. It states that because dictionaries, interfaces, and namespaces each have distinct semantics and JavaScript bindings, spec authors should choose the construct that matches the purpose of the API rather than defaulting to interfaces for everything.

For human developers and browser engines, this principle exists to ensure Web Platform APIs feel consistent with idiomatic JavaScript and to avoid anti-patterns like "fake classes" (interfaces that cannot be constructed or exist only to hold static methods) or hollow classes that wrap plain data without providing any behavior.

## Fit for Coding Agents

This principle is a good fit for AI coding agents because LLM code generation is strongly governed by general JavaScript and TypeScript priors. In idiomatic JS/TS, plain object literals (`{ ... }`) represent stateless data bags and options, classes (`new Foo()`) represent stateful entities with lifecycle and methods, and namespaces (`Math`, `JSON`, `CSS`) group static utilities. When Web APIs misuse WebIDL interfaces to create "fake classes"—such as interfaces that cannot be instantiated, hold no behavior, or act merely as bags of properties or static method containers—agents frequently hallucinate `new SomeInterface()` (triggering `TypeError: Illegal constructor` at runtime) or attempt to pass a plain `{}` literal where a nominal interface instance is demanded.

Furthermore, choosing between WebIDL dictionaries and interfaces directly affects serialization and introspection in agent feedback loops. Because WebIDL interface attributes are defined as getters on the prototype chain rather than own enumerable properties, agents that log, spread (`{ ...obj }`), or `JSON.stringify()` an interface instance without a dedicated serializer silently get `{}`. Using WebIDL dictionaries for data and configuration avoids this silent failure mode and reduces token ceremony by letting agents write inline object literals directly at the call site.

Finally, WebIDL constructs map 1:1 into TypeScript's `lib.dom.d.ts` definitions. When specs use dictionaries, interfaces, and namespaces appropriately, TypeScript structural typing works naturally for data bags while nominal class checks guard stateful objects, giving coding agents fast, unambiguous compiler diagnostics in their edit-verify loop.

## Value as a Slide Example

This principle is a `clearly-useful` candidate for a TPAC slide (`3/5` strength) because its warning against "fake classes" directly captures a common failure mode for coding agents on legacy Web APIs. Contrasting legacy non-constructible or hollow DOM interfaces (where agents hit `TypeError: Illegal constructor` or get `{}` from `JSON.stringify()`) against modern WebIDL dictionary and namespace usage (`fetch(url, { method, headers })`, `DOMPointInit`, `CSS.supports()`) makes the value of idiomatic JS constructs immediately concrete.

It earns a `3/5` rather than a `5/5` only because §6.1 is a short three-sentence umbrella introduction whose specific rules are detailed in the subsections that follow it. On a slide, it is best combined with its child principles as part of a unified point on why idiomatic JS data shapes and avoiding "fake classes" matter for LLM priors and type-checking.
