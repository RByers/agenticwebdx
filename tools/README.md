# Tools

Scripts that fetch, measure or chart the data behind the slides, plus the deck's slide-fit check. Data they produce goes in [`../web/data/`](../web/data/) so the published deck can link to it. Each script's header comment gives its exact usage; the analysis file listed explains how the output is used.

| Script | What it does | Output | Analysis |
| --- | --- | --- | --- |
| [`check-slide-fit.js`](check-slide-fit.js) | Fails if any slide in `web/index.html` overflows the 16:9 slide size (uses Playwright and [`../web/slide-fit.js`](../web/slide-fit.js)). Run after editing slides: `node tools/check-slide-fit.js` | exit status | – |
| [`so_fetch.py`](so_fetch.py) | Monthly new-question counts from the Stack Exchange API | `web/data/stackoverflow-questions.csv` | [`the-shift.md`](../analysis/the-shift.md) |
| [`so_chart.py`](so_chart.py) | Renders the Stack Overflow CSV as the deck's inline SVG chart | SVG on stdout | [`the-shift.md`](../analysis/the-shift.md) |
| [`botcommits_chart.py`](botcommits_chart.py) | Renders AI-attributed commits as a share of GitHub push events (from botcommits.dev) as an inline SVG chart | SVG on stdout; data in `web/data/ai-commit-share.csv` | [`the-shift.md`](../analysis/the-shift.md) |
| [`npm_downloads.py`](npm_downloads.py) | Monthly npm download counts for frameworks, UI libraries and baselines | `web/data/npm-downloads.csv` | [`what-agents-write.md`](../analysis/what-agents-write.md) |
| [`chromestatus_fetch.py`](chromestatus_fetch.py) | Every feature entry from the chromestatus.com API | `web/data/chromestatus-features.csv` | [`volatility.md`](../analysis/volatility.md), [`robustness.md`](../analysis/robustness.md) |

## Subdirectories

- [`tokens/`](tokens/) – token counts for equivalent web-platform snippets and common API identifiers ([`token-efficiency.md`](../analysis/token-efficiency.md))
- [`transcripts/`](transcripts/) – pipeline for mining Claude Code session transcripts for Web API misuse ([`agent-sessions.md`](../analysis/agent-sessions.md))
