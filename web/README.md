# web/

Everything in this directory is published to GitHub Pages at https://rbyers.github.io/agenticwebdx/ by [`../.github/workflows/static.yml`](../.github/workflows/static.yml) on pushes to `main`.

- [`index.html`](index.html) – the slide deck, built with the b6+ framework from the TPAC 2026 template
- [`slide-fit.js`](slide-fit.js) – runs when the deck loads and outlines in red any slide that overflows the fixed 16:9 size (also used by [`../tools/check-slide-fit.js`](../tools/check-slide-fit.js))
- `.nojekyll` – tells GitHub Pages to serve files as-is, without Jekyll processing
- [`Templates/`](Templates/) – the unmodified TPAC 2026 slide template files
- [`data/`](data/) – CSV data behind the slides, so the deck can link to it
- [`images/`](images/) – images and icons used by the deck
