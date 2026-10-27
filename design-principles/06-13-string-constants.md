---
section: "6.13"
id: "string-constants"
title: "Use strings for constants and enums"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#string-constants"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "String enums and dictionary objects strongly benefit coding agents by making runtime logs self-describing, aligning with natural-language token priors, enabling strict TypeScript literal unions and loud WebIDL runtime TypeErrors, and eliminating error-prone bitwise arithmetic."
---

# §6.13 Use strings for constants and enums

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §6.13 string-constants — Use strings for constants and enums: String enums and dictionary objects strongly benefit coding agents by making runtime logs self-describing, aligning with natural-language token priors, enabling strict TypeScript literal unions and loud WebIDL runtime TypeErrors, and eliminating error-prone bitwise arithmetic.

- **URL:** https://w3ctag.github.io/design-principles/#string-constants
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** String enums and dictionary objects strongly benefit coding agents by making runtime logs self-describing, aligning with natural-language token priors, enabling strict TypeScript literal unions and loud WebIDL runtime TypeErrors, and eliminating error-prone bitwise arithmetic.

## Principle Summary

W3C TAG Design Principle §6.13 directs spec authors to represent constants and enumerated values as strings (via WebIDL enums) rather than integers, and to represent combined states using dictionary objects rather than integer bitmasks.

The principle exists to move the web platform away from legacy C/Java-style integer constants (such as Node.ELEMENT_NODE === 1, XMLHttpRequest.DONE === 4, or WebGL's numeric gl.* constants) and bitmasks (such as Node.compareDocumentPosition() or NodeFilter.SHOW_*). Because JavaScript engines optimize and intern strings, integer constants provide no performance benefit while making both source code and logged runtime values harder for developers to read and inspect.

## Fit for Coding Agents

This principle is a strong fit for AI coding agents and arguably benefits LLMs even more than human developers across both code generation and agentic debugging loops. First, coding agents depend heavily on serialized runtime output—console logs, test assertion diffs, DOM snapshots, and DevTools/Playwright inspection—to verify and repair code. When an API returns a string like "granted", "visible", or a dictionary like { readable: true, writable: false }, the value is immediately self-explanatory in the LLM's natural-language token stream. By contrast, when a legacy API logs readyState: 4, nodeType: 3, a WebGL enum like 3553, or a compareDocumentPosition bitmask of 20, the raw integer carries zero semantic meaning without cross-referencing the specific interface's constant table, and decomposing an integer bitmask like 20 (4 | 16) in a test failure requires binary arithmetic that token-predicting LLMs notoriously struggle with.

Second, replacing bitmasks with dictionary objects eliminates one of the most frequent sources of subtle bugs in LLM-generated JavaScript. When writing bitwise expressions for APIs like Node.compareDocumentPosition() or MouseEvent.buttons, agents routinely fall into JavaScript's operator-precedence trap—writing mask & FLAG === 0, which evaluates as mask & (FLAG === 0) because === binds tighter than &—or confuse bit positions (such as MouseEvent.button using 0/1/2 vs. MouseEvent.buttons using 1/2/4) or hallucinate which interface holds a constant (e.g., Node.SHOW_ELEMENT instead of NodeFilter.SHOW_ELEMENT). Using a dictionary object with named boolean properties removes bitwise arithmetic and constant-namespace lookup errors altogether.

Third, WebIDL string enums and dictionaries provide loud, actionable feedback in both static type-checking and runtime execution. In TypeScript's lib.dom.d.ts, WebIDL enums compile to string literal union types (e.g., "include" | "omit" | "same-origin"), so an agent passing a hallucinated string receives an immediate compiler error listing the exact valid literals, and at runtime WebIDL enum conversion throws a loud TypeError. Passing an invalid integer or unintended bit combination to a numeric API, by contrast, often fails silently or masks unrelated bits.

## Value as a Slide Example

§6.13 is a strong (4/5), concrete "clearly-useful" slide example for TPAC because it offers a crisp side-by-side comparison from web platform history showing how semantic self-description helps language models even more than humans. A slide can directly contrast legacy numeric constants and bitmasks—such as `a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING === 0` (which contains a classic JS operator-precedence bug and logs an opaque integer like `20` on failure) or WebGL's numeric `gl.TRIANGLES` (`4`)—against modern string enums and dictionaries in `fetch(url, { credentials: 'include', mode: 'cors' })` or WebGPU's `{ topology: 'triangle-list', cullMode: 'back' }`.

For spec authors, this grounds a memorable rule of thumb: LLMs are language models, not bit-shifters. Encoding API states as semantic words and named dictionary keys rather than integers and bitmasks directly leverages token priors, makes runtime state self-describing in agent feedback loops, and converts silent bitwise bugs into loud compile-time and runtime errors.
