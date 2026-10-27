---
section: "1.4.1"
id: "user-decisions"
title: "Help users make good decisions"
chapter: "1. Principles behind design of Web APIs"
url: "https://w3ctag.github.io/design-principles/#user-decisions"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 2
verdict: "Primarily an end-user security and consent-UX principle orthogonal to whether code is written by a human or an agent, though its push for safe default API patterns helps agents while its recommendation to make permission refusal indistinguishable from other states can hinder agent debugging loops."
---

# §1.4.1 Help users make good decisions

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=neutral | §1.4.1 user-decisions — Help users make good decisions: Primarily an end-user security and consent-UX principle orthogonal to whether code is written by a human or an agent, though its push for safe default API patterns helps agents while its recommendation to make permission refusal indistinguishable from other states can hinder agent debugging loops.

- **URL:** https://w3ctag.github.io/design-principles/#user-decisions
- **Chapter:** 1. Principles behind design of Web APIs
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Primarily an end-user security and consent-UX principle orthogonal to whether code is written by a human or an agent, though its push for safe default API patterns helps agents while its recommendation to make permission refusal indistinguishable from other states can hinder agent debugging loops.

## Principle Summary

This principle guides browser vendors and specification authors on how to manage security and privacy risks without overwhelming end users with incomprehensible or fatiguing permission prompts. It argues that risk should be mitigated at the API design level first so that a "bad" user decision cannot result in catastrophic harm (such as device compromise or severe data exposure). When asking the user is unavoidable, prompts must provide clear context, connect risks directly to the feature's utility (avoiding abstract technical questions like fingerprinting), offer persistent visibility into ongoing permissions, and allow users to revoke access at any time.

It also emphasizes that respecting user intent should be the natural outcome of following the simplest, default usage pattern of an API, rather than requiring complex developer effort. Finally, when a user denies permission, the site must not be able to obtain the same data through side channels or alternative APIs, and ideally the API should make refusal indistinguishable from other common situations so sites cannot easily coerce or nag users into granting consent.

## Fit for Coding Agents

At its core, this principle is neutral (orthogonal) with respect to AI coding agents because it governs the relationship between the browser, the website, and the end user's security and privacy. End users suffer from decision fatigue, lack of technical context, and coercive permission walls regardless of whether the website's JavaScript was authored by a human engineer or an LLM agent. Most of the guidance—such as reminding users of persistent permissions in browser UI or avoiding prompts for subtle risks like fingerprinting—addresses browser UX and capability scoping rather than developer ergonomics.

Where the principle does touch developer experience, it cuts in two opposite directions for coding agents. On the positive side, the advice that "respect for user intent is a natural outcome of following the simple, obvious, or default usage pattern for the API" (for example, using one-off in-context choosers like `<input type="file">` or `showOpenFilePicker()` instead of broad standing permissions) aligns strongly with how LLM agents generate code. Coding agents gravitate toward the shortest, highest-probability usage pattern in their training data; they frequently omit complex permission pre-checks (`navigator.permissions.query`), revocation listeners (`onchange`), or multi-step consent state machines unless explicitly prompted. Designing APIs where the default one-liner is inherently safe and user-intent-preserving reduces boilerplate and prevents agents from shipping broken permission flows.

On the negative side, two aspects of the principle create friction for autonomous agent workflows. First, the recommendation that "refusal is most effective if the site cannot distinguish refusal from other, common situations" intentionally degrades observability: when an agent runs automated tests or debugs an application, an indistinguishable refusal (such as returning an empty device list or a generic failure instead of a clear `NotAllowedError`) can trick the agent into thinking its application logic is buggy, triggering hallucinated code rewrites rather than recognizing a denied permission. Second, APIs gated on interactive browser chooser prompts and transient user activation are harder for coding agents to verify autonomously in headless browser loops unless standardized WebDriver BiDi or Permissions API automation hooks exist alongside them.

## Value as a Slide Example

This principle is not a headline slide example (`neither`, strength 2/5) because a W3C TPAC audience will immediately recognize it as an end-user privacy and consent rule rather than a developer ergonomics rule. Featuring it as a primary example of how standards should adapt to coding agents would risk conflating end-user protection with developer convenience.

However, one specific sentence in the principle—"Refusal is most effective if the site cannot distinguish refusal from other, common situations"—makes an interesting secondary talking point about the tension between end-user privacy obfuscation (such as returning empty `enumerateDevices()` results or disguising permission denial as hardware unavailability) and agent feedback-loop observability. While hiding the reason for failure protects end users from dark patterns in production, coding agents in development/test environments rely heavily on loud, specific diagnostics to self-correct, highlighting why browsers and test automation protocols like WebDriver BiDi need clear developer/agent inspection channels even when runtime JS APIs intentionally obscure refusal states.
