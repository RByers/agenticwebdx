---
section: "10.5"
id: "extend-manifests"
title: "Extend existing manifest files rather than creating new ones"
chapter: "10. Other API Design Considerations"
url: "https://w3ctag.github.io/design-principles/#extend-manifests"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Consolidating app metadata into existing manifests (or avoiding manifests altogether) and using single-word keys to bridge snake_case manifests and camelCase DOM APIs helps agents avoid cross-file wiring bugs and casing hallucinations, though the rule is too minor for a headline slide."
---

# §10.5 Extend existing manifest files rather than creating new ones

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §10.5 extend-manifests — Extend existing manifest files rather than creating new ones: Consolidating app metadata into existing manifests (or avoiding manifests altogether) and using single-word keys to bridge snake_case manifests and camelCase DOM APIs helps agents avoid cross-file wiring bugs and casing hallucinations, though the rule is too minor for a headline slide.

- **URL:** https://w3ctag.github.io/design-principles/#extend-manifests
- **Chapter:** 10. Other API Design Considerations
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Consolidating app metadata into existing manifests (or avoiding manifests altogether) and using single-word keys to bridge snake_case manifests and camelCase DOM APIs helps agents avoid cross-file wiring bugs and casing hallucinations, though the rule is too minor for a headline slide.

## Principle Summary

This principle advises specification authors that new web features should ideally be self-contained and self-describing without requiring a separate manifest file at all. When out-of-band metadata is genuinely needed, spec authors should extend an existing manifest format—typically the Web App Manifest (`manifest.webmanifest`) for application metadata—and reuse or extend existing keys rather than inventing a new manifest file. Creating a separate manifest is only justified when a feature has a complex, domain-specific metadata model, distinct fetch timing that cannot be reconciled, or non-browser interoperability requirements (such as Payment Method Manifest, Publication Manifest, or Origin Policy).

The principle also highlights a practical naming hazard: existing JSON manifest formats conventionally use lowercase, underscore-delimited (`snake_case`) keys, whereas DOM APIs use `camelCase`. When dictionaries are shared between a manifest and a DOM API (such as `ImageResource`), keys have to be converted between casing styles. To minimize friction across contexts, the principle recommends harmonizing naming conventions and preferring single-word keys that are identical in both `snake_case` and `camelCase`.

## Fit for Coding Agents

This principle aligns well with the ergonomics of AI coding agents (`good`) for three distinct reasons: avoiding out-of-band files when possible, consolidating unavoidable metadata into a single well-known location, and eliminating cross-context casing traps. First, the opening advice that features should be self-contained and ideally not require a manifest file directly benefits agents. Out-of-band JSON manifests split a feature's implementation across multiple files, are frequently omitted from an agent's active context window during targeted edits, and tend to fail silently when misconfigured.

Second, when a manifest is required, extending the Web App Manifest (`manifest.webmanifest`) rather than proliferating new feature-specific manifest files reduces scaffolding and wiring errors. Every new manifest format introduces extra deployment ceremony—`<link>` relations or `.well-known` paths, MIME types, CORS headers, service worker caching rules, and bundler static-asset configuration—that coding agents routinely forget to wire up end-to-end. Consolidating capabilities (like `share_target`, `file_handlers`, `protocol_handlers`, and `shortcuts`) into `manifest.webmanifest` lets agents rely on strong training-data priors and existing JSON Schema validation (`schemastore.org/web-manifest`) to catch typos immediately in the IDE/linter feedback loop.

Third, the note recommending single-word keys to avoid `snake_case` (manifest) versus `camelCase` (DOM dictionary) conversion targets a classic LLM hallucination failure mode. When the same conceptual dictionary (such as `ImageResource` or share/launch metadata) uses `short_name` or `form_factor` in JSON but `shortName` or `formFactor` in JavaScript, models frequently bleed casing conventions across boundaries—especially when generating inline JSON inside JS/TS build configs (like `vite-plugin-pwa` or Next.js metadata objects) where JS property conventions and raw manifest keys look nearly identical. Single-word keys (`src`, `sizes`, `type`, `purpose`, `label`) sidestep that ambiguity entirely.

## Value as a Slide Example

Despite being helpful in practice, this principle is too narrow and spec-process-oriented to serve as a standalone headline example on a TPAC slide (`neither`, strength 2/5). Most of the section reads as governance advice for W3C working groups on coordinating with Web App Manifest editors versus minting a new spec like Origin Policy or Publication Manifest, which is an infrequent architectural decision rather than a day-to-day developer or agent pain point.

However, the closing note on `snake_case` manifests versus `camelCase` DOM dictionaries—and the advice to prefer single-word keys when reusing dictionaries like `ImageResource`—is a useful supporting bullet if the deck has a broader slide on naming consistency and cross-boundary schema reuse (§12). It illustrates concretely how small surface inconsistencies between JSON configs and WebIDL dictionaries create predictable token-confusion traps for LLMs, and how simple rules like single-word keys eliminate an entire category of translation errors.
