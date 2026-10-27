---
section: "1.10"
id: "data-minimization"
title: "Minimize user data"
chapter: "1. Principles behind design of Web APIs"
url: "https://w3ctag.github.io/design-principles/#data-minimization"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 2
verdict: "Primarily an end-user privacy principle orthogonal to agent DX, though its 'pit of success' advice—making minimal-data APIs lower friction than bulk-data APIs—matters even more when LLMs default to the lowest-ceremony code path."
---

# §1.10 Minimize user data

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=neutral | §1.10 data-minimization — Minimize user data: Primarily an end-user privacy principle orthogonal to agent DX, though its 'pit of success' advice—making minimal-data APIs lower friction than bulk-data APIs—matters even more when LLMs default to the lowest-ceremony code path.

- **URL:** https://w3ctag.github.io/design-principles/#data-minimization
- **Chapter:** 1. Principles behind design of Web APIs
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Primarily an end-user privacy principle orthogonal to agent DX, though its 'pit of success' advice—making minimal-data APIs lower friction than bulk-data APIs—matters even more when LLMs default to the lowest-ceremony code path.

## Principle Summary

Section 1.10 ("Minimize user data") directs spec authors to design Web APIs so that features work with the minimum amount of user data necessary to accomplish the user's goal, reducing the risk of inappropriate disclosure, fingerprinting, or misuse. Rather than granting broad or bulk access to personal data, APIs should provide fine-grained access and user controls aligned with explicit user intent (such as pickers that return a single user-chosen item rather than full device access).

Crucially, the principle frames data minimization as an ergonomic design rule: APIs should make it easier for websites to request, collect, and transmit small, specific pieces of data than generic or bulk data, requiring extra steps or explicit user consent only when additional functionality genuinely requires more data.

## Fit for Coding Agents

At its core, this principle is neutral (orthogonal) to coding-agent DX because its primary purpose is protecting the end user's privacy from the website, regardless of whether the site's code was authored by a human developer or an AI coding agent. The browser trust boundary must enforce data minimization irrespective of developer ergonomics. In fact, enforcing data minimization at the Web API boundary becomes even more valuable when coding agents author and debug web applications: agents routinely serialize entire returned objects into `fetch()` payloads, telemetry, or `console.log()` output during automated test-and-fix loops without inspecting which fields contain sensitive PII. When an API returns only the minimal, task-specific data by default, an agent cannot inadvertently leak excess user data through naive object serialization.

Where the principle directly touches agent behavior is its "pit of success" instruction: make it easier for sites to request granular, minimal data than generic or bulk data. LLM coding agents strongly favor the lowest-ceremony, lowest-token path in their training distribution. When a minimal-data API is a simple one-line call (such as `<input type="file">`, `navigator.share()`, or low-entropy `navigator.userAgentData.mobile`), agents use it cleanly. Conversely, when a granular API introduces multi-step async ceremony while a legacy bulk surface remains a one-liner (e.g., reading `navigator.userAgent` vs. calling `navigator.userAgentData.getHighEntropyValues([...])` with exact string hints), agents often revert to the legacy bulk surface from training priors. Aligning the simplest API call with minimal data disclosure ensures agents take the privacy-preserving path by default.

## Value as a Slide Example

This principle is neither a strong `clearly-useful` nor `clearly-harmful` slide example for a TPAC session on how agents redefine DX (`2/5`). A W3C audience will view data minimization as a non-negotiable end-user privacy principle (putting users above authors in the Priority of Constituencies) that applies identically whether code is written by humans or machines, so featuring it on a DX slide would muddy the distinction between developer ergonomics and end-user protections.

At best, it serves as a brief supporting point about "pit of success" defaults: because LLM coding agents systematically pick the lowest-ceremony API in their training data and often pass or log entire response objects verbatim, making the minimal-data API path simpler than bulk data access (as seen in `navigator.share()` or file pickers versus bulk contact/filesystem APIs) helps keep agent-written web apps privacy-preserving by default.
