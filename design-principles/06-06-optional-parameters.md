---
section: "6.6"
id: "optional-parameters"
title: "Make method arguments optional if possible"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#optional-parameters"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Aligning optional defaults with the common case and enforcing `false` as the default for booleans matches LLM statistical priors, prevents polarity inversions in wrapper code, and eliminates error-prone positional filler tokens."
---

# §6.6 Make method arguments optional if possible

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §6.6 optional-parameters — Make method arguments optional if possible: Aligning optional defaults with the common case and enforcing `false` as the default for booleans matches LLM statistical priors, prevents polarity inversions in wrapper code, and eliminates error-prone positional filler tokens.

- **URL:** https://w3ctag.github.io/design-principles/#optional-parameters
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Aligning optional defaults with the common case and enforcing `false` as the default for booleans matches LLM statistical priors, prevents polarity inversions in wrapper code, and eliminates error-prone positional filler tokens.

## Principle Summary

W3C TAG Design Principle §6.6 states that whenever a method argument has a reasonable default value, the specification should mark that parameter as optional and define the default value explicitly. That default should match what most authors want in the common case. Furthermore, for boolean arguments and attributes, a default value of `false` is strongly preferred—meaning API designers should name parameters or attributes so that `false` (omitting the argument or attribute) represents the common, standard behavior and `true` opts into the specialized mode.

This principle exists to keep common API calls concise, prevent authors from having to pass meaningless placeholder values (such as `, false` or `, undefined`) on every invocation, and maintain consistency with JavaScript's truthiness model and HTML's boolean attribute semantics (where the absence of an attribute means `false` and its presence means `true`). It also avoids historical web platform footguns like `XMLHttpRequest.prototype.open(method, url, async = true)` or `Element.prototype.scrollIntoView(alignToTop = true)`, where a `true` default contradicts JavaScript's `Boolean(undefined) === false` coercion rule.

## Fit for Coding Agents

This principle is a good fit (`agent_fit: good`) for AI coding agents for three interconnected reasons: statistical priors around the common case, wrapper forwarding safety with `false` defaults, and reduced positional token overhead.

First, LLMs are fundamentally statistical models that strongly gravitate toward minimal, canonical call patterns when generating standard operations. If an API requires an argument despite having an obvious default—or if the default does not match what most authors intend (for example, `node.cloneNode()` defaulting to `deep = false` when callers frequently expect a full copy, or older DOM methods that threw a `TypeError` when trailing arguments were omitted)—agents either omit the parameter and hit runtime argument-count exceptions, or must emit boilerplate positional arguments that increase the chance of argument-order hallucinations. Making the statistical majority choice the default ensures that the simplest call an agent writes works as intended out of the box.

Second, the rule that boolean defaults must be `false` (and named accordingly) is particularly helpful for coding agents. Agents frequently generate helper functions, UI component wrappers, or TypeScript adapters that forward configuration flags downward (e.g., `apiCall(data, { disableCache: props.disableCache })` or `Boolean(options?.flag)`). In JavaScript, an omitted property or uninitialized variable evaluates to `undefined`, which is falsy. When an API violates §6.6 and defaults a boolean parameter to `true`, agents frequently introduce subtle polarity bugs—either assuming that omitting or passing a falsy expression keeps the default behavior, or getting confused by double-negatives when translating user intent. Naming boolean parameters and attributes so that `false`/`undefined` is the default preserves a uniform invariant across HTML attributes, JS conditionals, and Web IDL defaults.

## Value as a Slide Example

This principle is a `clearly-useful` example with moderate-to-good slide strength (`3/5`). It illustrates a concrete way that good human ergonomics and LLM ergonomics converge: when defaults match the 90% use case and boolean defaults are always `false`, both humans and agents write fewer tokens and make fewer logic-inversion errors.

On a TPAC slide, however, §6.6 works best as a supporting point alongside §6.5 (Accept optional and/or primitive arguments through dictionaries) and §6.7 (Name optional arguments appropriately) rather than as a standalone headline slide. While the "boolean defaults must be `false`" rule provides a crisp, memorable talking point (contrasting `XMLHttpRequest.open(method, url, async = true)` or `Element.scrollIntoView(alignToTop = true)` with modern options dictionaries), the broader advice to "make arguments optional" is familiar API design wisdom that is most impactful for agents when paired with named dictionary parameters.
