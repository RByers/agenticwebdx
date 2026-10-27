---
section: "3.6"
id: "naming-of-url-attributes"
title: "Name URL-containing attributes based on their primary purpose"
chapter: "3. HTML"
url: "https://w3ctag.github.io/design-principles/#naming-of-url-attributes"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Consistent purpose-based URL attribute naming (`href` for navigation, `src` for loading, semantic names for auxiliary URLs) aligns directly with LLM statistical priors and reduces silent attribute hallucinations on new or infrequent HTML elements."
---

# §3.6 Name URL-containing attributes based on their primary purpose

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §3.6 naming-of-url-attributes — Name URL-containing attributes based on their primary purpose: Consistent purpose-based URL attribute naming (`href` for navigation, `src` for loading, semantic names for auxiliary URLs) aligns directly with LLM statistical priors and reduces silent attribute hallucinations on new or infrequent HTML elements.

- **URL:** https://w3ctag.github.io/design-principles/#naming-of-url-attributes
- **Chapter:** 3. HTML
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Consistent purpose-based URL attribute naming (`href` for navigation, `src` for loading, semantic names for auxiliary URLs) aligns directly with LLM statistical priors and reduces silent attribute hallucinations on new or infrequent HTML elements.

## Principle Summary

Section 3.6 ("Name URL-containing attributes based on their primary purpose") establishes a three-part naming convention for HTML attributes that hold URLs: use `href` when the element enables user navigation (like `<a href>`, noting that `<form action>` should have been `href` in hindsight), use `src` when the element loads an external resource (like `<img src>` or `<script src>`, noting `<link href>` as a legacy inconsistency not to be emulated), and use a specific semantic name when the URL is auxiliary to the element's primary purpose (like `<video poster>`, `<q cite>`, or `<a ping>`). It also reminds spec authors to reflect URL attributes as `USVString` in WebIDL.

For human developers, this principle reduces cognitive load and guesswork across HTML elements by ensuring that an attribute's name reliably communicates whether a URL will be fetched immediately as a subresource, navigated to upon user interaction, or used for an auxiliary purpose.

## Fit for Coding Agents

This principle is a good fit for AI coding agents because it directly reinforces the statistical priors LLMs learn from existing HTML corpora and mitigates one of HTML's worst agent feedback-loop traps: silent failure on unknown attributes. Across billions of lines of training data, LLMs strongly associate `href` with navigation and hyperlinks, `src` with embedded subresource fetching, and descriptive names (`poster`, `cite`, `ping`) with secondary URLs.

While models have thoroughly memorized high-frequency legacy exceptions like `<link rel="stylesheet" href="...">`, `<form action="...">`, and `<object data="...">`, their accuracy drops on newly standardized HTML elements, niche elements in the long tail of training data (e.g., `<model>`, `<fencedframe>`, `<track>`, `<embed>`), and custom elements. When a new element adheres to this principle, an agent can zero-shot predict `src` or `href` from the element's behavioral category even if the element rarely appeared in pre-training data.

Crucially, HTML parsers do not throw syntax or runtime errors when an unknown attribute is used—an agent that hallucinates `<new-media-element url="clip.mp4">` or mixes up `src` and `href` on an unfamiliar tag produces valid DOM markup that fails silently at runtime unless caught by a linter or network/visual inspection in a browser. By standardizing on `href` for navigation, `src` for resource loading, and semantic names for auxiliary URLs (rather than introducing synonyms like `url`, `uri`, `data`, or `action`), web standards eliminate unnecessary degrees of freedom where agents might guess wrong and fail silently, while also making unfamiliar markup self-describing when agents read code in context.

## Value as a Slide Example

This principle is a solid supporting example (3/5, `clearly-useful`) for a TPAC slide, particularly as a quick, relatable illustration of how predictable naming conventions leverage LLM priors and prevent silent HTML failures. Every standards participant has experienced the friction of `<script src>` vs. `<link href>` vs. `<form action>` vs. `<object data>`, and pointing out that HTML ignores wrong attributes silently (`<script href="...">` does nothing with zero console errors) makes it immediately obvious why consistent `src` vs. `href` naming helps agents accurately generate markup for newer elements like `<model src>` or `<fencedframe src>`.

It rates a 3/5 rather than a 5/5 because LLMs have already memorized the most famous legacy exceptions (`<link href>`, `<form action>`) from massive pre-training corpora, so agents rarely fail on those classic tags in practice. As a result, it works best as a concise supporting bullet under a broader slide on "Aligning new APIs with platform priors to avoid silent no-ops" rather than a standalone headline slide.
