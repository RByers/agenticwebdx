---
section: "12.5"
id: "naming-consistency"
title: "Name things consistently"
chapter: "12. Naming principles"
url: "https://w3ctag.github.io/design-principles/#naming-consistency"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Grammatical and negation consistency across related API sets directly aligns with LLM pattern completion, reducing hallucinated member names and silent boolean-polarity inversions."
---

# §12.5 Name things consistently

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §12.5 naming-consistency — Name things consistently: Grammatical and negation consistency across related API sets directly aligns with LLM pattern completion, reducing hallucinated member names and silent boolean-polarity inversions.

- **URL:** https://w3ctag.github.io/design-principles/#naming-consistency
- **Chapter:** 12. Naming principles
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Grammatical and negation consistency across related API sets directly aligns with LLM pattern completion, reducing hallucinated member names and silent boolean-polarity inversions.

## Principle Summary

W3C TAG Design Principle §12.5 ("Name things consistently") states that sets of related names—such as properties on a configuration dictionary, methods on an interface, enum values, or HTML attributes—should agree with one another in part of speech (e.g., all nouns, all verbs, or all adjectives) and in negation/polarity (either all names in the set describe what is allowed/enabled, or all describe what is denied/disabled).

For human developers, this consistency reduces cognitive load and documentation lookups by allowing developers who know one member of a set (e.g., `allowScripts`) to accurately infer sibling names (`allowForms`, `allowPopups`) without guessing whether another member switched part of speech (`popupsAllowed`) or flipped polarity (`noModals`), while also avoiding confusing double negatives (`!options.disableCache`) in application code.

## Fit for Coding Agents

This principle is a strong positive fit (`good`) for AI coding agents because it directly reinforces how large language models predict tokens and reason about boolean state. Autoregressive coding models rely heavily on structural and grammatical symmetry both in their training priors and within the active context window. When an agent sees one or two related properties in context (for example, configuring options in a dictionary or reading attributes on an element), it predicts sibling members by extrapolating the grammatical template. If a set of related API names mixes parts of speech—such as pairing a modal verb (`canEdit`), a past participle (`disabled`), and a noun (`readOnlyMode`)—agents frequently hallucinate non-existent sibling properties that follow the dominant pattern (`canRead`, `editable`) rather than recalling the irregular spec name.

Consistent negation (boolean polarity) is arguably even more important for coding agents than for humans because it prevents silent logic inversions. When an API mixes positive and negative flags in the same set (such as combining `allow*` or `enable*` options with `no*`, `disable*`, or `prevent*` options), LLMs frequently commit polarity errors—passing `true` where `false` was intended or writing inverted double-negative conditions. Worse, boolean configuration mistakes in web APIs (such as permission policies, caching flags, or event listener options) almost never throw runtime exceptions or type errors; they fail silently by enabling or disabling the wrong behavior, depriving the agent's test/execution feedback loop of a loud signal to self-correct.

## Value as a Slide Example

This principle is `clearly-useful` with an example strength of 3/5. It is a solid supporting illustration of how classic human API ergonomics ("keep part of speech and negation uniform across related sets") map directly onto LLM mechanics (in-context pattern completion and avoiding silent boolean-polarity bugs), though as a brief two-bullet naming guideline it works best grouped with broader naming/predictability principles rather than as a standalone headline slide.

Concrete Web platform examples that bring this principle to life on a slide include HTML's mixed attribute polarity—where positive capability attributes (`controls`, `autoplay`, `contenteditable="true"`, `draggable="true"`, `spellcheck="true"`) coexist with negative/disabling boolean attributes (`disabled`, `readonly`, `hidden`, `inert`, `novalidate`, `nomodule`), regularly prompting agents to emit broken markup like `disabled="false"`—as well as `AddEventListenerOptions` (`{ capture, once, passive }`), where `passive: true` acts as a disguised negative constraint ("will not call `preventDefault()`") that agents frequently misapply.
