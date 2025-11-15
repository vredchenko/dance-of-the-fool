# spastics-dance

Python toolkit for efficient PDF and EPUB book processing - chunking, splitting, and content extraction.

## Features

- **PDF Processing**: Split, chunk, and extract content from PDF files
- **EPUB Support**: Parse and extract content from EPUB ebooks
- **Memory Efficient**: Process large books page-by-page without loading entire files
- **Unicode Support**: Handles international text (tested with Ukrainian, Cyrillic)
- **Modular Dependencies**: Install only the tools you need

## Installation

```bash
# Install with PDF tools
pip install -e ".[pdf-tools]"

# Install with EPUB tools
pip install -e ".[epub-tools]"

# Install everything
pip install -e ".[all]"
```

## Quick Start

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
python3 demo_pdf_tools.py

# EPUB processing demo
python3 demo_epub_tools.py
```

## Translation Output Generation

This project includes scripts to generate translation outputs in multiple formats.

### Regenerate All Formats

To regenerate all translation outputs at once (webui data, PDF, and EPUB with/without uncertainties):

**Option 1: Using uv/pip scripts (recommended)**
```bash
# After installing the package with pip/uv
regenerate-all
```

**Option 2: Using the bash script**
```bash
# From project root
./regenerate-all.sh
```

**Option 3: Using Python directly**
```bash
python3 scripts/regenerate_all.py
```

This will generate:
- `webui/src/data/translation-data.json` - Data for the web UI
- `translation.pdf` - PDF without translator notes
- `translation-with-notes.pdf` - PDF with uncertainty annotations
- `translation.epub` - EPUB without translator notes
- `translation-with-notes.epub` - EPUB with uncertainty annotations

### Individual Format Generation

You can also run individual generators:

```bash
# Webui data only
python3 scripts/build-webui-data.py

# PDF without uncertainties
python3 scripts/generate-pdf.py --output translation.pdf

# PDF with uncertainties
python3 scripts/generate-pdf.py --output translation-with-notes.pdf --include-uncertainties

# EPUB without uncertainties
python3 scripts/generate-epub.py --output translation.epub

# EPUB with uncertainties
python3 scripts/generate-epub.py --output translation-with-notes.epub --include-uncertainties
```

## Dependency Groups

This project uses optional dependency groups:

- **pdf-tools**: PyMuPDF, pypdf, pdfplumber, pikepdf
- **epub-tools**: ebooklib, lxml
- **dev**: pytest, black, ruff, mypy
- **all**: All of the above

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
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Lint
ruff check .
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
