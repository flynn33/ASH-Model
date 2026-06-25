# Research Paper Guide

The repository contains both a GitHub-readable manuscript and LaTeX source.

| File | Role |
|---|---|
| `docs/ASH-research-paper.md` | Markdown research narrative |
| `latex/main.tex` | publication-oriented LaTeX source |
| `docs/ASH-Model-Preprint-v1.pdf` | committed PDF |
| `proofs/manuscript-manifest.json` | source-input and PDF hash binding |

## Manuscript policy

The manuscript manifest uses source-input equivalence. It records hashes for:

- LaTeX source;
- bibliography files;
- tracked figure inputs;
- committed PDF bytes.

Run:

```bash
python tools/build_manuscript.py
python tools/verify_repository.py
```

Use `--build-pdf` only when the local environment has `pdflatex` and the PDF itself is intentionally being rebuilt.
