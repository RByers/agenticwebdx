---
section: "1.4"
id: "user-intent"
title: "Design for user intent"
chapter: "1. Principles behind design of Web APIs"
url: "https://w3ctag.github.io/design-principles/#user-intent"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 2
verdict: "Primarily an end-user security and UX principle governing browser permission prompts and capability gating, largely orthogonal to whether code is written by a human or a coding agent."
---

# §1.4 Design for user intent

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=neutral | §1.4 user-intent — Design for user intent: Primarily an end-user security and UX principle governing browser permission prompts and capability gating, largely orthogonal to whether code is written by a human or a coding agent.

- **URL:** https://w3ctag.github.io/design-principles/#user-intent
- **Chapter:** 1. Principles behind design of Web APIs
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Primarily an end-user security and UX principle governing browser permission prompts and capability gating, largely orthogonal to whether code is written by a human or a coding agent.

## Principle Summary

Section 1.4 ("Design for user intent") instructs web specification authors to design APIs accessing potentially unsafe capabilities so that their behavior naturally matches what the end user intends and expects. When an API's invocation inherently aligns with user expectations—or when the capability can be easily reverted and causes at most mild annoyance—browsers can avoid interrupting the user with explicit confirmation dialogs that cause permission fatigue and regrettable security decisions.

For example, websites do not need to trigger a permission prompt to play audio because users can easily identify and mute or close a noisy tab, and browsers can gate autoplay or clipboard writes on user interaction or revocable browser UI controls instead of upfront permission prompts.

## Fit for Coding Agents

At its core, "Design for user intent" governs the security and UX boundary between an untrusted website and the human end user operating the browser. Because a potentially harmful capability—such as reading local files, accessing device hardware, or modifying persistent state—poses the exact same risk to the end user whether the site's JavaScript was authored by a human developer or an AI coding agent, this principle is largely orthogonal to coding agent ergonomics (`neutral`).

Looking at secondary developer-experience effects, designing APIs around implicit user intent rather than explicit permission prompts has minor tradeoffs for coding agents. On the positive side, eliminating upfront permission prompts for reversible or intent-aligned actions reduces the amount of permission-state boilerplate (`navigator.permissions.query()`, handling `'granted' | 'denied' | 'prompt'` states, and rendering custom pre-permission UI) that an agent has to generate and maintain, and prevents headless browser verification loops from stalling on unexpected permission prompts.

On the other hand, the primary mechanism web specs use to verify "user intent" without a permission prompt is transient user activation (for example, requiring a click gesture before calling `audio.play()`, `navigator.clipboard.writeText()`, `HTMLElement.requestFullscreen()`, or `window.showOpenFilePicker()`). LLM coding agents frequently struggle with transient activation boundaries—such as calling intent-gated APIs inside `useEffect`/page-load hooks or after an asynchronous `fetch()`/`await` that expires the user gesture—leading to runtime `NotAllowedError` exceptions that only surface during interactive or end-to-end testing.

## Value as a Slide Example

This principle is a poor headline slide example (`neither`, 2/5) for a session on how coding agents change developer experience, because it is fundamentally an end-user security and anti-permission-fatigue guideline rather than a developer-ergonomics rule. Putting it on a slide risks confusing the audience into thinking that coding agents somehow change the browser's responsibility to protect end users from unsafe capabilities.

If mentioned at all, its main relevance would be as a quick contrast between *coding agents* (where user-intent gating mainly manifests as transient user activation `NotAllowedError` traps in async code and Playwright tests) and *browser-operating agents* (where APIs that rely on human physical gestures or OS file pickers to establish user intent face new challenges when an AI agent acts on the user's behalf).
