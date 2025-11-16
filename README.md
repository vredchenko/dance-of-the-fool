# spastics-dance

Python toolkit for efficient PDF and EPUB book processing - chunking, splitting, and content extraction.

## Features

- **PDF Processing**: Split, chunk, and extract content from PDF files
- **EPUB Support**: Parse and extract content from EPUB ebooks
- **Memory Efficient**: Process large books page-by-page without loading entire files
- **Unicode Support**: Handles international text (tested with Ukrainian, Cyrillic)
- **Modular Dependencies**: Install only the tools you need

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable dependency management.

### Quick Start

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and sync all dependencies (creates .venv automatically)
uv sync --all-extras
```

### Selective Installation

```bash
# Install with PDF tools only
uv sync --extra pdf-tools

# Install with EPUB tools only
uv sync --extra epub-tools

# Install with export tools only
uv sync --extra export-tools

# Install everything (all extras)
uv sync --all-extras

# Development tools
uv sync --extra dev
```

### Alternative: Using pip

If you prefer pip:

```bash
pip install -e ".[all]"
```

## Quick Start

All examples below assume you've run `uv sync --all-extras` to set up the environment.

### PDF Splitting

```python
import fitz  # PyMuPDF

doc = fitz.open("book.pdf")
for i, page in enumerate(doc):
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=i, to_page=i)
    new_doc.save(f"page_{i+1}.pdf")
    new_doc.close()
doc.close()
```

Run with: `uv run python3 your_script.py`

### Page-by-Page Processing

```python
import fitz

doc = fitz.open("book.pdf")
for page_num, page in enumerate(doc):
    text = page.get_text()
    print(f"Page {page_num + 1}: {len(text)} characters")
doc.close()
```

### EPUB Chapter Extraction

```python
from ebooklib import epub, ITEM_DOCUMENT

book = epub.read_epub("book.epub")
for item in book.get_items_of_type(ITEM_DOCUMENT):
    content = item.get_content().decode('utf-8')
    # Process chapter content
```

## Demo Scripts

Try the included demos:

```bash
# PDF processing demo
uv run python3 demo_pdf_tools.py

# EPUB processing demo
uv run python3 demo_epub_tools.py
```

## Translation Output Generation

This project includes scripts to generate translation outputs in multiple formats.

### Regenerate All Formats

To regenerate all translation outputs at once (webui data, PDF, and EPUB with/without uncertainties):

**Option 1: Using uv (recommended)**
```bash
uv run regenerate-all
```

**Option 2: Using the bash script**
```bash
./regenerate-all.sh
```

**Option 3: Using Python directly**
```bash
uv run python3 tools/regenerate_all.py
```

This will generate:
- `webui/src/data/translation-data.json` - Data for the web UI
- `dist/translation.pdf` - PDF without translator notes
- `dist/translation-with-notes.pdf` - PDF with uncertainty annotations
- `dist/translation.epub` - EPUB without translator notes
- `dist/translation-with-notes.epub` - EPUB with uncertainty annotations

### Individual Format Generation

You can also run individual generators:

```bash
# Webui data only
uv run python3 tools/build-webui-data.py

# PDF without uncertainties
uv run python3 tools/generate-pdf.py --output dist/translation.pdf

# PDF with uncertainties
uv run python3 tools/generate-pdf.py --output dist/translation-with-notes.pdf --include-uncertainties

# EPUB without uncertainties
uv run python3 tools/generate-epub.py --output dist/translation.epub

# EPUB with uncertainties
uv run python3 tools/generate-epub.py --output dist/translation-with-notes.epub --include-uncertainties
```

## Local Development - WebUI

The translation proofreading web interface lives in the `webui/` directory.

### First Time Setup

```bash
cd webui
npm install
```

### Running the WebUI Locally

The WebUI reads from `webui/src/data/translation-data.json`, which is **generated** from the markdown translation files. This file is not tracked in git.

**Option 1: Quick start (if data already exists)**
```bash
cd webui
npm run dev
```

**Option 2: Full rebuild (regenerates data first)**
```bash
cd webui
npm run dev:full
```

Or manually:
```bash
uv run python3 tools/build-webui-data.py
cd webui
npm run dev
```

### Building for Production

```bash
cd webui
npm run build  # Automatically regenerates data via prebuild hook
```

The build output will be in `webui/dist/`.

**Note:** The translation data file (`webui/src/data/translation-data.json`) is derived from the source of truth (markdown files in `book/translations/v1/`). Always regenerate it after updating translation files.

## Dependency Management

This project uses [uv](https://github.com/astral-sh/uv) for dependency management, providing:
- ⚡ **10-100x faster** installs than pip
- 🔒 **Lock file** (`uv.lock`) for reproducible builds
- 🐍 **Python version management** (`.python-version`)
- 📦 **Optional dependency groups** for modular installs

### Dependency Groups

- **pdf-tools**: PyMuPDF, pypdf, pdfplumber, pikepdf
- **epub-tools**: ebooklib, lxml
- **export-tools**: reportlab, ebooklib
- **dev**: pytest, black, ruff, mypy, coverage
- **all**: All of the above

### Why uv?

- **Speed**: Rust-based implementation is dramatically faster
- **Reliability**: Lock files ensure everyone gets the same versions
- **Modern**: Follows latest Python packaging standards (PEP 621)
- **Convenience**: Manages Python versions and virtualenvs automatically

## Technology

- **PyMuPDF** (primary): Fast C++ backend, excellent Unicode support
- **pypdf**: Pure Python PDF manipulation
- **pdfplumber**: Advanced text/table extraction
- **pikepdf**: PDF repair and manipulation
- **ebooklib**: EPUB reading and writing

See [PDF_CHUNKING_RESEARCH.md](PDF_CHUNKING_RESEARCH.md) for detailed tool comparison.

## Development

```bash
# Install with dev tools
uv sync --extra dev

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov

# Format code
uv run black .

# Lint
uv run ruff check .

# Type check
uv run mypy .
```

### Adding Dependencies

```bash
# Add a new dependency
uv add package-name

# Add to a specific group
uv add --group dev package-name

# Update all dependencies
uv lock --upgrade
```

## Documentation

- [CLAUDE.md](CLAUDE.md) - Technical notes and development guide
- [PDF_CHUNKING_RESEARCH.md](PDF_CHUNKING_RESEARCH.md) - Library research and comparison
- [PROPOSED_SKILLS.md](PROPOSED_SKILLS.md) - Planned CLI commands

## Test Files

Includes test books in both formats:
- Ukrainian novel (468 pages PDF, 13 chapters EPUB)
- Perfect for testing large file handling and Unicode support

## License

TBD

## Credits

Research and development assisted by Claude Code.
