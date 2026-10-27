---
section: "6.14"
id: "async-by-default"
title: "If you need both asynchronous and synchronous methods, synchronous is the exception"
chapter: "6. Designing JavaScript APIs"
url: "https://w3ctag.github.io/design-principles/#async-by-default"
agent_fit: "good"
slide_example: "clearly-useful"
example_strength: 3
verdict: "Making asynchronous methods the unmarked default and marking blocking variants with a Sync() suffix aligns with LLM naming priors, prevents missing-await bugs, and keeps default agent-generated code off the main-thread blocking path."
---

# §6.14 If you need both asynchronous and synchronous methods, synchronous is the exception

GREP_SUMMARY: slide_example=clearly-useful | strength=3/5 | agent_fit=good | §6.14 async-by-default — If you need both asynchronous and synchronous methods, synchronous is the exception: Making asynchronous methods the unmarked default and marking blocking variants with a Sync() suffix aligns with LLM naming priors, prevents missing-await bugs, and keeps default agent-generated code off the main-thread blocking path.

- **URL:** https://w3ctag.github.io/design-principles/#async-by-default
- **Chapter:** 6. Designing JavaScript APIs
- **Agent-Fit:** good
- **Slide-Example:** clearly-useful
- **Example-Strength:** 3/5
- **Verdict:** Making asynchronous methods the unmarked default and marking blocking variants with a Sync() suffix aligns with LLM naming priors, prevents missing-await bugs, and keeps default agent-generated code off the main-thread blocking path.

## Principle Summary

This principle states that in the rare cases where a web platform API must provide both asynchronous and synchronous methods for the same operation, the asynchronous method should be the unmarked default and the synchronous variant should be treated as an exception named with a `Sync()` suffix. It also recommends having a clear deprecation path for the synchronous methods as web platform capabilities evolve to support asynchronous execution everywhere.

For human developers and browser engines, this principle exists to protect main-thread responsiveness and user experience by steering authors toward non-blocking operations by default. Naming blocking variants with an explicit `Sync()` suffix makes main-thread performance hazards and Worker-only restrictions immediately obvious during authoring and code review, avoiding legacy footguns like `XMLHttpRequest.open(method, url, false)` where a boolean flag silently changes execution semantics.

## Fit for Coding Agents

This principle is a good fit for AI coding agents because it encodes execution semantics and return-type shape directly into method names. LLMs rely heavily on lexical conventions learned from massive JavaScript and TypeScript corpora (such as Node.js `fs.readFile` vs. `fs.readFileSync` or `crypto.scrypt` vs. `crypto.scryptSync`). When an API follows the `foo()` (returns a `Promise`) vs. `fooSync()` (returns a direct value synchronously) convention, the token stream itself tells the model whether to emit `await` and how to type the return value. In contrast, APIs that toggle synchronous behavior via a configuration flag or boolean argument (like `xhr.open(method, url, async)`) or invert the naming convention frequently cause agents to hallucinate `await` on synchronous return values, omit `await` on promises, or confuse static type narrowing.

Furthermore, making the shorter, unmarked base name asynchronous aligns with how LLMs sample default completions. Unless specifically prompted to write high-throughput synchronous code inside a Dedicated Worker, an agent reaching for the canonical method name will naturally generate non-blocking code that is safe on the main thread, rather than accidentally emitting a Worker-only synchronous call in a `Window` context and triggering runtime exceptions.

The only part of the principle that pulls slightly against coding agents is the suggestion to introduce synchronous methods as temporary stopgaps with a plan to deprecate them as platform capabilities evolve. Because LLMs suffer from training-data inertia, temporary `Sync()` methods remain in model weights long after specifications deprecate them, causing agents to continue proposing obsolete calls. Nonetheless, the core rule—async by default with an explicit `Sync()` suffix for exceptions—strongly supports reliable agent code generation.

## Value as a Slide Example

This principle is a clearly-useful supporting example (3/5) for a TPAC slide on how predictable lexical conventions help coding agents. Contrasting the legacy boolean-flag antipattern (`xhr.open('GET', url, false)`) with explicit `Sync()` suffixing (`readSync()` vs. `read()`) provides an intuitive visual example of why LLMs perform better when control-flow (`await` vs. blocking) and return-type differences (`Promise<T>` vs. `T`) are encoded in the method identifier rather than hidden in positional arguments.

It merits a 3/5 rather than a top-tier 5/5 score because the principle explicitly applies only to the "rare case" where a web API needs both synchronous and asynchronous variants, making it narrower than cross-cutting principles that govern every API on the platform. It is best used as a supporting bullet in a slide about naming consistency and aligning Web API conventions with JavaScript/Node.js statistical priors.
