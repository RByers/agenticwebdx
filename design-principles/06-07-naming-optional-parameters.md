---
section: "6.7"
id: "naming-optional-parameters"
title: "Name optional arguments appropriately"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#naming-optional-parameters"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Positive, opt-in names for optional boolean arguments (like once: true instead of noRepeat: true) help coding agents avoid double-negation polarity bugs and preserve falsy-default invariants when forwarding options, provided the positive name remains concrete rather than opaque jargon."
---

# §6.7 Name optional arguments appropriately

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §6.7 naming-optional-parameters — Name optional arguments appropriately: Positive, opt-in names for optional boolean arguments (like once: true instead of noRepeat: true) help coding agents avoid double-negation polarity bugs and preserve falsy-default invariants when forwarding options, provided the positive name remains concrete rather than opaque jargon.

- **URL:** https://w3ctag.github.io/design-principles/#naming-optional-parameters
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Positive, opt-in names for optional boolean arguments (like once: true instead of noRepeat: true) help coding agents avoid double-negation polarity bugs and preserve falsy-default invariants when forwarding options, provided the positive name remains concrete rather than opaque jargon.

## Principle Summary

W3C TAG Design Principle §6.7 ("Name optional arguments appropriately") states that optional parameters—whether positional or in an options dictionary—should be named so that their default behavior is obvious without using negative names. Because omitted optional booleans in JavaScript evaluate to `undefined` (falsy), optional boolean flags should default to `false`. Rather than naming an option `repeat` (which would require a `true` default) or `noRepeat` (which introduces a negative name), API designers should choose a positive word for the non-default behavior, such as `once` in `addEventListener(type, listener, { once: true })`, `passive` instead of `active`, `isolate` instead of `connect`, or `private` instead of `public`.

For human developers and browser engines, this keeps JavaScript's falsy semantics consistent (`undefined` and `false` produce the same default behavior) while preventing confusing double negatives like `{ noRepeat: false }` at call sites.

## Fit for Coding Agents

This principle is a good fit for AI coding agents and directly mitigates two frequent classes of LLM code-generation bugs: boolean polarity inversion and wrapper prop-forwarding errors. Transformer-based coding models are measurably more error-prone when reasoning over negated identifiers (`noRepeat`, `disableCache`, `ignoreCase`) and double negations (`{ noRepeat: false }`). When an API uses a negated flag name, agents are much more likely to flip the boolean value during generation or misinterpret existing call sites during refactoring. Naming the option positively for the opt-in behavior (`{ once: true }`) aligns with strong statistical priors across JavaScript/TypeScript training data, where setting a flag to `true` activates a specific feature and omitting it preserves default behavior.

Positive opt-in naming that preserves a `false` default also helps agents generate clean, bug-free wrapper components and helper functions. Agents routinely write pass-through code that forwards optional configuration properties (e.g., `el.addEventListener('click', handler, { once: props.once })`). Because `once` defaults to `false`, passing `undefined` or `false` through a wrapper seamlessly preserves the default behavior without requiring verbose conditional object-spreading boilerplate. If the option were instead named `repeat` (requiring a `true` default), an agent passing a coerced boolean or uninitialized state variable would silently invert the default behavior.

One important nuance for standards authors is that avoiding a negative name (`no*`) should not come at the expense of mechanical explicitness. While `{ once: true }` is immediately self-describing in token context, another example cited by the principle—`{ passive: true }` on `addEventListener()`—uses a positive adjective that obscures its actual operational constraint (that the listener will never call `event.preventDefault()`). Because violating `passive: true` only emits a console warning rather than throwing an exception, agents sometimes combine `passive: true` with `preventDefault()` and miss the silent failure. Thus, agents benefit most when positive optional parameter names describe the concrete mechanism rather than an abstract mode.

## Value as a Slide Example

This principle is a solid supporting example (`clearly-useful`, strength `3/5`) for a TPAC slide deck, particularly when grouped with boolean defaults (§6.6) and dictionary arguments. It demonstrates how a classic human ergonomics rule—avoiding negative boolean names like `noRepeat` so defaults remain `false` without double negatives—directly helps LLMs avoid polarity-inversion bugs and makes prop-forwarding in agent-generated wrapper code safe.

The most compelling slide angle comes from contrasting two of §6.7's own built-in examples: `once: true` vs. `passive: true` in `addEventListener(type, listener, options)`. Both satisfy the principle by using positive words with a `false` default, yet `once: true` clearly communicates its exact runtime behavior, whereas `passive: true` hides the "cannot call `preventDefault()`" contract behind domain jargon and a silent console warning. This gives standards authors a memorable takeaway: positive opt-in names help agents, but only when the positive name is mechanically explicit rather than euphemistic.
