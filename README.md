# The Dance of the Fool — English translation

[![Latest release](https://img.shields.io/github/v/release/vredchenko/dance-of-the-fool?label=release)](https://github.com/vredchenko/dance-of-the-fool/releases/latest)
[![Read online](https://img.shields.io/badge/read-online-blue)](https://vredchenko.github.io/dance-of-the-fool/)
[![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-6366f1?logo=claude)](https://claude.ai/code)

An unofficial, non-commercial English fan translation of the Ukrainian science-fiction
novel **_Танець недоумка_ ("The Dance of the Fool")** by **Ілларіон Павлюк (Illarion Pavliuk)**,
together with the open-source tooling used to produce it — a PDF/EPUB processing pipeline
and a web reader for proofreading the translation.

<p align="center">
  <img src="webui/public/book-cover.png" alt="Cover of «Танець недоумка» (The Dance of the Fool) by Illarion Pavliuk" width="300">
  <br>
  <em>Original cover art © The Old Lion Publishing House.</em>
</p>

<p align="center">
  <strong>📖 <a href="https://vredchenko.github.io/dance-of-the-fool/">Read it online →</a></strong>
  <br>
  <em>The web reader is published to GitHub Pages at <a href="https://vredchenko.github.io/dance-of-the-fool/">vredchenko.github.io/dance-of-the-fool</a>.</em>
</p>

> [!IMPORTANT]
> **This is a fan translation, published for non-commercial and educational purposes.**
> It is **not** authorized by or affiliated with the author or the original publisher.
> See [Copyright & Attribution](#copyright--attribution) below before reading, reusing,
> or redistributing anything in this repository.

---

## About the book

- **Title:** _Танець недоумка_ ("The Dance of the Fool")
- **Author:** Ілларіон Павлюк (Illarion Pavliuk)
- **Original publisher:** Видавництво Старого Лева (The Old Lion Publishing House), 2019
- **ISBN:** 978-617-679-720-3
- **Genre:** Science fiction / psychological thriller (~468 pages)

Space biologist Gil — a veteran of many off-world military operations — takes a job on a
scientific expedition to the distant, strange planet Ix-Chel, hoping it will solve all his
problems at once. It doesn't.

## What's in this repository

This repo has two halves that grew together:

1. **The translation** (`book/`) — the source text chunked for translation, the English
   translation itself (39 chunks), and per-chunk *uncertainty notes* recording ambiguous
   passages and the reasoning behind translation choices.
2. **The tooling** (`src/`, `tools/`, `webui/`) — a small Python toolkit for chunking and
   extracting text from PDF/EPUB books, a build pipeline that renders the translation into
   PDF/EPUB/web outputs, and an [Astro](https://astro.build) web app for reading and
   proofreading the result side by side with the original.

## Reading the translation

The translation lives as Markdown in `book/translations/v1/` and can be rendered into:

- **PDF** — clean, or with translator's uncertainty notes
- **EPUB** — clean, or with translator's uncertainty notes
- **Web** — a browsable reader (the `webui/` Astro app), published live at
  **[vredchenko.github.io/dance-of-the-fool](https://vredchenko.github.io/dance-of-the-fool/)**

### Download the latest release

Prebuilt files are attached to every [GitHub Release](https://github.com/vredchenko/dance-of-the-fool/releases/latest).
These links always point at the newest build:

- [PDF](https://github.com/vredchenko/dance-of-the-fool/releases/latest/download/dance-of-the-fool.pdf)
  · [PDF with notes](https://github.com/vredchenko/dance-of-the-fool/releases/latest/download/dance-of-the-fool-annotated.pdf)
- [EPUB](https://github.com/vredchenko/dance-of-the-fool/releases/latest/download/dance-of-the-fool.epub)
  · [EPUB with notes](https://github.com/vredchenko/dance-of-the-fool/releases/latest/download/dance-of-the-fool-annotated.epub)
- [Web reader bundle (.zip)](https://github.com/vredchenko/dance-of-the-fool/releases/latest/download/dance-of-the-fool-web.zip)

Releases are versioned `X.Y.Z` (book · website · other) and published
automatically from a `vX.Y.Z` tag — see [`docs/VERSIONING.md`](docs/VERSIONING.md).

See [Building the outputs](#building-the-outputs) to generate them locally.

## Repository layout

```
dance-of-the-fool/
├── book/
│   ├── originals/                  # Source book + extracted text chunks (see Copyright)
│   │   ├── *.pdf, *.epub
│   │   └── chunks/                 # Ukrainian text extracted as JSON
│   └── translations/v1/            # English translation + uncertainty notes (Markdown)
│       ├── original_chunk_NN.md
│       ├── translation_chunk_NN.md
│       └── translation_chunk_NN_uncertainty.md
├── src/spastics_dance/             # PDF/EPUB toolkit (pdf-info/split/chunk, epub-*)
├── tools/                          # Build pipeline: PDF/EPUB/webui generators
├── webui/                          # Astro web reader (proofreading UI)
├── .github/workflows/              # CI to build outputs
├── dist/                           # Generated PDFs/EPUBs (gitignored)
└── pyproject.toml                  # uv-managed Python project
```

## Setup

The Python side uses [`uv`](https://github.com/astral-sh/uv):

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install everything (creates .venv automatically)
uv sync --all-extras
```

Selective installs are available via extras — `pdf-tools`, `epub-tools`, `export-tools`,
`dev` — e.g. `uv sync --extra pdf-tools`.

## Building the outputs

Regenerate every format at once (web data, PDFs, EPUBs, with and without notes):

```bash
uv run regenerate-all
```

Or generate individual formats:

```bash
# Web reader data (derived from the Markdown translation)
uv run python3 tools/build-webui-data.py

# PDF — clean, or with uncertainty notes
uv run python3 tools/generate-pdf.py  --output dist/translation.pdf
uv run python3 tools/generate-pdf.py  --output dist/translation-with-notes.pdf  --include-uncertainties

# EPUB — clean, or with uncertainty notes
uv run python3 tools/generate-epub.py --output dist/translation.epub
uv run python3 tools/generate-epub.py --output dist/translation-with-notes.epub --include-uncertainties
```

Generated outputs land in `dist/` (gitignored). The source of truth is always the Markdown
in `book/translations/v1/` — regenerate after editing it.

## Web reader (development)

```bash
cd webui
npm install
npm run dev        # if translation-data.json already exists
npm run dev:full   # regenerates data first, then serves
npm run build      # production build (regenerates data via prebuild hook)
```

`webui/src/data/translation-data.json` is generated from the Markdown translation and is
not tracked in git.

## The PDF/EPUB toolkit

The translation pipeline is built on a reusable toolkit for splitting, chunking, and
extracting text from large books memory-efficiently (page-by-page, so 500+ page PDFs stay
near-constant memory). It exposes CLI commands:

```bash
pdf-info <file.pdf>            # metadata
pdf-split <file.pdf>           # split into per-page PDFs
pdf-chunk <file.pdf> ...       # extract page ranges as text/JSON
epub-info / epub-split / epub-chunk   # EPUB equivalents
```

It uses **PyMuPDF** (fast C++ backend, strong Unicode support — important for Cyrillic),
with `pypdf`, `pdfplumber`, and `pikepdf` available for specific tasks, and `ebooklib`
for EPUB. See [`docs/PDF_CHUNKING_RESEARCH.md`](docs/PDF_CHUNKING_RESEARCH.md) for the tool comparison
that informed these choices.

## Development

```bash
uv sync --extra dev
uv run pytest              # tests
uv run black .             # format
uv run ruff check .        # lint
uv run mypy .              # type-check
```

## Copyright & Attribution

The original novel **_Танець недоумка_ is © Ілларіон Павлюк** and its publisher,
**Видавництво Старого Лева (The Old Lion Publishing House)**. All rights to the original
work belong to them.

This repository contains an **unofficial, fan-made English translation** created and shared
on a **non-commercial basis** for readers who cannot access the work in Ukrainian. It is
**not endorsed by, affiliated with, or licensed by** the author or publisher. The English
translation is a derivative work; no rights in the underlying novel are claimed or granted.

**If you are the rights holder** and would like the original text, this translation, or any
part of this repository amended or removed, please open an issue or contact the maintainer —
requests will be honored promptly.

### Source of the original text

The Ukrainian source files under `book/originals/` are:

- `pavlyuk_tanets_nedoumka_e27087_470337.pdf` (3.23 MB, 468 pages)
- `pavlyuk_tanets_nedoumka_e27087_470337.epub` (1.38 MB) — a Calibre conversion of a
  FictionBook (FB2) edition; embedded metadata records **ISBN 978-617-679-720-3**,
  publisher **Видавництво Старого Лева**.

Downloaded from: [uabook.com.ua/book/tanets-nedoumka](https://uabook.com.ua/book/tanets-nedoumka/)

If you enjoy the story, please **support the author** by buying the original book:
[Старий Лев](https://starylev.com.ua/tanec-nedoumka) ·
[Yakaboo](https://www.yakaboo.ua/ua/tanec-nedoumka.html) ·
[Goodreads](https://www.goodreads.com/book/show/49447405).

### Code license

The **software** in this repository (the toolkit in `src/`, the build pipeline in `tools/`,
and the `webui/` app) is separate from the book content and is offered under the MIT
License (see [`LICENSE-CODE`](LICENSE-CODE)). The book text and its translation are **not**
covered by that license — see above.

## Credits

- Original novel: **Ілларіон Павлюк** — buy it, it's good.
- Translation, tooling, and web reader: this project's maintainer, with development
  assistance from Claude Code.
