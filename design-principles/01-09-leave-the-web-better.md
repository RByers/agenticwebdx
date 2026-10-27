---
section: "1.9"
id: "leave-the-web-better"
title: "Leave the web better than you found it"
chapter: "1. Principles behind design of Web APIs"
url: "https://w3ctag.github.io/design-principles/#leave-the-web-better"
agent_fit: "poor"
slide_example: "clearly-harmful"
example_strength: 5
verdict: "Eliminating legacy footguns and silent defects helps agents avoid reproducing bugs, but breaking consistency with adjacent legacy APIs or refusing small extensions to ubiquitous APIs clashes with LLM training priors and pattern generalization."
---

# §1.9 Leave the web better than you found it

GREP_SUMMARY: slide_example=clearly-harmful | strength=5/5 | agent_fit=poor | §1.9 leave-the-web-better — Leave the web better than you found it: Eliminating legacy footguns and silent defects helps agents avoid reproducing bugs, but breaking consistency with adjacent legacy APIs or refusing small extensions to ubiquitous APIs clashes with LLM training priors and pattern generalization.

- **URL:** https://w3ctag.github.io/design-principles/#leave-the-web-better
- **Chapter:** 1. Principles behind design of Web APIs
- **Agent-Fit:** poor
- **Slide-Example:** clearly-harmful
- **Example-Strength:** 5/5
- **Verdict:** Eliminating legacy footguns and silent defects helps agents avoid reproducing bugs, but breaking consistency with adjacent legacy APIs or refusing small extensions to ubiquitous APIs clashes with LLM training priors and pattern generalization.

## Principle Summary

W3C TAG Design Principle §1.9 ("Leave the web better than you found it") instructs specification authors that new web capabilities must improve the overall quality of the platform rather than propagating existing flaws. Specifically, the existence of a defect in one part of the platform must not be used as a precedent to excuse adding or extending that defect elsewhere, and "consistency with existing problematic design patterns" is explicitly rejected as a justification for repeating those patterns in new Web APIs. Furthermore, when extending an existing feature that has known flaws, spec authors are expected to make some attempt to mitigate those defects so that increased usage does not amplify the harm.

For human developers and browser engines, this principle acts as a circuit breaker against compounding technical debt. Because the web cannot easily remove legacy APIs (`document.cookie`, `Date`, `localStorage`, synchronous DOM queries, or live `HTMLCollection`s), allowing new features to copy their flawed semantics for the sake of local consistency would permanently lock the platform into its worst historical mistakes and make independent evolution impossible.

## Fit for Coding Agents

This principle has a mixed fit for AI coding agents because it sits right at the fault line between two competing agent needs: eliminating silent platform footguns versus preserving statistical predictability and local consistency.

On the positive side, legacy web platform defects are major traps for LLMs. Because coding agents learn by imitating statistical patterns in training corpora, they readily reproduce historical footguns—such as string-concatenation parsing bugs in `document.cookie`, mutability and zero-indexed month errors in `Date`, main-thread blocking in `localStorage`, or unexpected mutation during iteration over live `HTMLCollection`s. When spec authors follow §1.9 by refusing to propagate those defective patterns into new APIs—instead designing cleaner, structured, invariant-preserving replacements like `CookieStore`, `Temporal`, or static `NodeList` returns from `querySelectorAll`—they reduce the surface area of silent bugs and give agents safer primitives with louder failure modes.

On the negative side, the principle's core prescription—"Consistency with existing problematic design patterns is not a good reason to propagate those patterns" and partially addressing flaws when extending an existing feature—often pulls against how LLMs generalize. First, LLMs rely heavily on local symmetry across an interface or domain; when a new extension or sibling API breaks consistency with an existing "problematic" pattern on the same object or subsystem (e.g., mixing live `HTMLCollection` getters with static `NodeList` getters, or giving new methods on a legacy interface Promise/strict semantics while sibling methods use callbacks/silent coercion), agents frequently hallucinate the legacy behavior onto the new extension or vice versa. Second, when standards bodies refuse to add a small, pragmatic extension to a defective legacy API and instead require switching to a clean-sheet replacement (`IndexedDB` over `localStorage`, or `Temporal` over `Date`), coding agents remain anchored to the billions of lines of legacy code in their pre-training weights and often continue emitting the legacy API with brittle userland glue code to work around the missing extension.

## Value as a Slide Example

This principle is neither a strong `clearly-useful` nor `clearly-harmful` headline example for a TPAC slide (2/5 strength). At its core, §1.9 is a high-level meta-principle about long-term platform stewardship and avoiding the propagation of security, privacy, or architectural defects. Arguing on a slide that web standards should stop leaving the web better—and instead propagate known defects just to match LLM training priors—would be unpersuasive to standards engineers, especially when the defects involve end-user security, privacy, or main-thread responsiveness.

At the same time, it is not a clean `clearly-useful` slide example because its most concrete rule of thumb—sacrificing consistency with existing patterns to fix design flaws—creates real friction for LLM pattern matching when applied incrementally inside existing APIs. That specific tradeoff (fixing legacy warts vs. maintaining predictable consistency and respecting training-data inertia) is much better illustrated on slides via more concrete API design principles or specific case studies like `Date` vs. `Temporal` and live `HTMLCollection` vs. static `NodeList`, rather than through this broad stewardship principle.
