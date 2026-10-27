---
section: "6.4"
id: "attributes-vs-methods"
title: "Accessors should behave like properties, not methods"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#attributes-vs-methods"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Strong fit for coding agents: LLMs rely heavily on the syntactic prior that property reads are pure, cheap, non-throwing, and referentially stable (obj.prop === obj.prop), and violations cause silent bugs (like layout thrashing or infinite reactive re-renders) that agent test loops rarely catch."
---

# §6.4 Accessors should behave like properties, not methods

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §6.4 attributes-vs-methods — Accessors should behave like properties, not methods: Strong fit for coding agents: LLMs rely heavily on the syntactic prior that property reads are pure, cheap, non-throwing, and referentially stable (obj.prop === obj.prop), and violations cause silent bugs (like layout thrashing or infinite reactive re-renders) that agent test loops rarely catch.

- **URL:** https://w3ctag.github.io/design-principles/#attributes-vs-methods
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Strong fit for coding agents: LLMs rely heavily on the syntactic prior that property reads are pure, cheap, non-throwing, and referentially stable (obj.prop === obj.prop), and violations cause silent bugs (like layout thrashing or infinite reactive re-renders) that agent test loops rarely catch.

## Principle Summary

W3C TAG §6.4 ("Accessors should behave like properties, not methods") specifies that IDL attributes (getters and setters) must behave like regular JavaScript data properties. Getters must not have observable side effects, should not throw exceptions on read (invalid state should be rejected on write instead), and must not perform synchronous blocking operations—explicitly citing layout-forcing DOM getters like `offsetTop` as an antipattern.

Additionally, getters must preserve referential identity (`obj.property === obj.property` when underlying state is unchanged) and should preserve values across write-then-read (`obj.property = x` implies `obj.property === x` under normal conditions). While live objects may be returned from either properties or methods (returning the same object until state changes), static snapshots that allocate and return a new object on every call must be methods.

## Fit for Coding Agents

This principle is a strong, direct fit for AI coding agents because LLMs are statistical pattern matchers governed by local syntactic cues. Across billions of lines of JavaScript and TypeScript training data, property access (`obj.prop`) carries an overwhelming prior: it is pure, cheap, non-throwing, and referentially stable. Method invocation (`obj.getSnapshot()`, `obj.compute()`), by contrast, syntactically signals computation, allocation, side effects, or potential failure. When Web APIs blur this line, coding agents fall into subtle traps because the local syntax contradicts the hidden runtime behavior.

Crucially, violating the property contract typically produces *silent* bugs rather than loud exceptions, defeating the agent's verification loop. First, because legacy DOM getters like `element.offsetTop`, `element.offsetHeight`, and `element.clientWidth` look like simple property reads, coding agents routinely interleave them with style mutations inside loops (`el.style.top = ...; const h = el.offsetHeight;`), introducing catastrophic synchronous layout thrashing while all functional tests pass. Second, agent-generated frontend code heavily targets reactive frameworks (such as React `useEffect` and `useMemo` dependency arrays); if a getter returns a newly allocated object on each read (`obj.prop !== obj.prop`), an agent passing `[obj.prop]` as a dependency triggers infinite re-render loops, or writes `obj.prop.sub = x` and silently mutates a throwaway object.

Finally, adhering to side-effect-free, non-throwing getters protects the agent's own tooling and feedback loop. Agentic test runners, DevTools bridges, and REPL harnesses routinely enumerate and serialize object properties to summarize runtime state for the model. Getters that throw exceptions on read or mutate state when observed can break automated state inspection or cause Heisenbugs when an agent inspects an object during debugging.

## Value as a Slide Example

This principle is a strong `clearly-useful` slide candidate (`4/5`) because it illustrates how classic Web IDL ergonomics directly govern LLM failure modes—specifically how hidden costs or allocations behind property syntax cause silent bugs that escape an agent's test runner.

It provides two concrete, immediately recognizable Web API examples for a slide: (1) `el.offsetTop` / `el.offsetHeight` tricking coding agents into writing layout-thrashing loops because they look like free property reads and never fail functional tests, and (2) `obj.prop === obj.prop` preventing LLM-written React `useEffect([obj.prop])` hooks from entering infinite render loops (or silently mutating ephemeral snapshot objects when writing `obj.prop.x = y`), showing why static snapshots must be methods (`getBoundingClientRect()`) rather than getters.
