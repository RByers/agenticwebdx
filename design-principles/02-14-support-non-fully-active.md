---
section: "2.14"
id: "support-non-fully-active"
title: "Support non-fully active BFCached documents"
chapter: "2. API Design Across Languages"
url: "https://w3ctag.github.io/design-principles/#support-non-fully-active"
agent_fit: "neutral"
slide_example: "neither"
example_strength: 2
verdict: "Primarily a spec-completeness and browser lifecycle rule for defining BFCache behavior, though platform-managed BFCache support helps coding agents that rarely write or test pagehide/pageshow lifecycle logic."
---

# §2.14 Support non-fully active BFCached documents

GREP_SUMMARY: slide_example=neither | strength=2/5 | agent_fit=neutral | §2.14 support-non-fully-active — Support non-fully active BFCached documents: Primarily a spec-completeness and browser lifecycle rule for defining BFCache behavior, though platform-managed BFCache support helps coding agents that rarely write or test pagehide/pageshow lifecycle logic.

- **URL:** https://w3ctag.github.io/design-principles/#support-non-fully-active
- **Chapter:** 2. API Design Across Languages
- **Agent-Fit:** neutral
- **Slide-Example:** neither
- **Example-Strength:** 2/5
- **Verdict:** Primarily a spec-completeness and browser lifecycle rule for defining BFCache behavior, though platform-managed BFCache support helps coding agents that rarely write or test pagehide/pageshow lifecycle logic.

## Principle Summary

W3C TAG Design Principle §2.14 instructs specification authors to explicitly define how their features behave when a document is kept in a "non-fully active" state inside the browser's Back/Forward Cache (BFCache) after navigation, as well as when it is later restored. It highlights three risk areas: features that interact with a document from the outside (such as sending messages or events), features that share resources across documents (such as holding locks or database connections), and features whose saved document state may malfunction if it spans multiple navigations instead of being destroyed.

This principle exists because historically many web specifications assumed a document was either actively running or permanently unloaded on navigation. As browsers introduced BFCache to make back/forward navigations instant for end users, underspecified features either caused subtle bugs and cross-tab deadlocks when frozen or forced browsers to conservatively disqualify any page using those APIs from BFCache altogether.

## Fit for Coding Agents

At its core, §2.14 is neutral with respect to AI coding agents because it is a specification-completeness checklist item directed at spec editors and browser implementers ("Specify how your feature behaves in non-fully active BFCached documents"), governing internal browser navigation caching and document-lifecycle state transitions rather than the surface ergonomics of JavaScript APIs.

However, the underlying problem it addresses—how web features behave when a document is frozen in the Back/Forward Cache (BFCache) and later restored—interacts strongly with the blind spots of LLM coding agents. Coding agents have strong statistical priors toward simple load-to-unload page lifecycles or SPA component mount/unmount cycles; unless explicitly prompted, they almost never proactively write `pagehide` or `pageshow` (`event.persisted`) handlers to clean up cross-document resources or refresh stale state after BFCache restoration. Even more importantly, an agent's automated verification loop (such as unit tests or linear Playwright/Puppeteer test flows) almost never exercises back/forward navigation across BFCache states or checks whether a frozen document holds a resource that deadlocks another tab.

Therefore, how spec authors fulfill §2.14 matters for agent-written code. When specifications support BFCache transparently in the browser (for example, by automatically queuing or coalescing outside events while frozen, or cleanly managing resource handles without disqualifying the page from BFCache), the platform absorbs lifecycle edge cases that agents routinely miss. Conversely, when an API requires developers to manually tear down connections or release locks on `pagehide` to avoid either cross-tab deadlocks (e.g., `navigator.locks`, open `IndexedDB` version-change blocks) or silent BFCache disqualification, agent-generated applications will systematically omit that glue code—and because silent BFCache eviction throws no runtime error, the agent's feedback loop will never catch it.

## Value as a Slide Example

§2.14 is a weak candidate for a standalone TPAC slide (`neither`, 2/5) because the principle itself is phrased as a procedural reminder for spec editors ("Specify how your feature behaves... following the guidelines in the Supporting BFCached Documents guide") rather than prescribing a concrete developer-facing API pattern. Putting it on a slide would require explaining internal browser document states ("non-fully active") before getting to the agent DX point.

If mentioned at all, its best use is as a secondary example under a broader theme of "invisible failure modes in agent feedback loops": APIs that require manual `pagehide`/`pageshow` (`event.persisted`) ceremony to remain BFCache-eligible (or to avoid holding onto `WebSocket`, `IndexedDB`, or `Web Locks` resources across navigations) fail silently in agent-written code because standard headless browser test runs neither trigger BFCache restoration nor fail when a page is silently evicted from BFCache.
