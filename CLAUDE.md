# CLAUDE.md

This repo holds the slides for a W3C TPAC 2026 breakout session (see README.md). The talk is developed interactively with the user.

## Workflow

- Pull requests are not used for this repo. Do not create PRs.
- Commit and push directly to the current branch only when the user indicates to (e.g. "commit", "push", "save this").

## Layout

- Files in `web/` are served at https://rbyers.github.io/agenticwebdx/.
- The deck is `web/index.html`. It uses the b6+ framework from the TPAC 2026 template.
- `web/Templates/` contains the unmodified TPAC 2026 template files. Don't edit them; put custom styles in the deck itself. `web/Templates/Overview.html` is the template's example deck and user manual: consult it for available slide classes and layouts (cover, part, final, two-column, etc.).
- Put any images or other assets for the slides in `web/`, not in `web/Templates/`.
