---
section: "3.1"
id: "attribute-reuse"
title: "Re-use HTML attribute names (only) for similar functionality"
chapter: "3. HTML"
url: "https://w3ctag.github.io/design-principles/#attribute-reuse"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Reusing attribute names with identical syntax for similar functionality aligns directly with LLM token priors for zero-shot cross-element transfer, while avoiding homonymous overloading prevents syntax bleed and silent HTML parser fallbacks."
---

# §3.1 Re-use HTML attribute names (only) for similar functionality

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §3.1 attribute-reuse — Re-use HTML attribute names (only) for similar functionality: Reusing attribute names with identical syntax for similar functionality aligns directly with LLM token priors for zero-shot cross-element transfer, while avoiding homonymous overloading prevents syntax bleed and silent HTML parser fallbacks.

- **URL:** https://w3ctag.github.io/design-principles/#attribute-reuse
- **Chapter:** 3. HTML
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Reusing attribute names with identical syntax for similar functionality aligns directly with LLM token priors for zero-shot cross-element transfer, while avoiding homonymous overloading prevents syntax bleed and silent HTML parser fallbacks.

## Principle Summary

This principle directs specification authors designing a new HTML attribute to check whether another HTML element already uses an attribute name for similar functionality, and if so, to reuse that name while keeping its syntax as close as possible to the existing attribute. Conversely, it warns against reusing an existing attribute name when the new functionality is not genuinely similar.

For human developers, this keeps HTML's vocabulary compact, allows authors to transfer existing mental models across elements without consulting documentation for every tag, and avoids the confusion that arises when the same attribute name means completely different things or requires different microsyntaxes depending on which element it decorates.

## Fit for Coding Agents

This principle is a strong positive fit (`good`) for AI coding agents because it maps directly onto how statistical language models represent, generalize, and sample tokens across markup contexts. In a transformer model, an attribute name token (such as `disabled`, `loading`, `fetchpriority`, `crossorigin`, or `readonly`) carries dense semantic and syntactic priors aggregated across every element where it appears in pre-training data. When a new or less-frequent HTML element reuses an established attribute name with identical syntax and behavior—such as `loading="lazy"` on both `<img>` and `<iframe>`, or `fetchpriority="high"` across `<img>`, `<script>`, and `<link>`—coding agents achieve high zero-shot and few-shot accuracy even when the new element–attribute pairing is sparse in their training corpus.

Conversely, when the platform violates the first half of this principle by inventing different attribute names for parallel concepts across elements (such as historically split resource attributes like `<link href>`, `<script src>`, and `<object data>`, or when an expected shared attribute like `loading="lazy"` is supported on `<img>` and `<iframe>` but not `<video>`), LLMs routinely hallucinate the dominant attribute onto the element that lacks it. Because HTML's parsing rules silently ignore unrecognized attributes rather than throwing a runtime or build-time error, these hallucinations fail silently in the agent's execution loop—leaving a broken or unoptimized page with no console diagnostic to trigger self-correction.

The inverse rule—not reusing an existing attribute name for divergent functionality or with incompatible syntax—is equally critical for agents. LLMs are highly susceptible to semantic and syntactic bleed when a single token is overloaded across contexts. For example, historical overloading of `type` across `<input type="text">`, `<button type="submit|button">`, `<script type="module">`, and `<ol type="a">`, or subtle differences in how `value` behaves on `<input>`, `<button>`, `<option>`, and `<li>`, forces the model to rely purely on local attention to disambiguate microsyntaxes. When a rarely used element overloads a high-frequency attribute name with a different syntax, the model's strong prior from the dominant element pulls generation toward the wrong value format.

## Value as a Slide Example

This principle is a strong (`4/5`), relatable `clearly-useful` slide example for TPAC because it translates a familiar HTML design rule into concrete LLM mechanics: shared token priors combined with HTML's silent failure on unknown attributes. Standards participants immediately grasp the contrast between positive reuse (`loading="lazy"`, `fetchpriority`, `disabled`, `crossorigin`) and historical inconsistencies (`href` vs. `src` vs. `data`, or `type` overloading).

On a slide about which existing TAG principles already serve coding agents well, `attribute-reuse` provides a punchy, memorable takeaway: when HTML reuses attribute names and microsyntaxes consistently across elements, LLMs get "free" cross-element generalization on newly standardized features; when HTML invents synonyms or overloads attribute names with divergent syntax, agents hallucinate attributes across elements and HTML silently swallows the mistake without an error in the feedback loop.
