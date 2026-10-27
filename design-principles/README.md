# W3C TAG Web Platform Design Principles — Agent DX Audit

Each file in this directory evaluates one of the 103 numbered principles in the [W3C TAG Web Platform Design Principles](https://w3ctag.github.io/design-principles/) in isolation for AI coding agents.

## Greppable Format

Every principle file (`XX-YY-*.md`) includes YAML frontmatter, a single-line `GREP_SUMMARY:` line, and standardized bullet metadata:

- `agent_fit`: `good` | `mixed` | `poor` | `neutral`
- `slide_example`: `clearly-useful` | `clearly-harmful` | `neither`
- `example_strength`: `1` to `5` (`5/5` = strongest candidate for the TPAC slide deck)

### Example `grep` Queries

List all principles rated as strong examples that apply well to agents (`clearly-useful`, strength `5/5` or `4/5`):

```sh
  grep -h "^GREP_SUMMARY: slide_example=clearly-useful | strength=[45]/5" design-principles/*.md | sort -t'|' -k2,2r
```

List all principles rated as examples where the guideline or its human-author assumptions likely don't apply to or pull against agent-written code (`clearly-harmful`):

```sh
  grep -h "^GREP_SUMMARY: slide_example=clearly-harmful" design-principles/*.md | sort -t'|' -k2,2r
```

Count principles by `agent_fit` or `slide_example`:

```sh
  grep -h "^agent_fit:" design-principles/*.md | sort | uniq -c
  grep -h "^slide_example:" design-principles/*.md | sort | uniq -c
```
