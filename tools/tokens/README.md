# Token counts for web-platform snippets

Reproduces the token counts in [`analysis/token-efficiency.md`](../../analysis/token-efficiency.md)
and the `token-efficiency` slide.

- `snippets/`: hand-written equivalent snippets, one file per variant
  (`*.old.*` vs `*.new.*` for older vs newer platform APIs; other pairs are
  named by approach, e.g. `counter.react.jsx`, `delegate.jquery.js`).
- `measure.py`: counts tokens in every snippet → [`web/data/token-counts.csv`](../../web/data/token-counts.csv).
- `identifiers.py`: tokenizes common web API identifiers (bare, as `.member`, and
  in short code contexts) → [`web/data/identifier-tokens.csv`](../../web/data/identifier-tokens.csv).

## Requirements

Python 3 (tested with 3.13), plus:

```sh
pip install tiktoken==0.14.0 tokenizers==0.23.3
# Qwen2.5-Coder tokenizer (7 MB; not checked in). Measured at repo
# revision c03e6d358207e414f1eca0bb1891e29f1db0e242.
curl -L -o /tmp/qwen-tokenizer.json \
  https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct/resolve/c03e6d358207e414f1eca0bb1891e29f1db0e242/tokenizer.json
```

`tiktoken` downloads the `o200k_base` and `cl100k_base` encodings on first use.

## Run

From the repo root:

```sh
python3 tools/tokens/measure.py /tmp/qwen-tokenizer.json --csv web/data/token-counts.csv
python3 tools/tokens/identifiers.py /tmp/qwen-tokenizer.json --csv web/data/identifier-tokens.csv
```

Each snippet's trailing newline is stripped before counting; nothing else is
normalized, so indentation and quotes count. No BOS/EOS or chat-template
tokens are added.

## Snippet style rules

To keep pairs comparable, all snippets follow one style: 2-space indent,
single quotes in JS, semicolons, no comments, short realistic names
(`el`, `res`, `items`), and the same placeholder functions (`render`,
`showError`, `removeItem`) on both sides of a pair. Each pair does the same
job, including equivalent error handling where relevant (e.g. the XHR
version handles HTTP errors and network errors; the fetch version uses
try/catch for both).
