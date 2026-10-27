---
section: "12.3"
id: "naming-consultation"
title: "Consult others on naming"
chapter: "12. Naming principles"
url: "https://w3ctag.github.io/design-principles/#naming-consultation"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 4
verdict: "Aligning Web API names with popular libraries, other programming languages, adjacent specs, and developer vocabulary directly leverages LLM training priors and enables zero-shot accuracy even for newly shipped APIs."
---

# §12.3 Consult others on naming

GREP_SUMMARY: slide_example=clearly-useful | strength=4/5 | agent_fit=good | §12.3 naming-consultation — Consult others on naming: Aligning Web API names with popular libraries, other programming languages, adjacent specs, and developer vocabulary directly leverages LLM training priors and enables zero-shot accuracy even for newly shipped APIs.

- **URL:** https://w3ctag.github.io/design-principles/#naming-consultation
- **Chapter:** 12. Naming principles
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 4/5
- **Verdict:** Aligning Web API names with popular libraries, other programming languages, adjacent specs, and developer vocabulary directly leverages LLM training priors and enables zero-shot accuracy even for newly shipped APIs.

## Principle Summary

W3C TAG Design Principle §12.3 ("Consult others on naming") advises specification authors to look outside their immediate working group when choosing names for new Web APIs. Specifically, it recommends four sources of input: examining what similar APIs are named on other platforms or in popular libraries across programming languages; asking developers and end users what they naturally call the concepts being manipulated; reviewing related web platform specifications and consulting adjacent domain experts; and verifying that names are inclusive. It cites Tantek Çelik's cross-implementation research on URL component names—which informed the WHATWG URL standard—as a model of evidence-based naming.

For human developers, this principle exists to prevent "committee-speak" and insular jargon. When a web standard adopts terminology that already matches userland libraries, other major languages, and everyday developer vocabulary, humans can transfer their existing mental models without having to memorize arbitrary new names for familiar concepts.

## Fit for Coding Agents

This principle is a strong, direct fit (`good`) for AI coding agents because an LLM's weights are literally a statistical compression of the exact sources §12.3 tells spec authors to consult: cross-language standard libraries (Python, Rust, Go, Java, POSIX), popular userland packages (Lodash, RxJS, Node.js, React), existing Web specifications, and natural-language developer prose. Because LLMs map user intent in natural-language prompts onto code tokens via shared semantic embeddings, matching the names developers use in conversation and across ecosystems dramatically lowers hallucination risk.

Crucially, consulting existing libraries and languages solves one of the hardest problems in agentic web DX: the training-data cutoff and low-resource lag for new Web APIs. When a brand-new browser API ships, it has near-zero representation in pre-training corpora compared to years of legacy patterns. However, if its surface matches established cross-platform or library conventions—such as `Set.prototype.intersection()` / `difference()` (matching Python and math vocabulary), `Object.groupBy()` (matching Lodash and SQL), or `URLPattern` (matching `path-to-regexp` and routing libraries)—an agent needs only a minimal hint in system instructions or TypeScript definitions (and sometimes zero-shot intuition alone) to generate the exact method and property names without hallucinating argument shapes or non-existent helper methods. Conversely, when a spec invents a bespoke name that diverges from popular libraries, agents repeatedly hallucinate the library method name on the native object.

Furthermore, this principle takes on a new, actionable dimension in the era of coding agents: LLMs themselves are now an empirical consultation tool for spec authors. Because a frontier model aggregates naming conventions across millions of repositories and languages, spec editors can prompt models with a problem description and inspect the top-k method, property, and parameter names the model predicts before a spec is finalized. If multiple models independently reach for the same method name when asked to use a hypothetical native API, adopting that name guarantees immediate alignment with agent priors.

## Value as a Slide Example

This principle is a strong (`4/5`) `clearly-useful` slide candidate, particularly for the second half of the TPAC question: "[How] should web standards adapt?". While sibling principles like §12.2 ("Consistency") address the technical artifact, §12.3 addresses the standards process and offers a concrete, constructive takeaway for W3C working groups.

On a slide, §12.3 illustrates two compelling points: (1) Why cross-ecosystem naming matters more than ever: paving the cowpaths of popular libraries and other languages (`Object.groupBy`, `Set.prototype.intersection`, `AbortSignal.timeout`, URL component naming) doesn't just save humans from reading MDN—it transfers billions of tokens of cross-language and npm training data directly to brand-new Web APIs, making them usable by coding agents on day one; and (2) A new way to apply §12.3 ("Consult the model"): alongside surveying human developers and other specs, W3C editors can empirically test API naming by prompting coding agents with a problem statement and observing what API names and signatures they naturally guess from cross-platform priors.
