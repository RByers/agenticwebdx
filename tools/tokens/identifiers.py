#!/usr/bin/env python3
"""Tokenize common web API identifiers, bare and in code context.

Usage:
  python3 identifiers.py QWEN_TOKENIZER_JSON [--csv OUT.csv]
"""
import argparse
import csv

import tiktoken
from tokenizers import Tokenizer

IDENTIFIERS = """document fetch querySelector querySelectorAll getElementById getElementsByClassName
addEventListener removeEventListener preventDefault stopPropagation classList textContent innerHTML
appendChild createElement setAttribute requestAnimationFrame setTimeout XMLHttpRequest localStorage
customElements attachShadow shadowRoot connectedCallback attributeChangedCallback observedAttributes
adoptedStyleSheets CSSStyleSheet replaceSync IntersectionObserver ResizeObserver MutationObserver
structuredClone AbortSignal withResolvers groupBy toggleAttribute replaceChildren showModal showPopover
popovertarget scrollIntoView startViewTransition getBoundingClientRect ElementInternals attachInternals
setFormValue formAssociated CSSNumericValue computedStyleMap PerformanceObserver""".split()

CONTEXTS = [
    "el.addEventListener(",
    "document.getElementById(",
    "document.getElementsByClassName(",
    '<button popovertarget="menu">',
    "this.shadowRoot.adoptedStyleSheets = [sheet];",
    "el.remove()",
    "el.classList.toggle('open')",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qwen_tokenizer")
    ap.add_argument("--csv")
    args = ap.parse_args()
    o = tiktoken.get_encoding("o200k_base")
    c = tiktoken.get_encoding("cl100k_base")
    q = Tokenizer.from_file(args.qwen_tokenizer)

    def split(enc, s):
        return "|".join(enc.decode([t]) for t in enc.encode(s))

    rows = []
    for kind, items in (("identifier", IDENTIFIERS), ("member", ["." + i for i in IDENTIFIERS]),
                        ("context", CONTEXTS)):
        for s in items:
            r = {"kind": kind, "text": s, "chars": len(s),
                 "o200k_base": len(o.encode(s)), "cl100k_base": len(c.encode(s)),
                 "qwen2.5_coder": len(q.encode(s, add_special_tokens=False).ids),
                 "o200k_split": split(o, s), "cl100k_split": split(c, s)}
            rows.append(r)
            print(f"{kind:10s} {s:46s} o200k={r['o200k_base']} cl100k={r['cl100k_base']} "
                  f"qwen={r['qwen2.5_coder']}  [{r['o200k_split']}]  [{r['cl100k_split']}]")
    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)


if __name__ == "__main__":
    main()
