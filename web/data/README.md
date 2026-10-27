# Slide data

Data behind the slides, published with the deck so slides can link to it. Each file is produced by a script in [`../../tools/`](../../tools/) (or captured as described in its analysis file), and is explained in the linked analysis file.

| File | Contents | Produced by | Analysis |
| --- | --- | --- | --- |
| [`stackoverflow-questions.csv`](stackoverflow-questions.csv) | Monthly new Stack Overflow questions: all, `[javascript]`, `[css]` | `tools/so_fetch.py` | [`the-shift.md`](../../analysis/the-shift.md) |
| [`ai-commit-share.csv`](ai-commit-share.csv) | Monthly AI-attributed commits as a share of public GitHub push events (from botcommits.dev) | see analysis | [`the-shift.md`](../../analysis/the-shift.md) |
| [`npm-downloads.csv`](npm-downloads.csv) | Monthly npm downloads per package, Sep 2023 – Sep 2026 | `tools/npm_downloads.py` | [`what-agents-write.md`](../../analysis/what-agents-write.md) |
| [`chromestatus-features.csv`](chromestatus-features.csv) | Every chromestatus.com feature entry (type, status, milestone, spec link) | `tools/chromestatus_fetch.py` | [`volatility.md`](../../analysis/volatility.md), [`robustness.md`](../../analysis/robustness.md) |
| [`token-counts.csv`](token-counts.csv) | Token counts of equivalent snippets under three tokenizers | `tools/tokens/measure.py` | [`token-efficiency.md`](../../analysis/token-efficiency.md) |
| [`identifier-tokens.csv`](identifier-tokens.csv) | Token counts of common web API identifiers | `tools/tokens/identifiers.py` | [`token-efficiency.md`](../../analysis/token-efficiency.md) |
| [`agent-session-incidents.csv`](agent-session-incidents.csv) | One row per Web API problem found in real coding-agent sessions | `tools/transcripts/to_csv.py` | [`agent-sessions.md`](../../analysis/agent-sessions.md) |
| [`agent-session-patterns.csv`](agent-session-patterns.csv) | Those incidents grouped into patterns, with frequency and cost | `tools/transcripts/to_csv.py` | [`agent-sessions.md`](../../analysis/agent-sessions.md) |
