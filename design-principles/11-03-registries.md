---
section: "11.3"
id: "registries"
title: "Plan for future extensibility through main spec updates if possible; otherwise use a registry"
chapter: "11. Writing good specifications"
url: "https://w3ctag.github.io/design-principles/#registries"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 1
verdict: "Spec-governance guidance on managing extension points via main spec revisions or IANA/W3C registries, largely orthogonal to AI coding agents beyond a mild benefit from centralized, short-string token sets over URI namespaces."
---

# §11.3 Plan for future extensibility through main spec updates if possible; otherwise use a registry

GREP_SUMMARY: slide_example=neither | strength=1/5 | agent_fit=neutral | §11.3 registries — Plan for future extensibility through main spec updates if possible; otherwise use a registry: Spec-governance guidance on managing extension points via main spec revisions or IANA/W3C registries, largely orthogonal to AI coding agents beyond a mild benefit from centralized, short-string token sets over URI namespaces.

- **URL:** https://w3ctag.github.io/design-principles/#registries
- **Chapter:** 11. Writing good specifications
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 1/5
- **Verdict:** Spec-governance guidance on managing extension points via main spec revisions or IANA/W3C registries, largely orthogonal to AI coding agents beyond a mild benefit from centralized, short-string token sets over URI namespaces.

## Principle Summary

This principle advises specification authors on how to manage features that are expected to be extended over time. Because variability complicates interoperability, the simplest and most coherent approach is to define optional features and future extensions directly via revisions to the main specification under a single working group. When a wider set of participants or implementers needs to add extensions without waiting for a full specification revision, spec authors should establish an explicit registry (typically an IANA registry under RFC 8126 or a W3C Registry) with clear extension point rules, specifications for registered entries, and at least one mandatory-to-implement entry so independent implementations can interoperate.

The principle also warns against using uncoordinated URLs or URIs as extension identifiers (such as XML namespaces) as a shortcut around maintaining a registry table, noting that domain-based URIs sacrifice specification-backed interoperability and risk domain loss. It illustrates the tradeoffs of registry design using the Well-Known URI registry (`/.well-known/`, RFC 8615) and HTML `rel` link relations—where values are split across the IANA Link Relations registry (RFC 8288), the permissive Microformats Wiki, and the HTML specification's table of browser-recognized link types.

## Fit for Coding Agents

This principle is primarily about standards-body governance, specification maintenance, and multi-implementer coordination rather than developer or coding-agent ergonomics, making it largely neutral for AI coding agents. Whether a web application is written by a human or an LLM does not change how W3C or IETF working groups decide between revising a main specification and delegating identifier allocation to an IANA or W3C registry.

Where the principle touches developer-facing surfaces, its secondary effects slightly favor coding agents in two ways while introducing one recurring point of friction. First, preferring main-spec updates (like the HTML specification's canonical table of browser-supported `<link rel="...">` keywords) over fragmented external registries concentrates documentation, MDN guides, and TypeScript DOM definitions (`lib.dom.d.ts`) in a single authoritative place, which strengthens LLM training priors and enables static type checking. Second, favoring short registered strings over URI-based extension identifiers (such as `xmlns="http://www.w3.org/2000/svg"` or custom XML namespace URIs) saves tokens and avoids a classic class of LLM errors where models hallucinate or transpose date-stamped namespace URLs.

Conversely, when a web platform feature relies on open-ended or multi-part registries—such as `rel` values split across IANA, the Microformats Wiki, and HTML, or open string extension points that cannot be closed into a TypeScript union type—coding agents lose compiler feedback (since the DOM attribute is typed simply as `string`) and can hallucinate valid-looking registered tokens that have no actual browser behavior. Furthermore, unrecognized registry tokens (like an unsupported `<link rel>` keyword) typically fail silently in browsers, offering no runtime signal in an agent's execution loop. Even so, these are downstream consequences of open string extension points rather than the primary subject of §11.3.

## Value as a Slide Example

This principle is neither a strong example of a rule that clearly helps coding agents nor one that backfires for them (1/5). Because it focuses on institutional standards process—when a Working Group should revise its own spec versus setting up an IANA/W3C registry, and how strict registration policies should be—featuring it on a TPAC slide about how AI coding agents are redefining developer experience would distract from concrete API and language ergonomics.

If registries are mentioned at all in an agentic DX discussion, the relevant takeaway is not IANA vs. W3C registration policy, but that machine-readable, single-source-of-truth enumerations (exposed via Web IDL enums, `@webref`, and TypeScript union types) are far more valuable to coding agents than prose-only or wiki-based registries (like the Microformats `rel` wiki) where browser-supported tokens cannot be statically distinguished from inert metadata.
