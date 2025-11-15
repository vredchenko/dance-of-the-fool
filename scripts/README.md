# Scripts

Utility scripts for processing and exporting translation data.

## Available Scripts

### Data Aggregation

**`build-webui-data.py`**
- Aggregates translation chunks into structured JSON for the web UI
- Reads: `chunk_*.json`, `translation_chunk_*.md`, `translation_chunk_*_uncertainty.md`
- Outputs: `webui/src/data/translation-data.json`
- Usage: `python3 scripts/build-webui-data.py`
- Called automatically by `npm run dev` and `npm run build` in webui/

### PDF Export

**`generate-pdf.py`**
- Generates PDF from English translation
- Options:
  - `--output <path>` - Output file path (default: `translation_english.pdf`)
  - `--include-uncertainties` - Include translator notes
- Usage:
  ```bash
  python3 scripts/generate-pdf.py
  python3 scripts/generate-pdf.py --include-uncertainties
  ```
- Requires: `reportlab>=4.0.0`
- Output: Letter-size PDF (~140-150KB)

### EPUB Export

**`generate-epub.py`**
- Generates EPUB e-book from English translation
- Options:
  - `--output <path>` - Output file path (default: `translation_english.epub`)
  - `--include-uncertainties` - Include translator notes
- Usage:
  ```bash
  python3 scripts/generate-epub.py
  python3 scripts/generate-epub.py --include-uncertainties
  ```
- Requires: `ebooklib>=0.18`
- Output: EPUB 3 format (~70KB)

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
# Clean versions
python3 scripts/generate-pdf.py
python3 scripts/generate-epub.py

# With translator notes
python3 scripts/generate-pdf.py --include-uncertainties
python3 scripts/generate-epub.py --include-uncertainties
```

## See Also

- `../TRANSLATION_EXPORT.md` - Detailed export documentation
- `../WEBUI_SETUP.md` - Web UI setup guide
- `../pyproject.toml` - Dependency definitions
