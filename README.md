# The Dance of the Fool — English translation

An unofficial, non-commercial English fan translation of the Ukrainian science-fiction
novel **_Танець недоумка_ ("The Dance of the Fool")** by **Ілларіон Павлюк (Illarion Pavliuk)**,
together with the open-source tooling used to produce it — a PDF/EPUB processing pipeline
and a web reader for proofreading the translation.

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
- **Web** — a browsable reader (the `webui/` Astro app)

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
