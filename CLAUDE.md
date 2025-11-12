# CLAUDE.md

> Project documentation for Claude Code and AI assistants working on this project

## Project Overview

**spastics-dance** is a Python toolkit for processing PDF and EPUB book files, with a focus on efficient chunking, splitting, and content extraction. The project was created to handle large book files (like the 468-page Ukrainian book "Танець недоумка" by Ілларіон Павлюк) in a memory-efficient way.

## Project Structure

```
spastics-dance/
├── pyproject.toml              # Project config with dependency groups
├── README.md                   # User-facing documentation
├── CLAUDE.md                   # This file - AI assistant notes
├── PDF_CHUNKING_RESEARCH.md   # Comprehensive PDF library research
├── PROPOSED_SKILLS.md         # Planned CLI skills/commands
├── demo_pdf_tools.py          # PyMuPDF demonstration
├── demo_epub_tools.py         # ebooklib demonstration
├── src/
│   └── spastics_dance/        # Main package (to be developed)
└── tests/                     # Test suite (to be developed)
```

## Technology Choices

### PDF Processing
**Primary: PyMuPDF (fitz)** - Selected for:
- Exceptional performance (C++ backend via MuPDF)
- Comprehensive feature set (text, images, rendering, annotations)
- Memory-efficient page-by-page processing
- Excellent Unicode support (critical for Ukrainian text)

**Secondary tools available:**
- `pypdf` - Pure Python, great for simple splitting
- `pdfplumber` - Best for table extraction and precise layout analysis
- `pikepdf` - Robust, can repair corrupted PDFs

### EPUB Processing
**ebooklib** - Chosen for:
- Clean Pythonic API
- Full EPUB 2 and 3 support
- Easy chapter extraction
- Metadata handling

**Why EPUB matters:**
- EPUB is an open format (ZIP + HTML + CSS + metadata)
- Easier to parse than PDF for structured content
- Natural chapter/section boundaries

## Dependency Groups

We use `uv` for dependency management with separate groups:

```bash
# PDF tools only
uv pip install -e ".[pdf-tools]"

# EPUB tools only
uv pip install -e ".[epub-tools]"

# Everything
uv pip install -e ".[all]"

# Development tools
uv pip install -e ".[dev]"
```

**Rationale for separation:**
- Users may only need PDF OR EPUB support
- Reduces dependency bloat
- Some dependencies (PyMuPDF) are larger (~20MB)
- Allows targeted installations in constrained environments

## Key Research Findings

### Performance Comparison (on 468-page test PDF)

| Tool | Load Time | Memory | Text Quality | Speed Rating |
|------|-----------|--------|--------------|--------------|
| PyMuPDF | Fast | Low | Excellent | ⚡⚡⚡⚡⚡ |
| pdfplumber | Slow | Medium | Excellent | ⚡⚡☆☆☆ |
| pypdf | Medium | Low | Good | ⚡⚡⚡☆☆ |
| pikepdf | Fast | Low | Good | ⚡⚡⚡⚡☆ |

### Memory Efficiency Pattern

For large PDFs, always use page-by-page iteration:

```python
# ✅ Good - memory efficient
import fitz
doc = fitz.open("large.pdf")
for page in doc:
    text = page.get_text()
    process(text)  # Process one page at a time

# ❌ Bad - loads all pages into memory
texts = [page.get_text() for page in doc]
```

## Planned Skills/Commands

See `PROPOSED_SKILLS.md` for full details. Priority order:

1. **pdf-split** - Split PDF into one-page files (most requested)
2. **pdf-chunk** - Memory-efficient page-by-page processing
3. **pdf-info** - Quick metadata viewer
4. **epub-info** - EPUB metadata and structure
5. **book-chunk** - Universal chunker for both formats

## Test Files

The repository includes test books in both formats:
- `pavlyuk_tanets_nedoumka_e27087_470337.pdf` (3.23 MB, 468 pages)
- `pavlyuk_tanets_nedoumka_e27087_470337.epub` (1.38 MB, 13 chapters)

**Important:** These are real books in Ukrainian, perfect for testing:
- Unicode handling (Cyrillic script)
- Large file processing (468 pages)
- Different format comparison (PDF vs EPUB)

## Development Guidelines

### Code Style
- Use `black` for formatting (configured in pyproject.toml)
- Use `ruff` for linting
- Type hints required (checked with `mypy`)

### Testing Strategy
- Test with both small and large PDFs
- Test Unicode text (use Ukrainian test files!)
- Memory profiling for large files
- Edge cases: encrypted PDFs, malformed files, empty pages

### Performance Targets
- Should handle 500+ page PDFs without memory issues
- Page-by-page processing should be near-constant memory
- Splitting 100 pages should take <5 seconds

## Common Patterns

### PDF Splitting Pattern
```python
import fitz

doc = fitz.open("input.pdf")
for i, page in enumerate(doc):
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=i, to_page=i)
    new_doc.save(f"page_{i+1}.pdf")
    new_doc.close()
doc.close()
```

### EPUB Chapter Iteration
```python
from ebooklib import epub, ITEM_DOCUMENT

book = epub.read_epub("input.epub")
for item in book.get_items_of_type(ITEM_DOCUMENT):
    content = item.get_content()
    # Process chapter
```

### Memory-Efficient Text Extraction
```python
import fitz

def extract_text_generator(pdf_path):
    """Yield text page by page without loading all into memory"""
    doc = fitz.open(pdf_path)
    for page in doc:
        yield page.get_text()
    doc.close()
```

## Known Issues & Gotchas

1. **PyMuPDF licensing**: AGPL for free version, commercial license available
   - Fine for open source and personal use
   - Consider if building commercial product

2. **Unicode in PDFs**: Some PDFs have encoding issues
   - PyMuPDF handles this best
   - Always test with non-English text

3. **Page numbers**: PDFs are 0-indexed in code but 1-indexed for users
   - Always clarify in user-facing messages
   - Example: "Page 1" means `doc[0]` in code

4. **EPUB structure varies**: Not all EPUBs have clear chapter boundaries
   - Some have 1 HTML file per chapter
   - Others split chapters across multiple files
   - Use TOC/NCX for reliable navigation

## Installation Quick Start

```bash
# Clone and enter directory
cd spastics-dance

# Install PDF tools (recommended to start)
uv pip install -e ".[pdf-tools]"

# Test installation
python3 demo_pdf_tools.py

# Install EPUB tools
uv pip install -e ".[epub-tools]"

# Test EPUB
python3 demo_epub_tools.py
```

## Git Workflow

- Main development branch: `main`
- Feature branches: `claude/feature-name-<session-id>`
- Always push to Claude branches first
- Create PRs for review before merging to main

## Resources

### Documentation
- PyMuPDF: https://pymupdf.readthedocs.io/
- ebooklib: https://github.com/aerkalov/ebooklib
- uv: https://github.com/astral-sh/uv

### Research Files
- `PDF_CHUNKING_RESEARCH.md` - Detailed tool comparison
- `PROPOSED_SKILLS.md` - Command specifications
- Demo files show working code

## Questions & Decisions Log

### Q: Why not use pdf2image?
A: Requires system-level Poppler installation, adds deployment complexity. PyMuPDF can render to images natively if needed.

### Q: Why separate dependency groups?
A: Users may only need PDF OR EPUB support. Some environments (containers, Lambda) benefit from minimal dependencies.

### Q: Why not use pdfminer.six directly?
A: pdfplumber provides better API on top of pdfminer.six. If we need low-level control, we can switch.

### Q: Should we support other ebook formats (MOBI, AZW)?
A: Future consideration. MOBI/AZW are proprietary Amazon formats, harder to parse. Start with open formats (PDF, EPUB).

## Notes for Future Development

1. **Claude Code Skills**: These tools are designed to be wrapped in Claude Code skills/commands
2. **MCP Server**: Consider building an MCP server for PDF/EPUB operations
3. **Streaming**: All tools should support streaming/generators for large files
4. **Progress bars**: Add `tqdm` for long operations (splitting large PDFs)
5. **Caching**: Consider caching extracted text for repeat operations

---

*Last updated: 2025-11-12*
*Project initialized with research on PDF/EPUB processing tools*
