# Token-count snippets

Hand-written, equivalent code snippets that [`../measure.py`](../measure.py) tokenizes to produce [`web/data/token-counts.csv`](../../../web/data/token-counts.csv). See [`../README.md`](../README.md) for how to run it and the style rules every snippet follows, and [`analysis/token-efficiency.md`](../../../analysis/token-efficiency.md) for the results.

Files are named `<task>.<variant>.<ext>`:

- `*.old.*` / `*.new.*` – the same task with an older vs. newer platform API (e.g. `fetch.old.js` uses XHR, `fetch.new.js` uses `fetch`).
- Other variants are named by approach, e.g. `counter.react.jsx` / `counter.svelte` / `counter.lit.js` / `counter.vanilla.js`, or `delegate.jquery.js` / `delegate.platform.js`.

Every file in a task group does the same job, so token counts are comparable. `measure.py` lists the snippet files it reads explicitly, so a new snippet must be added there too.
