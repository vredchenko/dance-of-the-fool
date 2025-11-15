# Tools

Utility scripts for processing and exporting translation data.

## Available Tools

### Data Aggregation

**`build-webui-data.py`**
- Aggregates translation chunks into structured JSON for the web UI
- Reads: `book/originals/chunks/chunk_*.json`, `book/translations/v1/translation_chunk_*.md`, `book/translations/v1/translation_chunk_*_uncertainty.md`
- Outputs: `webui/src/data/translation-data.json`
- Usage: `python3 tools/build-webui-data.py`
- Called automatically by `npm run dev` and `npm run build` in webui/

### PDF Export

**`generate-pdf.py`**
- Generates reader-friendly PDF from English translation
- Removes chunk/page structure for natural book flow
- Options:
  - `--output <path>` - Output file path (default: `dist/translation.pdf`)
  - `--include-uncertainties` - Include translator notes
- Usage:
  ```bash
  python3 tools/generate-pdf.py --output dist/translation.pdf
  python3 tools/generate-pdf.py --output dist/translation-with-notes.pdf --include-uncertainties
  ```
- Requires: `reportlab>=4.0.0`
- Output: Letter-size PDF (1.1 MB clean, 1.2 MB with notes)

### EPUB Export

**`generate-epub.py`**
- Generates reader-friendly EPUB e-book from English translation
- Organizes 39 chunks into 6 natural chapters
- Options:
  - `--output <path>` - Output file path (default: `dist/translation.epub`)
  - `--include-uncertainties` - Include translator notes
- Usage:
  ```bash
  python3 tools/generate-epub.py --output dist/translation.epub
  python3 tools/generate-epub.py --output dist/translation-with-notes.epub --include-uncertainties
  ```
- Requires: `ebooklib>=0.18`
- Output: EPUB 3 format (369K clean, 397K with notes)

## Quick Start

Install dependencies:

```bash
# All export tools
pip install -e ".[export-tools]"

# Or individually
pip install reportlab ebooklib
```

Generate all formats:

```bash
# Using the regeneration script (recommended)
python3 tools/regenerate_all.py
# or
./regenerate-all.sh

# Or individually:
# Clean versions
python3 tools/generate-pdf.py --output dist/translation.pdf
python3 tools/generate-epub.py --output dist/translation.epub

# With translator notes
python3 tools/generate-pdf.py --output dist/translation-with-notes.pdf --include-uncertainties
python3 tools/generate-epub.py --output dist/translation-with-notes.epub --include-uncertainties
```

## Additional Tools

**`regenerate_all.py`**
- Regenerates all output formats in one go
- Runs build-webui-data, generate-pdf (both versions), and generate-epub (both versions)
- Available as CLI command: `regenerate-all` (after installing with pip/uv)

**`extract-cover.py`**
- Extracts page 1 from the PDF as a high-quality PNG for webui background

**`normalize-markdown.py`**
- Normalizes all translation markdown files to consistent format

**`normalize-ukrainian-linebreaks.py`**
- Normalizes line breaks in Ukrainian text chunks (removes PDF layout artifacts)

## See Also

- `../pyproject.toml` - Dependency definitions
- `../README.md` - Main project documentation
