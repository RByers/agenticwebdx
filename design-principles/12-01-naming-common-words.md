---
section: "12.1"
id: "naming-common-words"
title: "Use common words"
chapter: "12. Naming principles"
url: "https://w3ctag.github.io/design-principles/#naming-common-words"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 5
verdict: "Valuing full, common English words and established terms of art over arbitrary abbreviations directly helps coding agents by aligning with BPE tokenization and eliminating abbreviation-guessing hallucinations, even though agents do not share humans' non-native vocabulary limits."
---

# §12.1 Use common words

GREP_SUMMARY: slide_example=clearly-useful | strength=5/5 | agent_fit=good | §12.1 naming-common-words — Use common words: Valuing full, common English words and established terms of art over arbitrary abbreviations directly helps coding agents by aligning with BPE tokenization and eliminating abbreviation-guessing hallucinations, even though agents do not share humans' non-native vocabulary limits.

- **URL:** https://w3ctag.github.io/design-principles/#naming-common-words
- **Chapter:** 12. Naming principles
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 5/5
- **Verdict:** Valuing full, common English words and established terms of art over arbitrary abbreviations directly helps coding agents by aligning with BPE tokenization and eliminating abbreviation-guessing hallucinations, even though agents do not share humans' non-native vocabulary limits.

## Principle Summary

W3C TAG §12.1 advises that Web APIs should be named in easily readable US English using common vocabulary that most developers—particularly non-native English speakers—will understand on first encounter (for instance, preferring `setSize` over `cardinality`).

It further instructs spec authors to value readability over brevity by avoiding abbreviations unless they are universally understood (`UIEvent`) or represent established technical terms of art directly tied to what the API does or returns (such as `Body.prototype.json()` in the Fetch API).

## Fit for Coding Agents

This principle is a good fit for AI coding agents, though for reasons that differ in an instructive way from its human motivation. The human rationale begins with the observation that most web developers are not native English speakers and may be tripped up by academic vocabulary like `cardinality`. An LLM does not have a vocabulary ceiling: it understands `cardinality`, `idempotent`, or `coalesce` just as effortlessly as `setSize`. However, when generating code—especially for newer or lower-frequency APIs—common programming vocabulary (`size`, `setSize`) still benefits agents because it aligns with dominant cross-language statistical priors.

Where §12.1 shines most for coding agents is its guidance to value readability over brevity and avoid arbitrary abbreviations. A common misconception is that terse, abbreviated API names help LLMs by "saving tokens." In reality, modern subword (BPE) tokenizers encode common full words (`set`, `Size`, `Event`, `json`) as single tokens with rich semantic embeddings, whereas bespoke abbreviations (`crdnlty`, `evtMgr`, `usrIntf`) frequently split into multiple low-semantic character fragments—costing more tokens while conveying less meaning to attention heads. Furthermore, there is only one standard way to spell a full English word in US English, but many arbitrary ways to abbreviate it (`len` vs. `length`, `cfg` vs. `config`, `evt` vs. `event`, `cb` vs. `callback`). Avoiding ad-hoc abbreviations eliminates a major source of zero-shot naming hallucinations.

Finally, the principle's carve-out for well-known terms of art (`response.json()`, `UIEvent`) aligns directly with how coding agents infer types and intent in context. Naming a method `.json()` after its exact return concept creates an unmistakable statistical bridge between the user's prompt ("fetch the JSON data"), the method call (`await res.json()`), and downstream consumption without requiring redundant ceremony.

## Value as a Slide Example

This principle is a solid supporting example (3/5, `clearly-useful`) for a TPAC presentation, particularly for debunking the myth that "AI agents prefer terse or abbreviated APIs to save tokens."

On a slide, contrasting `setSize`, `response.json()`, and `UIEvent` against hypothetical abbreviated or esoteric alternatives illustrates two memorable points for spec authors: first, there is one way to spell a full word (`length`, `config`, `event`) but many ways to abbreviate it, and BPE tokenizers already compress full common words into single tokens; second, while humans need `setSize` over `cardinality` due to non-native English comprehension, agents benefit from common words and established terms of art because they maximize next-token predictability across training corpora.
