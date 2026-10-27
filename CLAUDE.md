# CLAUDE.md

This repo holds the slides for a W3C TPAC 2026 breakout session (see README.md). The talk is developed interactively with the user.

## Workflow

- Pull requests are not used for this repo. Do not create PRs.
- In a local checkout (initially on `main`), create a git worktree per task (`git worktree add -b <task-branch> .worktrees/<task-name> main`) so concurrent sessions don't collide. In Claude Code on the web (cloud), worktrees are unnecessary since each session already runs in its own isolated container on a dedicated session branch.
- Iterate on the working branch, committing locally as work progresses.
- Don't push the working branch itself to the remote.
- When a piece of work is complete, commit it, merge the working branch into `main`, and push `main` without waiting to be asked. If there are unanswered questions to confirm with the user first, ask them and wait instead of pushing.
- Once the work is pushed to `main`, remove any worktree and delete the local working branch (and its remote copy, if one exists).

## Layout

- The `web/` directory is served via GitHub Pages at https://rbyers.github.io/agenticwebdx/. Only files under `web/` are published, by the `.github/workflows/static.yml` Actions workflow on pushes to `main`.
- The deck is `web/index.html`. It uses the b6+ framework from the TPAC 2026 template.
- `web/Templates/` contains the unmodified TPAC 2026 template files. Don't edit them; put custom styles in the deck itself. `web/Templates/Overview.html` is the template's example deck and user manual: consult it for available slide classes and layouts (cover, part, final, two-column, etc.).
- Put any images or other assets for the slides in `web/` (or a subdirectory such as `web/images/`), not in `web/Templates/`.
