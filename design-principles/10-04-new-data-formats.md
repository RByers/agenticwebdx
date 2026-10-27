---
section: "10.4"
id: "new-data-formats"
title: "Add new data formats properly"
chapter: "10. Other API Design Considerations"
url: "https://w3ctag.github.io/design-principles/#new-data-formats"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Integrating new formats uniformly into existing ingress and egress APIs via standard MIME types matches how LLMs generalize across APIs and prevents silent fallback traps, though IANA registration and MIME-sniffing policy are mostly spec/browser hygiene."
---

# §10.4 Add new data formats properly

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §10.4 new-data-formats — Add new data formats properly: Integrating new formats uniformly into existing ingress and egress APIs via standard MIME types matches how LLMs generalize across APIs and prevents silent fallback traps, though IANA registration and MIME-sniffing policy are mostly spec/browser hygiene.

- **URL:** https://w3ctag.github.io/design-principles/#new-data-formats
- **Chapter:** 10. Other API Design Considerations
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Integrating new formats uniformly into existing ingress and egress APIs via standard MIME types matches how LLMs generalize across APIs and prevents silent fallback traps, though IANA registration and MIME-sniffing policy are mostly spec/browser hygiene.

## Principle Summary

Whenever a new data format (such as an image, audio, video, or text format) is introduced to the web platform, spec authors must define and register a strictly validated standard MIME type with IANA, mandate UTF-8 for any text-based format, and integrate the format into existing platform APIs for both ingress (decoding) and egress (encoding). Rather than extending legacy MIME-sniffing heuristics—which carry security risks and exist only for backward compatibility—browsers must enforce strict MIME type validation on new formats.

For human developers and browser engines, this ensures that new formats behave consistently as first-class citizens across the platform (for example, an image format working in `HTMLCanvasElement.toBlob()` and `toDataURL()` as well as `HTMLImageElement`), while avoiding the security vulnerabilities and encoding ambiguities of legacy content-sniffing and non-UTF-8 character sets.

## Fit for Coding Agents

This principle is a good fit for AI coding agents, primarily because of its requirement to integrate new formats symmetrically across existing ingress and egress APIs using a standard MIME type string. LLMs rely heavily on compositional generalization: once an agent knows how to use `HTMLCanvasElement.toBlob(callback, type, quality)`, `OffscreenCanvas.convertToBlob({ type })`, `ClipboardItem`, or `new Blob([data], { type })`, it expects any platform-supported data format to work across all of those surfaces simply by passing the new MIME type string (e.g., `'image/avif'` or `'image/webp'`). Plugging new formats into existing MIME-based APIs avoids bespoke format-specific APIs, reduces token overhead, and lets agents transfer priors from older formats with high accuracy.

When the platform violates this principle by adding partial or asymmetric format support—such as supporting a format for ingress in `<img>` and `createImageBitmap()`, but omitting it from egress in `canvas.toBlob()`, `canvas.toDataURL()`, or the Async Clipboard API's safelist—coding agents routinely hallucinate that egress works too. Worse, existing canvas egress APIs fail silently when given an unsupported or unintegrated MIME type: per the HTML specification, `canvas.toBlob(cb, 'image/unsupported')` and `canvas.toDataURL('image/unsupported')` silently fall back to `image/png` rather than throwing an error. In an agentic feedback loop, a test checking only that a non-empty `Blob` was returned will pass, hiding the bug unless the agent explicitly asserts on `blob.type`. Requiring full ingress and egress integration across existing APIs directly eliminates this class of hallucination and silent fallback.

The remaining parts of the principle—mandating UTF-8 for text formats and enforcing strict MIME validation instead of content sniffing—also generally help agents. UTF-8 exclusivity removes legacy character-encoding footguns (`TextDecoder` charset mismatches, BOM quirks) where training data is error-prone. While strict MIME type enforcement can occasionally trip up an agent configuring a local dev server that lacks a mapping for a brand-new file extension, failing deterministically on an invalid `Content-Type` header is much easier for an agent to diagnose in its feedback loop than debugging legacy MIME-sniffing heuristics.

## Value as a Slide Example

Despite aligning well with agent ergonomics, this principle is not a strong standalone slide example (`neither`, `2/5`) for the TPAC breakout session. Much of the principle focuses on browser security and standards-body housekeeping—registering MIME types with IANA and not extending legacy MIME-sniffing algorithms—which are orthogonal to whether web code is written by a human or an AI agent.

If referenced at all, its best value is as a brief supporting example under a broader point about **API symmetry and silent fallbacks**: because LLMs assume uniform capability matrices across standard MIME-accepting APIs, partial integration of a data format (e.g., `image/avif` working in `<img>` before `canvas.toBlob('image/avif')` is supported, where `toBlob` silently falls back to `image/png`, or `ClipboardItem` rejecting the MIME type) causes agents to hallucinate support and miss silent encoding fallbacks. However, core API design principles around consistency, loud errors, and abstraction level provide much stronger headline slide material.
