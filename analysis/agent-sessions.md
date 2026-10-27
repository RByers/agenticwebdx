# Where coding agents struggle with Web APIs: evidence from real sessions

*Research for the TPAC 2026 breakout "Agents are redefining DX. [How] should
web standards adapt?". Compiled 27 October 2026. The slides that use it are the
"Field notes" section of [`web/index.html`](../web/index.html):
`#flaky`, `#unclear-errors`, `#automation`, `#cant-see` and `#mobile`. It complements
[`robustness.md`](robustness.md) and [`token-efficiency.md`](token-efficiency.md)
with first-hand data rather than published studies.*

## Question

> When a coding agent builds a real web app, where does it make mistakes with
> Web APIs, and where does it burn an unexpectedly large number of tokens?
> How often does each kind of problem recur?

## Data and methodology

- **Projects.** Two hobby web apps built almost entirely by Claude Code agents, 27 Jul–23 Oct 2026:
  - **zpcrweb** (248 sessions): a browser app for a qPCR instrument, using WebUSB, the File System Access API, FileSystemObserver, IndexedDB, uPlot canvas charts, React, and a CDP-driven headless Chrome UI test suite.
  - **meshcore-web** (81 sessions): an installable PWA companion for MeshCore LoRa radios, using Web Bluetooth, Web Serial, WebCrypto, IndexedDB, Lit, and Vitest browser-mode tests.
- **Sessions.** All 329 non-empty sessions attached to these two repos, plus 4 unattached ones that clearly belong to them, read through the claude-code-remote MCP tools. Most are local CLI sessions synced via Remote Control. The user was usually directing several agents in parallel.
- **Pass 1, incident mining.** 17 subagents each read 20 full transcripts and recorded every incident where the agent either made a mistake with a web API or spent unusually heavily on one. Each record carries evidence quotes, a cost estimate, who discovered it, and a design lesson. Result: 167 incidents, 120 web-related and 47 non-web for contrast.
- **Pass 2, frequency.** The incidents were grouped into 14 patterns. A second round of subagents searched a flattened local corpus of 311 sessions for every occurrence of each pattern, confirming each keyword hit by reading the text around it. The other 18 sessions are small ones whose pages weren't saved; pass 1 found nothing relevant in them.
- **Data:**
  - [`web/data/agent-session-patterns.csv`](../web/data/agent-session-patterns.csv): per-pattern counts, costs and the list of sessions.
  - [`web/data/agent-session-incidents.csv`](../web/data/agent-session-incidents.csv): the 167 pass-1 incidents, without verbatim quotes.
  - [`tools/transcripts/`](../tools/transcripts/): the pipeline and the exact subagent prompts.
- **Sources.** Session IDs are cited as short prefixes, e.g. 016p7fHi = `session_016p7fHi…`. Full IDs are in the CSVs. The transcripts are private and not published.

### How much to trust these numbers

- **Small and unrepresentative sample.** This is one developer, two apps, one agent product and about three months. Both apps lean on device and storage APIs; neither is a typical content site.
- **Pattern-matching by LLM.** Agents chose what counts as an "episode", working from keyword search plus reading. Expect missed episodes and some arguable inclusions; most patterns are rated medium confidence.
- **Token figures are lower bounds.** They estimate transcript text (characters / 4) for the span of an episode. Real billed cost, which re-reads the cached context on every turn, is several times higher. Per-session usage metadata was unavailable for most sessions.
- **Subagent work is invisible.** Orchestrator sessions show only their subagents' final reports, so heavily delegated meshcore-web work is under-counted.
- **Not de-duplicated across patterns.** Patterns overlap: anchor positioning appears in P1, P8 and P10, and IndexedDB leaks appear in P6 and P7.
- **Not every cost is the API's fault.** Many episodes mix API design with agent judgement and the test harness. The "lesson" lines are hypotheses for discussion, not conclusions.

## Key findings

- **The largest cost is invisible async state, not wrong calls.** Flaky browser tests caused by state with no completion signal appear in **70 of 311 sessions**. 49 of those sessions dismissed the failure as "flaky" or "pre-existing" without finding the cause. The same race was waved off in up to 10 separate sessions.
- **Agents can't see what they built.** Separately from that, they wrote throwaway layout probes and screenshot loops in 30 sessions, about 0.7M tokens. All 24 user-reported CSS bugs were missed by the agent; where we can tell, 11 of 14 had already been "verified" by screenshot, measurement or tests.
- **Permission- and gesture-gated APIs (WebUSB, Web Bluetooth, File System Access, visibility) resist automation.** That produced 450–600+ lines of fake devices and stubs across 15 sessions. The fakes sometimes encoded a wrong model of the API, so tests passed on false beliefs.
- **Opaque errors and silent no-ops lead to guessing.**
  - In 13 opaque-error episodes the agent's first guess was wrong or never confirmed 7 times.
  - In one case, WebUSB's single `NetworkError` turned a guess into a retry policy the user kept hitting for a week.
  - 15 more episodes were silent no-ops, such as an invalid `min(1fr, …)` dropping a whole grid, or FileSystemObserver going quiet after an atomic save.
- **Agents' knowledge of new or gated features is shaky in both directions.**
  - They were confidently wrong about flags, as with Web Bluetooth `getDevices()`: 3 reversals and the wrong belief written into the README.
  - They avoided supported new features "for cross-browser reasons" in Chromium-only apps: anchor positioning, `popover="hint"` and `overflow-anchor`.
  - This fits [`evaluation.md`](evaluation.md)'s worry that evaluations favour the familiar.
- **Missing primitives lead to large hand-rolled workarounds:** a 300-line synchronous crypto library, three IndexedDB schema redesigns, and a 728-line PNG rasterizer that was later deleted.
- **Some platform behaviour is essentially untestable for an agent.** All 4 mobile-viewport and PWA bugs were found by the user on a real phone, and the agent never once enabled mobile or touch emulation.

All of these echo [`robustness.md`](robustness.md)'s headline that agents fix what fails loudly. The new part is how much token cost sits in what fails *quietly*, or *only on a device the agent can't drive*.

## Frequency at a glance

| # | Pattern | Episodes | Sessions | Who found it | Rough cost |
|---|---|---|---|---|---|
| P6 | Async browser state with no completion signal → flaky tests, often dismissed as "pre-existing flake" | **83** | **70** (23%) | tests 65, user 5 | ~845 min; 49 sessions dismissed it without finding a cause |
| P9 | The agent can't see layout → throwaway CDP measurement scripts and screenshot loops | 38 | 30 | user 17, agent 20 | ~1,180 tool calls, ~0.7M tokens (incl. 121 screenshots) |
| P10 | CSS bugs the user found that the agent's checks missed | 24 | 22 | **user 24/24** | ~850 tool calls, 2.7 h + 24 user round-trips; 79% of those with a known check had been "verified" |
| P3 | Permission- or activation-gated API that automation can't drive → fakes and mocks | 15 | 15 | agent 15 | 450–600+ lines of permanent fake code |
| P5 | Silent no-op: the platform accepts misuse with no error | 15 | 14 | agent 10, test 3, user 2 | ~200 tool calls, ~65 min |
| P8 | Missing platform primitive → hand-rolled replacement | 15 | 12 | agent 10, user 5 | ~900 tool calls, ~6.5 h, ~1,900 LOC (800 later deleted) |
| P1 | Stale or wrong belief about an API's availability (flag, default-on, Baseline) | 13 | 12 | agent 8, user 3 | ~270 tool calls, 9 web lookups, 7 probe scripts |
| P2 | Opaque error message → guessed diagnosis | 13 | 12 | user 6 | ~490 tool calls; first guess wrong or never confirmed in 7 of 13 |
| P4 | File System Access permission lifecycle | 11 | 10 | tests 7, user 3 | ~2–2.5 h, ~35 full test-suite runs |
| P14 | Event-model surprises (synthetic vs real input, same-document navigation) | 11 | 9 | user 5, test 5 | ~220 tool calls |
| P12 | WebUSB / Web Bluetooth transport semantics wrong | 10 | 8 | agent 6, user 4 | ~330 tool calls |
| P7 | IndexedDB origin-global state leaking between tests | 9 | 8 | tests 8 | ~75 min; 26 s added to every suite run until fixed |
| P11 | Mobile / installed-PWA behaviour that can't be verified headlessly | 4 | 3 | **user 4/4** | the agent never turned on touch or mobile emulation once |
| P13 | Canvas-rendered text invisible to DOM checks | 3 | 3 | test 2 | small |

---

## Examples

Candidate slide material, roughly in order of how strong the evidence is. Each entry gives what happened, how often, what it cost, a quote, and the API-design lesson it suggests.

Each entry gives what happened, how often it happens, what it cost, a quote, and the API-design lesson.

### 1. "It's a pre-existing flake": async state with no completion signal (P6, P7)
- **What happened:** browser UI tests waited on state that has no observable "done": an IndexedDB write committing, a dialog finishing rendering, a hash navigation settling, a popover finishing showing. The agent's usual response was to re-run the suite and call the failure pre-existing.
- **Frequency:** 83 episodes in **70 of 311 sessions**. 49 sessions dismissed it ("flaky", "pre-existing", "environmental") without finding a root cause, 19 found the cause, and 2 found the wrong cause.
- **Repeat offenders:** the same channel-details race was dismissed in **10 separate sessions**, and the hash deep-link race in 6.
- **Cost:** a dismissal took ~1 extra suite run and ~2.5 min. A root-cause hunt took ~7 runs, ~34 tool calls and ~14 min. Worst case: 51 min and 117 tool calls, then declared "environmental" (01Jww63r).
- **Quote (agent correcting itself):** "I said the Cq-filter test flakiness was pre-existing. It wasn't — it was mine. The `.pcrd`-threshold check I added yesterday left its run in IndexedDB…" (0199FRBg)
- **Sub-case, IndexedDB leaking between tests (P7, 9 episodes):** IndexedDB is per-origin and persists across tests. In zpcrweb, `deleteDatabase` was blocked by 25 open tabs, adding 26 s to every run. In meshcore-web, parallel test iframes deleted each other's databases.
- **Lesson:** async browser state needs an observable completion (promises or events for "committed", "rendered", "settled"). Storage needs a scoping or isolation primitive for tests.

### 2. Web Bluetooth `getDevices()`: three wrong theories in a row (P1)
- **What happened:** the agent believed `getDevices()` "only exists with the persistent-permissions flag" and wrote that into the commit message, the README, a test name and the mock (01EojErv). In the next session, after each user correction it produced a new wrong theory, reversing itself 3 times (016p7fHi).
- **Quotes:**
  - Agent: "in Chrome that function only exists with the persistent-permissions flag turned on."
  - User: "I have not turned on the flag but getDevices does exist."
- **Frequency:** P1 has 13 episodes in 12 sessions. This one cost ~110 tool calls across 3 sessions, plus a web search that only turned up 2020 sources.
- **Lesson:** API surface whose behaviour depends on flags and permission state is unknowable from documentation or training data. Agents need a reliable, queryable "is this enabled, and what's the permission lifetime?" answer.

### 3. Avoiding Baseline-uncertain features in a Chromium-only app (P1, P8)
- **What happened:** five times, the agent skipped a modern platform feature for cross-browser-support reasons and hand-built the old way instead:
  - anchor positioning, 3 times;
  - `popover="hint"` with `interestfor`, which the agent's own guidance lookup had recommended (015K4bNw);
  - native scroll anchoring (`overflow-anchor`).
- **Context:** both apps target only Chromium. A guidance skill's "no polyfill / no CDN" boilerplate pushed it further toward caution.
- **Quote:** "The guide's own note is that anchor positioning has no native support yet and needs a CDN polyfill — which this app can't use" (017ep63t). The hand-positioned menu then overflowed the viewport, and the user reported it.
- **Lesson:** this matches the session's "familiar beats better" evaluation question. Agents default to the older, well-represented pattern even when the newer one is right and supported.

### 4. WebUSB "A transfer error has occurred" became a retry policy (P2, P12)
- **What happened:** `transferIn` rejects with a generic `NetworkError`. The agent guessed it meant "stalled endpoint" and added 4 retries. In WebUSB a stall actually comes back as `status: 'stall'` and is cleared with `clearHalt`.
- **The chain:** the user kept hitting "transferIn error: Cancelled" for a week (014TW6Do → 01EAUs81 → 01Q29pfE). It ended with error classification done by regex over the exception name and message.
- **Quote:** "Chrome throws 'A transfer error has occurred' for a stalled/babbling endpoint as well as a genuine unplug…" (014TW6Do)
- **Frequency:** P2 has 13 episodes, 6 of them WebUSB. P12 has 10 episodes, ~330 tool calls in total; the worst single fix was 101 tool calls.
- **Lesson:** errors need machine-distinguishable causes (unplugged, stalled, cancelled, held by another context), not one exception type with prose.

### 5. Web Bluetooth: "User cancelled" when nothing was advertising (P2)
- **What happened:** the radio was paired to the user's phone and not advertising. `requestDevice()` rejected with NotFoundError "User cancelled the requestDevice() chooser.", and the app showed only "BLE connect failed". The agent built a CDP trace before the user worked out the real cause (01VoiDEJ).
- **Lesson:** an empty chooser and a deliberate cancel should be different errors.

### 6. File System Access: permissions that lapse on reload (P4, P2)
- **What happened:**
  - The agent assumed a saved directory handle stays granted after a reload. It comes back as `prompt`, so `#file=` deep links silently gave up (01G77vN7).
  - Then Chrome's raw NotAllowedError text showed up in the UI: "The request is not allowed by the user agent or the platform in the current context."
  - Then the agent wrongly assumed re-granting one folder covers only that folder; Chrome re-grants all of them (019TeUoW: 65 min, 101 tool calls, ~10 suite runs).
- **Root cause:** the agent's own earlier probe ran in one headless page with no reload, so it "confirmed" that permission persists.
- **Frequency:** 11 episodes in 10 sessions, ~2–2.5 h total.
- **Quote:** "A granted folder's permission comes back as `prompt` after almost every page load — which is exactly when a link arrives — and my first version treated that as 'not found' and silently gave up."
- **Lesson:** permission lifetime is invisible state. It needs to be documented, queryable and testable (for example, "simulate a reload / a permission lapse").

### 7. Permission-gated APIs can't be automated, so agents build fakes (P3)
- **What happened:** to test anything, agents built permanent fakes:
  - a fake `navigator.usb` replaying recorded instrument responses;
  - a ~300-line mock Bluetooth device, and a mock serial device;
  - an OPFS stand-in for `showDirectoryPicker`;
  - a patched `document.visibilityState`;
  - a fake WebAuthn authenticator.
- **Frequency:** 15 episodes in 15 sessions; 450–600+ lines of fake code, reused by at least 6 later sessions.
- **Problem:** some fakes encoded wrong permission models, so tests passed on wrong beliefs (see #2).
- **Bonus episode (0175YVYi):** typing into the page via CDP counted as user activation, so `requestDevice()` opened a chooser that headless Chrome never answers, and the connect *hung* instead of failing. The fix was a 6-second sleep to let activation expire.
- **Quote:** "The picker cannot be automated, so it is replaced. CDP intercepts `showDirectoryPicker` … but there is no command that can fulfil it with a directory."
- **Lesson:** every gated API needs a standard automation and test hook, as WebDriver offers for some permissions.

### 8. Silent no-ops (P5)
- **Frequency:** 15 episodes in 14 sessions, each looking like "nothing happens, and no error". Median cost is small (~3 min); a few were latent production bugs.
- **The most vivid ones:**
  - **`min(1fr, 19px)`:** `fr` isn't allowed in `min()`, so the whole `grid-template-columns` was dropped and a 96-cell grid collapsed to one 281px column. Found only with 4 throwaway measurement scripts (01MqbYxn).
  - **FileSystemObserver:** goes quiet after an editor's atomic save (delete + rename) unless re-armed (017K1NZU).
  - **`t?.click()` in tests:** silently did nothing when the tab hadn't rendered, a "latent flake across the whole suite" (01ABuvcs).
  - **ResizeObserver on a null ref:** the header stopped collapsing; found by the user, ~10 min and 35+ tool calls (019u6ezH).
  - **Smaller ones:** undefined `var()`, `blur()` on an unfocused element, `indexedDB.open()` silently creating a deleted database, and `a.download` turning "/" into "_".
- **Lesson:** robustness for agents means failing loudly. Invalid declarations, no-op calls and dead observers should be detectable (console warnings, an "invalid CSS" report, reportable errors).

### 9. The agent can't see layout (P9, P10)
- **Probing (P9):** 38 episodes in 30 sessions of throwaway CDP measurement scripts (often numbered: `zzmeasure`…`zzmeasure5`, `dbgwide1..5`, `anim1..6`) and screenshot→tweak→re-shoot loops: 71 probe calls and 121 screenshot reads, ~0.7M tokens.
- **Missed bugs (P10):** 24 CSS bugs were found by the user, never by the agent. In 11 of the 14 where we can tell, the agent had already "verified" the view by screenshot, measurement or tests. Recurring causes:
  - border-collapse tie rules;
  - `table-layout: auto` widening columns with 2-digit headers;
  - `flex: 1` meaning 0% basis;
  - sticky without a z-index;
  - an auto track combined with `aspect-ratio`;
  - test fixtures with names too short to wrap.
- **Quote:** "Measured rather than eyeballed, since 'looks fine in a screenshot' is how this slipped through in the first place." (017ep63t)
- **Lesson:** CSS has no way to ask "is anything overflowing or clipped, and why?" Agents need introspection such as layout warnings and explanations of computed sizes.

### 10. Breakpoint used as a proxy for "content doesn't fit" (P10)
- **What happened:** to collapse header labels, the agent used a fixed `max-width: 599px` media query and checked only 390px and desktop. The header actually overflows at ~780px, so it clipped in between.
- **Quote (user):** "today it gets 1/3rd truncated before collapsing".
- **Cost:** the fix took a whole follow-up session (~81 tool calls). Its 153-line JS fit-measuring hook then broke CSS transitions, which cost 6 more probe scripts (019WSwBm → 01FmGkzj).
- **Lesson:** there's no declarative "collapse when content overflows" primitive. Container queries come close, but neither the agent nor the platform offers "when I overflow".

### 11. WebCrypto is async-only, so a 300-line BigInt crypto twin (P8)
- **What happened:** a deterministic synchronous device emulator needed hashes and signatures. The agent measured "0 of 50 SHA-256 digests done by `setTimeout(0)`" and wrote `crypto-sync.ts`, ~300 lines of SHA-256/512, HMAC, Ed25519 and X25519 in BigInt (01PJZjFt).
- **Related gaps:** AES-ECB is missing. Ed25519 import accepts only a 32-byte seed, so keys exported from real firmware can't sign. Reactive UI code needs a separate synchronous SHA-256 (01Qczhzo).
- **Lesson:** async-only APIs have a real cost for agents building simulations and tests; a sync or worker variant would remove whole files.

### 12. IndexedDB: missing primitives and stale beliefs (P8, P1)
- **No partial update:** every read of a large record rewrote the whole thing (~45 MB written to append ~1 MB). That led to **three storage-schema redesigns** over two days; the worst session took 286 tool calls and ~2 h (01J2RAXJ, plus 012WmWHN and 0173T67n).
- **Stale belief:** in the same session the agent confidently claimed Chrome doesn't compress large IndexedDB values. The user challenged it, and Chrome's own blog post showed the claim was wrong.
- **No per-database size API:** the agent estimated size with a full cursor scan, since `navigator.storage.estimate()` is per-origin only (01JwcmNN).
- **Lesson:** missing primitives lead to large agent-written workarounds, and implementation details (compression, quotas) are easy to hallucinate.

### 13. Hand-rolled PNG rasterizer instead of using the browser (P8)
- **What happened:** for a PNG chart export, the agent wrote a software rasterizer, a PNG encoder and its own 5×7 pixel font: 728 lines over 78 tool calls. The user pushed back, and it was redone in 53 calls as a bundled chart screenshotted by headless Chrome (01HvAN6f).
- **Quote (user):** "much of the new 728 lines of code are because we refused to take a dependency on some existing software rasterizer/png encoder - that seems silly to reimplement ourselves."
- **Lesson:** this one is about agent judgement rather than the API, but it shows how much an agent will build when the platform path (canvas outside a page) isn't obvious.

### 14. Mobile viewport: every bug found by the user on a real phone (P11)
- **What happened:**
  - `100dvh` with `calc()` guesses still scrolled under Chrome's collapsing URL bar.
  - The agent's fix (`interactive-widget=resizes-content`) let the keyboard shrink the layout, so the user re-reported it 7 minutes later.
  - There's no API to detect that the keyboard is up, so "an input has focus" was used as a stand-in.
  - Missing `viewport-fit=cover` / safe-area insets, and no maskable icon.
- **Frequency:** 4 of 4 found by the user. In the whole corpus the agent never turned on touch or mobile emulation.
- **Quote:** "I haven't tried it on an Android phone, so that's the thing to check by hand."
- **Lesson:** mobile browser chrome behaviour is untestable headlessly and poorly specified, and there's no virtual-keyboard state API to observe.

### 15. Synthetic events lie (P14)
- **Frequency:** 11 episodes in 9 sessions. Tests that dispatch synthetic events pass or fail for reasons unrelated to real users.
- **Examples:**
  - A synthetic `mouseover` doesn't produce `mouseenter`.
  - A bare `dblclick` skips the click sequence.
  - A clipboard test passed even though a focused input would swallow the real shortcut.
- **Stand-out:** three "survives a reload" checks never actually reloaded, because navigating to the same URL with a new `#fragment` is a same-document navigation. They had passed for weeks (01Gyzu1y).
- **Lesson:** the event model's derived events and navigation types are subtle, and test tooling makes it easy to assert something that doesn't happen.

### 16. Smaller extras for a "rapid-fire" slide
- **Canvas text is invisible to the DOM** (P13, 3 episodes): DOM checks passed while the chart rendered in the wrong place, and only a screenshot caught it (01Uhk4ye).
- **WebUSB `open()` doesn't flush stale replies:** replies from a previous connection were read first, so every answer was one command behind, and the Identity panel showed "protocol garbage" (01GJrBMX; user-found, high severity).
- **Web Bluetooth `writeValueWithoutResponse`:** back-to-back writes merged into one corrupt frame. A reply timeout also started before the write resolved, so the OS pairing dialog caused a false "old firmware" result (01PJZjFt).
- **`popstate` and `hashchange` fire separately** for one hash navigation, and a render in between wrote stale state back. It took ~47 tool calls and 8 suite runs; 3 earlier sessions had called it flaky (01Gyzu1y).
- **WebAuthn:** the server-side origin check trusted the `Host` header, which a security-review subagent caught (01Qjt2xe).

---

## Positive counter-examples (for balance)
- The agent fetched modern-web-guidance on container queries and got the layout right first time (01D1KUTP).
- The agent knew a disabled `<button>` can't take the click that should focus a field, and used `aria-disabled` instead (018PPcvf).
- IntersectionObserver-based infinite scroll was implemented correctly first try (019yhrcx).

## Caveats (additional)
- Subagent transcripts launched from orchestrator sessions aren't visible; only their reports back are. Some large meshcore-web sessions are under-counted for this reason.
- `get_session` returned no usage data for most sessions, so per-session token totals are rough lower bounds from per-message usage.
- Pattern boundaries overlap: anchor positioning appears in P1, P8 and P10, and IndexedDB leaks in P6 and P7. Counts are per pattern, not de-duplicated across patterns.

## Open threads

- **Normalise by opportunity.** How many sessions used each API at all? We know 70 sessions had flaky tests, but not how many sessions ran browser tests. The `web_apis_used` field in pass-1 session records is a start.
- **Separate API-design cost from harness and agent-judgement cost** for the P6 flakes: how many root causes were app bugs, and how many were platform state with no completion signal?
- **Compare with a second agent or model generation** on the same tasks. Do the getDevices() and anchor-positioning beliefs persist?
- **Ask browser vendors** whether WebDriver BiDi or CDP hooks for permission prompts, device choosers, visibility and the virtual keyboard would have removed the fake layers in P3 and P11.
- **Check whether the same patterns show up in public agent transcripts** (open-source repos with committed agent logs), to get past n=1.

## Source audit (2026-10-27)

Slide numbers were re-checked against `web/data/agent-session-*.csv` and the examples above. Corrections:

- Flaky slide: "~10 h" is now "~9.5 h". The P6 total is ~845 min (~14 h), or ~570 min (~9.5 h) excluding session 01ABuvcs, which was a deliberate 4.6 h flake hunt the user asked for.
- Unclear-errors slide:
  - "4 sessions hit `A transfer error has occurred`" is now 3 sessions. The chain was 014TW6Do → 01EAUs81 → 01Q29pfE, and only the first saw that exact message; the later two saw `transferIn: Cancelled`.
  - The wrong `getDevices()` theory went into the README and *a* test name, not several test names.
  - The speaker note "first guess right in only 5" was inconsistent with "7 of 13 wrong or never confirmed". It now uses the latter.
- Automation slide: the 11 episodes / ~2 h (P4) cover the whole folder-permission lifecycle, not just the lapse on reload. The wording now says so.
- Mobile quote, in full (transcript 017nb1V6, 2026-10-18): "Typecheck is clean and all tests pass (1399 core, 262 web). I haven't tried it on an Android phone, so that's the thing to check by hand."
