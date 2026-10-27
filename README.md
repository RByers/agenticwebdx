# Agents are redefining DX. [How] should web standards adapt?

Slides for the W3C TPAC 2026 breakout session
[Agents are redefining DX. [How] should web standards adapt?](https://www.w3.org/events/meetings/8371a85c-bb6e-413c-b84e-e41ef38d8089/).

- **Date:** 28 October 2026, 15:15–16:15 GMT
- **Location:** Ground Floor – Ulster Suite
- **Proposers:** Rick Byers, Lea Verou
- **Session proposal:** [w3c/tpac2026-breakouts#56](https://github.com/w3c/tpac2026-breakouts/issues/56)
- **Slides:** https://rbyers.github.io/agenticwebdx/

## Session description

The Web Platform's design principles implicitly assume a human developer as the primary API consumer. As a growing share of web code is written by agents, these assumptions stop holding uniformly, and some pull in opposite directions.

Questions this session will explore:

- Should we take agent consumers into account at all? The counterarguments are that agents are not uniform — what is efficient for one model generation may not be for the next — and the landscape is still volatile, whereas Web APIs are permanent.
- What does agent DX mean? Token efficiency? Robustness/correctness? What else?
- Which existing design principles still hold for agents, and which actively hinder them?
- What makes a Web API token-efficient, both when writing code against it and when reading code that uses it?
- What makes a Web API robust for agents, i.e. harder to misuse?
- Where agent ergonomics and human DX conflict, how do we weigh them?
- **Evaluation:** An API's token cost is not an intrinsic property. An agent implementing an unfamiliar API spends tokens on lookup, trial and error, and correction, so a design that would be more token-efficient at parity of familiarity measures as worse until training data catches up — which takes years. Any evaluation we run today privileges familiar over better. How do we separate the two, and how do we evaluate API designs, or design principles, given such a delayed feedback loop?

**Goal:** Make progress on the questions above and identify people interested in exploring this further.

## Repository layout

- `web/index.html` – the slide deck (b6+ framework, TPAC 2026 template)
- `web/Templates/` – the unmodified [TPAC 2026 slide template](https://www.w3.org/2026/Talks/TPAC/Templates/) files. `web/Templates/Overview.html` is the template's example deck and user manual.

Everything under `web/` is published at https://rbyers.github.io/agenticwebdx/.
