---
section: "6.2"
id: "attributes-like-data"
title: "Attributes should behave like data properties"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#attributes-like-data"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Strong fit for coding agents: LLMs treat property access as cheap, side-effect-free, and referentially stable, so getters that allocate new objects, perform expensive work, or trigger side effects cause silent bugs, lost mutations, and infinite reactive loops."
---

# §6.2 Attributes should behave like data properties

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §6.2 attributes-like-data — Attributes should behave like data properties: Strong fit for coding agents: LLMs treat property access as cheap, side-effect-free, and referentially stable, so getters that allocate new objects, perform expensive work, or trigger side effects cause silent bugs, lost mutations, and infinite reactive loops.

- **URL:** https://w3ctag.github.io/design-principles/#attributes-like-data
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Strong fit for coding agents: LLMs treat property access as cheap, side-effect-free, and referentially stable, so getters that allocate new objects, perform expensive work, or trigger side effects cause silent bugs, lost mutations, and infinite reactive loops.

## Principle Summary

Although WebIDL attributes are implemented under the hood as JavaScript accessor properties with getter and setter functions, W3C TAG §6.2 states that they should behave like ordinary JavaScript data properties. Specifically, getters must have no observable side effects, must not perform complex or expensive operations, and must preserve referential identity across reads (`obj.attribute === obj.attribute` must always be `true`, never creating a new value each time the getter is called). Where possible, setting a property should also preserve identity (`obj.attribute = x` implies `obj.attribute === x`, unless type conversion is required).

If a capability cannot satisfy these data-property invariants—because it computes a fresh value, allocates a new object, performs expensive work, or triggers side effects—the specification should use a method instead of an attribute. This preserves developers' mental model that reading a property is safe, fast, and idempotent.

## Fit for Coding Agents

This principle aligns strongly with the statistical priors and code-generation patterns of LLM coding agents. Across billions of lines of JavaScript and TypeScript training data, `obj.prop` is overwhelmingly a cheap, side-effect-free, referentially stable read. Consequently, coding agents routinely generate code transformations that assume data-property invariants without consulting WebIDL specifications to check whether a getter secretly allocates a new object, triggers side effects, or performs expensive synchronous work.

When an API violates this principle, the resulting failure modes are particularly damaging for agents because they are almost always silent rather than throwing loud exceptions in the feedback loop. First, in reactive frameworks like React, Vue, and Solid, agents routinely pass property accesses into dependency arrays (`useEffect(() => ..., [obj.attribute])`) or memoized props; if a getter allocates a new object on each read (`obj.attribute !== obj.attribute`), `Object.is` checks fail on every render and cause infinite render loops without a clear stack trace. Second, when an attribute returns an object, agents frequently write nested mutations like `obj.attribute.foo = bar`; if the getter returns a fresh copy on each access, the mutation is silently discarded without throwing an error.

Third, agents debugging failing tests frequently inject `console.log(obj.attribute)` or repeat `obj.attribute` across conditions and loop bodies. If a getter has observable side effects, adding logging mutates program behavior; if a getter performs expensive synchronous work—such as legacy DOM layout attributes like `element.offsetWidth` and `element.offsetHeight` forcing synchronous reflow—agents read them inside loops and cause severe layout thrashing. Exposing non-trivial operations as methods (`obj.getSnapshot()`) instead of attributes gives the LLM a clear syntactic signal (`()`) in token space to cache the result in a `const` variable and invoke it deliberately.

## Value as a Slide Example

§6.2 is a strong, concrete slide example (`4/5`) of a classic human API ergonomics rule that becomes even more critical for coding agents because violations trigger silent runtime bugs rather than loud exceptions. It cleanly demonstrates how syntactic honesty (`obj.prop` vs. `obj.getProp()`) shapes LLM token predictions and prevents subtle agent failure modes.

On a slide, it can be illustrated with three immediately recognizable one-line agent traps when getters don't act like data properties: (1) `useEffect(..., [obj.attr])` triggering infinite React re-render loops when `obj.attr !== obj.attr`, (2) `obj.attr.enabled = true` silently evaporating when `obj.attr` returns a newly synthesized object on every read, and (3) legacy layout-inducing attributes like `el.offsetHeight` looking like cheap `O(1)` property reads and tricking agents into causing synchronous layout thrashing inside loops.
