---
section: "12.4"
id: "naming-future-proofing"
title: "Use names that describe a purpose"
chapter: "12. Naming principles"
url: "https://w3ctag.github.io/design-principles/#naming-future-proofing"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Naming APIs after their purpose rather than transient protocols or brands aligns identifiers with intent-based prompts and prevents API-rename churn in LLM training data, though overly generic purpose names like WebTransport can obscure distinguishing semantics."
---

# §12.4 Use names that describe a purpose

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §12.4 naming-future-proofing — Use names that describe a purpose: Naming APIs after their purpose rather than transient protocols or brands aligns identifiers with intent-based prompts and prevents API-rename churn in LLM training data, though overly generic purpose names like WebTransport can obscure distinguishing semantics.

- **URL:** https://w3ctag.github.io/design-principles/#naming-future-proofing
- **Chapter:** 12. Naming principles
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Naming APIs after their purpose rather than transient protocols or brands aligns identifiers with intent-based prompts and prevents API-rename churn in LLM training data, though overly generic purpose names like WebTransport can obscure distinguishing semantics.

## Principle Summary

W3C TAG Principle §12.4 advises spec authors to name web APIs for what they do (their purpose) rather than how they do it (their underlying implementation technology, internal codename, or proprietary brand inspiration). Because removing or renaming shipped web APIs is extremely difficult, names tied to specific protocols or vendor brands risk becoming anachronistic when the underlying technology evolves or is replaced.

The principle highlights two positive examples: the Remote Playback API (HTMLMediaElement.remote), which uses general functional terms rather than proprietary brand inspirations like Chromecast or AirPlay, and the WebTransport API, which is named for the general purpose of transporting data rather than the underlying QUIC protocol (RFC 9000) it initially exposes. Conversely, the classic historical counterexample on the web is XMLHttpRequest, whose name hardcodes both XML and HTTP despite being used for decades to fetch JSON and binary data.

## Fit for Coding Agents

This principle is a good fit for AI coding agents for two primary reasons: intent-to-API alignment and training-corpus stability. First, coding agents operate on an intent-driven loop where users prompt with functional goals ("allow the user to play this video on a remote screen", "fetch JSON from this endpoint") rather than browser implementation internals. When API names reflect purpose (RemotePlayback, fetch, IntersectionObserver), the lexical and semantic distance between a natural-language prompt and the target API is minimal, improving zero-shot API selection and making generated code self-describing in the context window. Second, future-proofing names against implementation changes avoids API deprecations and replacements. Whenever the platform has to introduce a new API name because an old one was tied to an obsolete technology, LLM training corpora suffer years of "split-brain" pollution where models mix legacy and modern surfaces. Keeping WebTransport stable even if QUIC evolves to a new transport protocol preserves the validity of existing training weights.

However, the principle has two notable nuances when applied to LLMs. First, LLMs are far more tolerant of historical implementation-bound misnomers than human newcomers once an API is ubiquitous in training data: no agent struggles to fetch JSON with XMLHttpRequest just because "XML" is in the identifier, even though fetch() is cleaner and more token-efficient. Second, taking "name for purpose" too far toward abstraction can backfire when multiple APIs share the same broad purpose. Calling an API WebTransport because it "transports data" obscures how its purpose differs from fetch(), WebSocket, and RTCDataChannel—all of which also transport data on the web. When a user prompts an agent for low-latency unreliable datagrams or multiplexed streams without head-of-line blocking (or explicitly asks for "QUIC in the browser"), an overly generic name like WebTransport provides less semantic signal about its distinguishing capabilities than a name referencing multiplexed streams or datagrams.

## Value as a Slide Example

This principle is a solid supporting example (clearly-useful, 3/5 strength) for a TPAC slide discussing how traditional naming hygiene translates to agentic DX, though it works better as a grouped bullet or nuanced contrast than as a standalone headline slide.

On a slide, the contrast between XMLHttpRequest vs. fetch() and RemotePlayback vs. Chromecast/AirPlay immediately illustrates why purpose-oriented naming helps intent-driven agents map user goals to web APIs without vendor fragmentation or deprecation churn. Even more interestingly for a standards audience, the WebTransport example in §12.4 offers a sharp talking point on the boundary of this rule: while avoiding transient protocol names (like WebQUICv1) protects training-data longevity, making a purpose name too abstract (WebTransport vs. WebSocket) forces agents and developers to rely on out-of-band documentation or memorized priors to know which data-transport API fits a given task.
