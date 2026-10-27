# Analysis notes

Research and analysis behind the deck, one Markdown file per topic. Each file holds the question, key findings, the data behind them, full sources with URLs, methodology, caveats and open threads. Slides point to their file with an `<!-- Analysis: … -->` comment before the slide's `<section>` and a link in its speaker notes.

These files are not published to GitHub Pages; the deck links to them on GitHub.

| File | Topic | Slides |
| --- | --- | --- |
| [`the-shift.md`](the-shift.md) | How far web development has shifted from human-led to agent-led | `#shift`, `#stackoverflow`, `#docs`, `#adoption`, `#code-share`, `#commits` |
| [`what-agents-write.md`](what-agents-write.md) | What agents actually write for the web (npm download trends) | `#what-agents-write` |
| [`volatility.md`](volatility.md) | Should we design for agents at all? Volatility vs. permanence | `#volatility` |
| [`token-efficiency.md`](token-efficiency.md) | Token efficiency of Web APIs | `#token-efficiency` |
| [`robustness.md`](robustness.md) | What makes a Web API robust (hard to misuse) for agents | `#robustness` |
| [`agent-sessions.md`](agent-sessions.md) | Where coding agents struggle with Web APIs, from real session transcripts | "Field notes" section |
| [`design-principles.md`](design-principles.md) | Which TAG design principles hold for agents (summary of [`../design-principles/`](../design-principles/)) | `#design-principles`, `#principle-text-formats` |
| [`agent-vs-human-dx.md`](agent-vs-human-dx.md) | Where agent and human DX conflict | `#conflicts` |
| [`evaluation.md`](evaluation.md) | Evaluating API designs under a delayed feedback loop | `#evaluation` |

Scripts that reproduce the data live in [`../tools/`](../tools/); the data itself is in [`../web/data/`](../web/data/).
