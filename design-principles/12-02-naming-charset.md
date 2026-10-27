---
section: "12.2"
id: "naming-charset"
title: "Use ASCII names"
chapter: "12. Naming principles"
url: "https://w3ctag.github.io/design-principles/#naming-charset"
agent_fit: "good"
slide_example: "neither"
example_strength: 1
verdict: "Baseline hygiene that also benefits coding agents by avoiding escaping footguns, Unicode homoglyph confusion, and multi-byte tokenizer overhead, though too trivial and uncontested to feature on a TPAC slide."
---

# §12.2 Use ASCII names

GREP_SUMMARY: slide_example=neither | strength=1/5 | agent_fit=good | §12.2 naming-charset — Use ASCII names: Baseline hygiene that also benefits coding agents by avoiding escaping footguns, Unicode homoglyph confusion, and multi-byte tokenizer overhead, though too trivial and uncontested to feature on a TPAC slide.

- **URL:** https://w3ctag.github.io/design-principles/#naming-charset
- **Chapter:** 12. Naming principles
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 1/5
- **Verdict:** Baseline hygiene that also benefits coding agents by avoiding escaping footguns, Unicode homoglyph confusion, and multi-byte tokenizer overhead, though too trivial and uncontested to feature on a TPAC slide.

## Principle Summary

W3C TAG Design Principle §12.2 ("Use ASCII names") states that names on the web platform must adhere to the local language restrictions—such as CSS identifier rules or JavaScript identifier syntax—and should remain within the ASCII character range.

For human developers and browser engines, this principle exists as basic platform hygiene: it ensures that platform names can be typed on any keyboard without special input methods, avoids character encoding and Unicode normalization (NFC vs. NFD) bugs, prevents visual spoofing via Unicode homoglyphs, and allows identifiers to be written directly without escape sequences like `CSS.escape()` or bracket notation.

## Fit for Coding Agents

This principle aligns well with the mechanics of LLM coding agents, even though one of its original human motivations—physical keyboard ergonomics—does not apply to models generating tokens directly. While an LLM does not use a physical keyboard and can emit arbitrary Unicode code points in a single forward pass, non-ASCII identifiers and names that violate host-language identifier syntax introduce distinct failure modes for agents.

First, requiring names to obey local language identifier rules (such as valid CSS `<ident-token>` or JavaScript `IdentifierName` syntax) prevents escaping and syntax footguns. When names contain characters that require context-specific escaping (such as colons, slashes, leading digits, or special punctuation in CSS selectors or JS property access), LLMs frequently miscount backslashes—especially when generating code inside JSON tool-call arguments, template literals, or nested strings (`\\` vs. `\\\\`).

Second, LLMs are prone to conflating visually or semantically similar Unicode characters from natural-language training text, such as substituting U+2013 (en-dash) or U+2212 (minus sign) for ASCII U+002D (`-`), curly quotes for straight quotes, or non-breaking spaces for standard spaces. Keeping platform identifiers strictly in ASCII makes any accidental non-ASCII substitution immediately detectable by parsers and linters. Finally, Byte-Pair Encoding (BPE) tokenizers are heavily optimized around ASCII English words and identifier subwords, compressing them into compact tokens with strong training priors rather than fragmenting into multi-byte token sequences.

## Value as a Slide Example

This principle is not useful on a TPAC slide (`neither`, strength 1/5). Although ASCII naming and adhering to host-language identifier syntax technically benefit coding agents, no one in web standards is seriously proposing non-ASCII Web IDL methods, CSS properties, or HTML attributes, nor does the rise of AI coding agents create any tension around this baseline hygiene rule. Featuring it on a slide would feel trivial and distract from principles where human DX and agentic DX meaningfully reinforce or conflict with each other.
