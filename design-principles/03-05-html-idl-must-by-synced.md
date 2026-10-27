---
section: "3.5"
id: "html-idl-must-by-synced"
title: "Keep attributes in sync"
chapter: "3. HTML"
url: "https://w3ctag.github.io/design-principles/#html-idl-must-by-synced"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 5
verdict: "1:1 name and state synchronization between HTML content attributes and JS IDL properties eliminates silent expando-property bugs, framework binding mismatches, and stale DOM snapshot reads in agent loops."
---

# §3.5 Keep attributes in sync

GREP_SUMMARY: slide_example=clearly-useful | strength=5/5 | agent_fit=good | §3.5 html-idl-must-by-synced — Keep attributes in sync: 1:1 name and state synchronization between HTML content attributes and JS IDL properties eliminates silent expando-property bugs, framework binding mismatches, and stale DOM snapshot reads in agent loops.

- **URL:** https://w3ctag.github.io/design-principles/#html-idl-must-by-synced
- **Chapter:** 3. HTML
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 5/5
- **Verdict:** 1:1 name and state synchronization between HTML content attributes and JS IDL properties eliminates silent expando-property bugs, framework binding mismatches, and stale DOM snapshot reads in agent loops.

## Principle Summary

This principle states that every new HTML content attribute (set in markup or via `setAttribute()`) should have a corresponding JavaScript IDL property on the DOM element with the same name, and that the state between the two must stay synchronized via attribute reflection. It explicitly warns against carving out synchronized IDL attributes with divergent names.

Historically, the web platform accumulated painful discrepancies between HTML attributes and DOM properties—both in naming (`class` vs. `className`, `for` vs. `htmlFor`, `colspan` vs. `colSpan`) and in state synchronization (such as `<input value="...">`, where the content attribute reflects `defaultValue` while the `.value` IDL property tracks the live user-edited state, or `<input checked>` vs. `.checked`). This principle exists to prevent new platform features from introducing similar mental-model splits for developers moving between declarative HTML and imperative JavaScript.

## Fit for Coding Agents

This principle is a strong positive fit (`good`) for AI coding agents because LLMs constantly translate intent across HTML markup, framework templates (JSX/TSX, Vue, Svelte, Lit), and imperative DOM scripts. When content attributes and IDL properties share identical names and synchronized state, an agent's statistical prior for the attribute name transfers directly across all representations. Conversely, when names diverge (e.g., `for` vs. `htmlFor`, `maxlength` vs. `maxLength`, or element-reference attributes like `popovertarget` vs. `popoverTargetElement`), models frequently hallucinate the wrong casing or property name when switching between HTML and JS or across frameworks that handle attribute-vs-property binding differently.

Even more critically for autonomous coding loops, violating this principle causes silent failures rather than loud errors. In JavaScript, assigning to a misspelled or non-existent IDL property on an `HTMLElement` (such as `button.popovertarget = "menu"` instead of `button.setAttribute("popovertarget", "menu")`) does not throw an exception—it silently creates an inert expando property on the JS wrapper while leaving the DOM behavior broken. Similarly, modern UI frameworks (such as React 19, Vue, and Lit) often rely on runtime `key in element` checks to decide whether to set a template binding as an IDL property or an attribute; missing or differently named IDL properties break these heuristics and force agents to generate brittle `ref` + `setAttribute` boilerplate.

Finally, state synchronization directly impacts browser-testing agents during verification. Agents inspecting live pages frequently read serialized DOM snapshots (`outerHTML`, `innerHTML`, or attribute dumps via Playwright/CDP) to verify whether an action succeeded. When IDL state is not synchronized back to the content attribute—as with `<input>` `.value` or `.checked`—the serialized HTML lies to the agent about the current UI state, causing false negatives or wasted debugging cycles during automated verification.

## Value as a Slide Example

This principle is a top-tier (`5/5`, `clearly-useful`) slide example for W3C TPAC because it connects a classic, universally understood web standards rule to two concrete agent failure modes: silent code-generation bugs and blind spots in agent DOM inspection.

On a slide, it contrasts legacy mismatches (`for`/`htmlFor`, `class`/`className`, `input.value` vs. `getAttribute('value')`, `popovertarget` vs. `popoverTargetElement`) against 1:1 reflected attributes across two agent axes: (1) Writing code, where a missing or renamed IDL property turns `el.foo = "bar"` into a silent dead expando property with no error feedback and breaks framework `key in el` binding heuristics; and (2) Reading state, where browser-using agents inspecting `outerHTML` snapshots miss live unreflected IDL state.
