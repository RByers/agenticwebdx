---
section: "10.2.1"
id: "worker-only"
title: "Some APIs should only be exposed to dedicated workers"
chapter: "10. Other API Design Considerations"
url: "https://w3ctag.github.io/design-principles/#worker-only"
agent_fit: "mixed"
slide_example: "neither"
example_strength: 3
verdict: "Agents need hard worker-only boundaries even more than humans because they cannot perceive UI jank in functional tests and easily generate postMessage glue, but file/URL-based worker and worklet loading creates multi-file bundling traps."
---

# §10.2.1 Some APIs should only be exposed to dedicated workers

GREP_SUMMARY: slide_example=neither | strength=3/5 | agent_fit=mixed | §10.2.1 worker-only — Some APIs should only be exposed to dedicated workers: Agents need hard worker-only boundaries even more than humans because they cannot perceive UI jank in functional tests and easily generate postMessage glue, but file/URL-based worker and worklet loading creates multi-file bundling traps.

- **URL:** https://w3ctag.github.io/design-principles/#worker-only
- **Chapter:** 10. Other API Design Considerations
- **Agent-Fit:** mixed
- **Slide-Example:** neither
- **Example-Strength:** 3/5
- **Verdict:** Agents need hard worker-only boundaries even more than humans because they cannot perceive UI jank in functional tests and easily generate postMessage glue, but file/URL-based worker and worklet loading creates multi-file bundling traps.

## Principle Summary

W3C TAG Design Principle §10.2.1 states that APIs likely to block rendering or cause main-thread jank when used as intended should be restricted to `DedicatedWorkerGlobalScope` rather than exposed on `Window`. It rests on a behavioral observation about human developers: developers prefer simple code over complex code and will naturally use an API in the easiest way it allows. If a potentially blocking capability is available on the main thread, developers will call it there, degrading responsiveness—especially on low-powered devices used by disadvantaged users.

By withholding such APIs from `Window` entirely, the platform ensures that the path of least resistance for developers aligns with a smooth user experience. The principle cites the Web Audio API's replacement of main-thread `ScriptProcessorNode` with `AudioWorklet` as a concrete precedent, alongside modern examples like Origin Private File System's `FileSystemSyncAccessHandle` (`createSyncAccessHandle()`), which is only exposed in dedicated workers.

## Fit for Coding Agents

This principle cuts both ways for AI coding agents (`mixed`), reinforcing the behavioral need for a hard main-thread boundary while exposing sharp friction in how the web platform packages worker code.

On one hand, the principle's core premise—"developers will use an API in the simplest way it allows"—applies even more strongly to LLM coding agents, and the human DX cost of worker plumbing is lower for agents. Agents strongly favor single-file, inline code on the main thread to minimize context and orchestration overhead. Crucially, unlike a human developer who might notice UI stutter or audio glitches while manually testing an app, a coding agent verifying its work via unit tests or headless browser checks (e.g., Playwright DOM assertions) is blind to main-thread jank: as long as the functional output is correct, the test passes. If a blocking API is exposed on `Window`, an agent will almost always use it on the main thread and ship degraded UX. Restricting the API to `DedicatedWorkerGlobalScope` converts an unobservable non-functional regression (jank) into an immediate, loud `TypeError` (`... is not a function` on `Window`) in the agent's feedback loop. Furthermore, once forced into a worker, the traditional human complaint—that writing `postMessage` serialization, transferables, and request/response correlation IDs is tedious boilerplate—matters far less to an agent that can generate a typed worker RPC wrapper in seconds.

On the other hand, worker-only APIs routinely trip up coding agents because web workers and worklets require separate script URLs (`new Worker(new URL('./worker.js', import.meta.url))` or `audioWorklet.addModule('processor.js')`) rather than inline functions or self-contained modules. Splitting execution across files and global scopes introduces bundler-specific quirks (Vite vs. Webpack vs. plain ES modules), relative-path resolution bugs, MIME-type failures, and CSP errors when agents resort to `Blob` URL workarounds. The principle's own canonical example—replacing `ScriptProcessorNode` with `AudioWorklet`—is a notorious LLM footgun: because `ScriptProcessorNode` still exists on `Window` and works inline in a single file while `AudioWorklet` requires registering an external module URL, agents frequently gravitate toward the deprecated `ScriptProcessorNode` or produce broken `addModule()` paths in sandboxes and single-file prototypes.

## Value as a Slide Example

As a slide example for TPAC, this principle doesn't fit neatly into a binary "clearly helps agents" or "clearly hurts agents" bucket (`neither`, strength 3/5), because its primary purpose is protecting end-user rendering performance and its impact on agent ergonomics is double-edged.

However, it makes a compelling nuance or discussion point about how agent capabilities shift the DX trade-offs of worker-only APIs. Historically, spec authors hesitated to make APIs worker-only (like OPFS `createSyncAccessHandle()`) because human developers hated writing `postMessage` glue; agents absorb that boilerplate effortlessly and need the hard `Window` omission so their headless test loops fail loudly instead of silently shipping jank. At the same time, the `ScriptProcessorNode` vs. `AudioWorklet` example illustrates that if standards force agents off the main thread, the platform needs bundler-agnostic, single-file-friendly ways to define worker/worklet tasks rather than fragile external URL loading.
