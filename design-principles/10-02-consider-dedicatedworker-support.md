---
section: "10.2"
id: "consider-dedicatedworker-support"
title: "Where possible APIs should be made available to dedicated workers"
chapter: "10. Other API Design Considerations"
url: "https://w3ctag.github.io/design-principles/#consider-dedicatedworker-support"
agent_fit: "good"
slide_example: "neither"
example_strength: 2
verdict: "Helps coding agents by preserving global API symmetry across main-thread and worker contexts and avoiding multi-file postMessage proxy boilerplate, though it is primarily a runtime concurrency principle rather than a headline agentic DX example."
---

# §10.2 Where possible APIs should be made available to dedicated workers

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=good | §10.2 consider-dedicatedworker-support — Where possible APIs should be made available to dedicated workers: Helps coding agents by preserving global API symmetry across main-thread and worker contexts and avoiding multi-file postMessage proxy boilerplate, though it is primarily a runtime concurrency principle rather than a headline agentic DX example.

- **URL:** https://w3ctag.github.io/design-principles/#consider-dedicatedworker-support
- **Chapter:** 10. Other API Design Considerations
- **Agent-Fit:** good
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Helps coding agents by preserving global API symmetry across main-thread and worker contexts and avoiding multi-file postMessage proxy boilerplate, though it is primarily a runtime concurrency principle rather than a headline agentic DX example.

## Principle Summary

W3C TAG Design Principle §10.2 (`consider-dedicatedworker-support`) recommends that specification authors expose new web platform features on `DedicatedWorkerGlobalScope` whenever possible, rather than limiting them to `Window`. Many APIs do not inherently depend on the DOM, and omitting them from dedicated workers prevents developers from running compute- or I/O-heavy code off the main thread in a non-blocking manner.

The principle acknowledges that features requiring user interaction—such as permission requests, file pickers, or device selectors—pose challenges for dedicated workers. However, it urges spec authors to still design such features with dedicated worker support in mind from the start, avoiding main-thread-only assumptions that would make exposing or transferring those capabilities to workers unnecessarily difficult later.

## Fit for Coding Agents

This principle is a good fit for AI coding agents because LLM training priors strongly assume uniform API availability across JavaScript execution contexts (`globalThis`). When a developer or performance tool asks an agent to offload heavy work into a Web Worker, the agent typically extracts the logic or imports shared utility modules directly into the worker file. When platform APIs (`fetch`, `crypto.subtle`, `CompressionStream`, `OffscreenCanvas`, `WebCodecs`, `WebGPU`, `IndexedDB`, or Origin Private File System handles) are exposed symmetrically on `DedicatedWorkerGlobalScope`, the agent's refactored code works out of the box without context-specific rewrites.

When an API is arbitrarily restricted to `Window`, coding agents hit two common failure modes. First, unless the project has separate, strictly configured TypeScript `lib: ["WebWorker"]` build targets for worker files, agents frequently assume main-thread globals exist in workers and produce code that fails only at runtime with a `ReferenceError` or `TypeError`. Second, working around a missing worker API forces the agent to synthesize custom, multi-file `postMessage` RPC bridge boilerplate—complete with request correlation IDs, pending-promise registries, error serialization, and `Transferable` handling. Although agents can type out boilerplate quickly, asynchronous cross-context state machines are a frequent source of subtle agent bugs (leaked listeners, swallowed errors, `DataCloneError` exceptions) and consume unnecessary context tokens.

Even for features that genuinely require main-thread UI interaction—such as permission prompts or pickers like `showOpenFilePicker()`—designing with dedicated workers in mind (e.g., making the resulting handles such as `FileSystemFileHandle`, `OffscreenCanvas`, or `MediaStreamTrack` structured-cloneable or transferable to workers) gives agents a clean, explicit boundary between UI acquisition on the main thread and non-blocking processing in the worker.

## Value as a Slide Example

As a slide example for a W3C TPAC session on how web standards should adapt to coding agents, this principle is relatively weak (2/5, `neither`). Its primary rationale is runtime execution architecture—allowing web applications to perform computation and I/O off the main thread without blocking UI rendering—rather than developer or agent authoring ergonomics.

Additionally, to the extent that missing worker APIs require `postMessage` proxy boilerplate when performance isn't bottlenecked by main-thread round-trips, LLMs actually find writing repetitive message-passing glue less tedious than humans do, even if native worker support is much cleaner and avoids cross-context hallucinations. At most, this principle serves as a minor supporting example of why consistent API availability across `globalThis` scopes (`Window`, `WorkerGlobalScope`, and server/edge JS runtimes) helps agents avoid environment-mismatch bugs.
