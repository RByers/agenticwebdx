# CLAUDE.md

This repo holds the slides for a W3C TPAC 2026 breakout session (see README.md). The talk is developed interactively with the user.

## Workflow

- Pull requests are not used for this repo. Do not create PRs.
- Iterate on the session's working branch, committing locally as work progresses.
- Don't push the working branch to the remote unless the user explicitly asks for it.
- When the user says the work is complete, merge the branch into `main`, push `main`, and delete the local working branch.

## Layout

- The `web/` directory is served via GitHub Pages at https://rbyers.github.io/agenticwebdx/. Only files under `web/` are published.
- The deck is `web/index.html`. It uses the b6+ framework from the TPAC 2026 template.
- `web/Templates/` contains the unmodified TPAC 2026 template files. Don't edit them; put custom styles in the deck itself. `web/Templates/Overview.html` is the template's example deck and user manual: consult it for available slide classes and layouts (cover, part, final, two-column, etc.).
- Put any images or other assets for the slides in `web/` (or a subdirectory such as `web/images/`), not in `web/Templates/`.
