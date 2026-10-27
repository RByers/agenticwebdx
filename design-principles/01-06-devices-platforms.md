---
section: "1.6"
id: "devices-platforms"
title: "Support the full range of devices and platforms (Media Independence)"
chapter: "1. Principles behind design of Web APIs"
url: "https://w3ctag.github.io/design-principles/#devices-platforms"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Designing APIs so the easiest path is media-independent is critical for coding agents, which default to desktop-centric training priors and verify their work inside headless desktop browsers."
---

# §1.6 Support the full range of devices and platforms (Media Independence)

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §1.6 devices-platforms — Support the full range of devices and platforms (Media Independence): Designing APIs so the easiest path is media-independent is critical for coding agents, which default to desktop-centric training priors and verify their work inside headless desktop browsers.

- **URL:** https://w3ctag.github.io/design-principles/#devices-platforms
- **Chapter:** 1. Principles behind design of Web APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Designing APIs so the easiest path is media-independent is critical for coding agents, which default to desktop-centric training priors and verify their work inside headless desktop browsers.

## Principle Summary

W3C TAG Design Principle §1.6 ("Support the full range of devices and platforms (Media Independence)") states that web features should work across the full spectrum of input and output devices, screen sizes, interaction modes, platforms, and media (including print and assistive technologies). It highlights that features should adapt gracefully when a device does not support their original interaction model—citing how a mobile tap fires a `click` event as a fallback—and emphasizes that "features should also be designed so that the easiest way to use them maintains flexibility." When features are not yet available across all platforms, they should support feature detection, graceful failure, or polyfilling (referencing §2.6).

For human developers and browser engines, this principle preserves the core value proposition of the universal web: authors should not have to write separate codebases for desktop mice, mobile touchscreens, keyboards, screen readers, or print media, and end users on diverse hardware or assistive technologies should not be locked out of web applications.

## Fit for Coding Agents

At first glance, one might assume media independence matters less when code is written by an AI agent: if supporting touch, mouse, keyboard, and screen readers requires extra boilerplate, an LLM can generate those extra lines of code almost for free. In practice, the opposite is true. Coding agents make the rule that "the easiest way to use [features] maintains flexibility" even more critical than it was for human authors, for two structural reasons.

First, LLMs are statistical engines that strongly favor the shortest, highest-probability pattern in their training data unless explicitly prompted to handle edge-case modalities. When an API requires separate handling per device modality—such as wiring up `touchstart`/`touchmove` alongside `mousedown`/`mousemove`, or manually listening for `Escape` on `keydown` without handling mobile back gestures—agents routinely emit only the desktop mouse/keyboard path. When the simplest, lowest-token primitive is media-independent by default—such as `click` firing on mouse click, tap, `Enter`/`Space`, and assistive technology activation, or `<dialog>` and `popover` automatically handling both desktop `Escape` and Android system back gestures via `CloseWatcher`—agent-written code inherits cross-device support automatically.

Second, autonomous coding agents verify their work in a narrow feedback loop using headless browser automation (such as Playwright or Chrome DevTools MCP inside a Linux container), almost always configured with a desktop viewport and synthetic mouse/keyboard actions. An agent cannot physically pick up a phone, test with a stylus, feel an awkward touch target, or notice that a hover-only menu is unreachable on touch devices; any device-specific bug passes the agent's automated verification silently. Furthermore, when features are restricted to specific platforms (such as `navigator.share` or `window.showOpenFilePicker`), agents frequently assume universal availability based on training data, making clear feature detection and graceful fallback essential to prevent unhandled runtime exceptions outside the agent's desktop test container.

## Value as a Slide Example

This principle is a solid supporting example (3/5, `clearly-useful`) for a TPAC slide because it directly refutes a common misconception about AI coding assistants—namely, that "because agents can write boilerplate cheaply, the web platform doesn't need high-level, device-independent defaults." On a slide, it highlights a sharp, memorable reality of agentic DX: agents only fix what their verification loop can observe, and an agent's verification loop is almost always a headless desktop browser with synthetic clicks and keystrokes.

Concrete Web API examples that make this tangible for a standards audience include `<dialog>`, `popover`, and `CloseWatcher` versus manual `keydown` (`Escape`) listeners (where an agent's `e.key === 'Escape'` check passes desktop Playwright tests while breaking Android back-gesture dismissal), as well as unified `click` and `PointerEvent` abstractions versus legacy `mousedown`/`mousemove` handlers that agents still frequently copy from training data. While not as centrally about agent-specific syntax or error reporting as some later principles, its "pit of success" mandate (`the easiest way to use them maintains flexibility`) is a compelling reason why high-level, multi-modal HTML/DOM primitives matter more than ever in an era of agent-authored code.
