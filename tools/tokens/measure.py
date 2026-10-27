#!/usr/bin/env python3
"""Count tokens in the equivalent web-platform snippets under snippets/.

Usage:
  python3 measure.py QWEN_TOKENIZER_JSON [--csv OUT.csv]

Prints a table and, with --csv, writes one row per snippet.
See README.md for setup.
"""
import argparse
import csv
import os
import sys

import tiktoken
from tokenizers import Tokenizer

HERE = os.path.dirname(os.path.abspath(__file__))
SNIPPETS = os.path.join(HERE, "snippets")

# (task, group, variant label, role, file)
# role: "old"/"new" for older vs newer platform pairs; "alt" otherwise.
ROWS = [
    ("Toggle a class", "platform-pair", "className string ops", "old", "toggle.old.js"),
    ("Toggle a class", "platform-pair", "classList.toggle()", "new", "toggle.new.js"),
    ("Lazy-load an image", "platform-pair", "IntersectionObserver + data-src", "old", "lazy.old.html"),
    ("Lazy-load an image", "platform-pair", "loading=lazy", "new", "lazy.new.html"),
    ("Remove an element", "platform-pair", "parentNode.removeChild()", "old", "remove.old.js"),
    ("Remove an element", "platform-pair", "remove()", "new", "remove.new.js"),
    ("Group an array", "platform-pair", "Array.reduce", "old", "groupby.old.js"),
    ("Group an array", "platform-pair", "Object.groupBy()", "new", "groupby.new.js"),
    ("Promise with external resolvers", "platform-pair", "new Promise + captured resolvers", "old", "resolvers.old.js"),
    ("Promise with external resolvers", "platform-pair", "Promise.withResolvers()", "new", "resolvers.new.js"),
    ("Fetch with timeout", "platform-pair", "AbortController + setTimeout", "old", "timeout.old.js"),
    ("Fetch with timeout", "platform-pair", "AbortSignal.timeout()", "new", "timeout.new.js"),
    ("Fetch JSON", "platform-pair", "XMLHttpRequest", "old", "fetch.old.js"),
    ("Fetch JSON", "platform-pair", "fetch + await (try/catch)", "new", "fetch.new.js"),
    ("Deep clone", "platform-pair", "JSON.parse(JSON.stringify())", "old", "clone.old.js"),
    ("Deep clone", "platform-pair", "structuredClone()", "new", "clone.new.js"),
    ("Scoped CSS rules (.card)", "platform-pair", "Repeated selectors", "old", "css.old.css"),
    ("Scoped CSS rules (.card)", "platform-pair", "CSS nesting", "new", "css.new.css"),
    ("Scoped CSS rules (.product-card)", "variant", "Repeated selectors", "old", "css2.old.css"),
    ("Scoped CSS rules (.product-card)", "variant", "CSS nesting", "new", "css2.new.css"),
    ("Counter component", "component", "Vanilla custom element", "alt", "counter.vanilla.js"),
    ("Counter component", "component", "Lit", "alt", "counter.lit.js"),
    ("Counter component", "component", "React", "alt", "counter.react.jsx"),
    ("Counter component", "component", "Svelte 5", "alt", "counter.svelte"),
    ("Add class to all matches", "library", "Platform (querySelectorAll + classList)", "alt", "addclass.platform.js"),
    ("Add class to all matches", "library", "jQuery", "alt", "addclass.jquery.js"),
    ("Delegated click handler", "library", "Platform (addEventListener + closest)", "alt", "delegate.platform.js"),
    ("Delegated click handler", "library", "jQuery", "alt", "delegate.jquery.js"),
    ("Append a link", "safety", "DOM (createElement + append)", "alt", "link.dom.js"),
    ("Append a link", "safety", "innerHTML += template (XSS-prone)", "alt", "link.innerhtml.js"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qwen_tokenizer")
    ap.add_argument("--csv")
    args = ap.parse_args()

    encs = {
        "o200k_base": tiktoken.get_encoding("o200k_base"),
        "cl100k_base": tiktoken.get_encoding("cl100k_base"),
    }
    qwen = Tokenizer.from_file(args.qwen_tokenizer)

    out = []
    for task, group, variant, role, fname in ROWS:
        # Trailing newline is stripped so counts reflect the code only.
        text = open(os.path.join(SNIPPETS, fname)).read().rstrip("\n")
        row = {
            "task": task, "group": group, "variant": variant, "role": role,
            "file": fname,
            "o200k_base": len(encs["o200k_base"].encode(text)),
            "cl100k_base": len(encs["cl100k_base"].encode(text)),
            "qwen2.5_coder": len(qwen.encode(text, add_special_tokens=False).ids),
            "chars": len(text),
        }
        out.append(row)
        print(f"{fname:22s} o200k={row['o200k_base']:4d} cl100k={row['cl100k_base']:4d} "
              f"qwen={row['qwen2.5_coder']:4d} chars={row['chars']:4d}  {task} / {variant}")

    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
            w.writeheader()
            w.writerows(out)


if __name__ == "__main__":
    sys.exit(main())
