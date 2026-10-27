---
section: "2.12"
id: "require-user-activation"
title: "Require user activation for powerful APIs"
chapter: "2. API Design Across Languages"
url: "https://w3ctag.github.io/design-principles/#require-user-activation"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 2
verdict: "An essential end-user security and anti-abuse boundary that applies regardless of whether a human or an agent wrote the code, though transient activation loss across async `await` boundaries is a common runtime footgun for coding agents."
---

# §2.12 Require user activation for powerful APIs

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=neutral | §2.12 require-user-activation — Require user activation for powerful APIs: An essential end-user security and anti-abuse boundary that applies regardless of whether a human or an agent wrote the code, though transient activation loss across async `await` boundaries is a common runtime footgun for coding agents.

- **URL:** https://w3ctag.github.io/design-principles/#require-user-activation
- **Chapter:** 2. API Design Across Languages
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** An essential end-user security and anti-abuse boundary that applies regardless of whether a human or an agent wrote the code, though transient activation loss across async `await` boundaries is a common runtime footgun for coding agents.

## Principle Summary

This principle states that web APIs capable of producing intrusive UI (such as auto-playing audio or fullscreen transitions), exposing or modifying user data (such as clipboard access), performing unannounced background activity, or triggering trusted browser permission and hardware prompts must require an indication of user intention—specifically HTML user activation. Spec authors are asked to calibrate the requirement to the risk and UX impact of the API by choosing between sticky activation (once per document lifetime), transient activation (within a short time window after a user gesture), or transient activation consumption (one API call per user gesture).

The principle exists to protect end users from drive-by abuse, permission fatigue, spoofing, and unwanted page behaviors. It ensures the browser can verify that a human user is intentionally interacting with the page before granting access to sensitive capabilities or disruptive UI surfaces.

## Fit for Coding Agents

At its core, this principle is neutral (orthogonal) to whether code is written by a human developer or an AI coding agent. It enforces a trust boundary between the untrusted web page and the end user. Even if coding agents write the vast majority of web application code—and arguably even more so when agents make it trivial to generate complex interactive sites rapidly—browsers must still require genuine user intent before opening file pickers, reading the clipboard, requesting hardware devices, or triggering popups.

However, the mechanics of how user activation is specified create a notable practical pitfall for coding agents: losing transient user activation across asynchronous `await` boundaries. When an LLM generates an event handler (for example, fetching data from a server before copying it to the clipboard via `navigator.clipboard.writeText()`, sharing via `navigator.share()`, or opening a save dialog via `window.showSaveFilePicker()`), its default statistical pattern is to write sequential `await fetch(...)` calls before invoking the gated Web API. If the network request takes longer than the transient activation window—or in browsers where activation is lost or consumed across async ticks—the call fails at runtime even though it originated inside a `click` handler. Coding agents also routinely attempt to call activation-gated APIs inside `useEffect` hooks on mount or inside background callbacks.

Where API design does affect coding agents under this principle is in failure observability and async ergonomics. When an activation check fails, APIs that reject with a descriptive `NotAllowedError` `DOMException` explicitly mentioning user activation give coding agents an immediate, actionable signal in their Playwright/DevTools test loop, whereas legacy APIs that fail silently (such as `input.click()` or `window.open()` returning `null`) cause agents to waste turns debugging application logic. Furthermore, API designs that allow invoking the activation-gated method synchronously with an unresolved Promise payload—such as passing a `Promise<Blob>` inside `new ClipboardItem({ 'text/plain': fetchPromise })` to `navigator.clipboard.write()`—let agents satisfy transient activation upfront without restructuring their async data fetching into awkward two-step UI flows.

## Value as a Slide Example

This principle is neither a strong `clearly-useful` nor `clearly-harmful` headline example (`2/5`) for a TPAC session on adapting web standards for coding agents, because the underlying rule is a non-negotiable end-user security and privacy constraint rather than a developer-ergonomics trade-off. No one would propose removing user activation requirements to make coding agents' lives easier.

To the extent it merits a brief mention at TPAC, it works best as a nuanced side note under error reporting and async API ergonomics: if an API requires transient user activation, specs should (1) accept deferred/Promise inputs at the synchronous call site (like `ClipboardItem` accepting Promises) so standard `async`/`await` agent code doesn't expire transient activation during a `fetch()`, and (2) mandate loud, machine-actionable `NotAllowedError` messages rather than silent no-ops when user activation is missing.
