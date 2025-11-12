# PDF Chunking Tools Research

## Overview
Research on tools for loading PDFs page-by-page or splitting into one-page PDFs.

## Top Tools

### 1. **pypdf** (formerly PyPDF2) - Best for splitting
- **Status**: Actively maintained, successor to PyPDF2
- **GitHub**: https://github.com/py-pdf/pypdf
- **Install**: `pip install pypdf`
- **Strengths**:
  - Pure Python, no external dependencies
  - Excellent for splitting PDFs into single pages
  - Can merge, rotate, crop pages
  - Good metadata handling
- **Use Cases**:
  - Split PDF into one-page files
  - Extract specific page ranges
  - Merge PDFs back together
- **Example**:
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        output.write(writer)
```

### 2. **PyMuPDF (fitz)** - Best for performance & features
- **Status**: Very actively maintained
- **GitHub**: https://github.com/pymupdf/PyMuPDF
- **Install**: `pip install PyMuPDF`
- **Strengths**:
  - VERY fast (C++ backend via MuPDF)
  - Rich feature set (text, images, annotations, forms)
  - Can render pages to images
  - Excellent text extraction with positioning
  - Can chunk/load page by page efficiently
- **Use Cases**:
  - Large PDFs that need fast processing
  - Extract text with layout information
  - Convert pages to images
  - Page-by-page streaming
- **Example**:
```python
import fitz  # PyMuPDF

doc = fitz.open("input.pdf")
for page_num in range(len(doc)):
    page = doc[page_num]
    # Get text
    text = page.get_text()
    # Or save as separate PDF
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
    new_doc.save(f"page_{page_num+1}.pdf")
    new_doc.close()
doc.close()
```

### 3. **pdfplumber** - Best for text extraction & tables
- **Status**: Actively maintained
- **GitHub**: https://github.com/jsvine/pdfplumber
- **Install**: `pip install pdfplumber`
- **Strengths**:
  - Built on pdfminer.six
  - Excellent table detection and extraction
  - Detailed character-level positioning
  - Page-by-page iteration
  - Visual debugging (can draw boxes on pages)
- **Use Cases**:
  - Extract tables from PDFs
  - Precise text extraction with coordinates
  - Analyzing PDF structure
  - Page-by-page text processing
- **Example**:
```python
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        tables = page.extract_tables()
        # Process each page individually
        print(f"Page {i+1}: {len(text)} chars")
```

### 4. **pdf2image** - Convert pages to images
- **Status**: Maintained
- **GitHub**: https://github.com/Belval/pdf2image
- **Install**: `pip install pdf2image` (requires poppler)
- **Strengths**:
  - Convert PDF pages to PIL Images
  - Page-by-page or bulk conversion
  - Control DPI, format, thread count
- **Use Cases**:
  - OCR preprocessing
  - Visual analysis of PDFs
  - Creating thumbnails
- **Example**:
```python
from pdf2image import convert_from_path

# One page at a time (memory efficient)
for i, image in enumerate(convert_from_path("input.pdf")):
    image.save(f"page_{i+1}.png", "PNG")
```

### 5. **pikepdf** - Advanced PDF manipulation
- **Status**: Very actively maintained
- **GitHub**: https://github.com/pikepdf/pikepdf
- **Install**: `pip install pikepdf`
- **Strengths**:
  - Based on QPDF (C++ library)
  - Can repair broken PDFs
  - Full PDF specification support
  - Pythonic API
  - Excellent for splitting/merging
- **Use Cases**:
  - Robust PDF splitting
  - Fixing corrupted PDFs
  - Advanced PDF manipulation
- **Example**:
```python
import pikepdf

pdf = pikepdf.open("input.pdf")
for i, page in enumerate(pdf.pages):
    new_pdf = pikepdf.new()
    new_pdf.pages.append(page)
    new_pdf.save(f"page_{i+1}.pdf")
```

## Comparison Table

| Tool | Speed | Splitting | Page-by-page | Text Extract | Images | Dependencies |
|------|-------|-----------|--------------|--------------|--------|--------------|
| pypdf | Medium | ★★★★★ | ★★★★☆ | ★★☆☆☆ | ☆☆☆☆☆ | None (Pure Python) |
| PyMuPDF | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | MuPDF (bundled) |
| pdfplumber | Slow | ★★☆☆☆ | ★★★★★ | ★★★★★ | ★★★☆☆ | pdfminer.six |
| pdf2image | Medium | ☆☆☆☆☆ | ★★★★★ | ☆☆☆☆☆ | ★★★★★ | Poppler |
| pikepdf | Fast | ★★★★★ | ★★★★☆ | ★★☆☆☆ | ★★☆☆☆ | QPDF (bundled) |

## Recommendations

### For Your Use Case:

**Option 1: PyMuPDF (fitz) - RECOMMENDED**
- Fastest performance
- Best all-around features
- Both splitting AND page-by-page loading
- Can extract text, images, render to images
- Single dependency

**Option 2: Combination Approach**
- Use **pdfplumber** for text extraction (better layout awareness)
- Use **pypdf** or **pikepdf** for splitting (pure Python, reliable)

**Option 3: Simple Splitting Only**
- Use **pypdf** - simplest, no external deps, perfect for just splitting

## Memory Efficiency Notes

For large PDFs, page-by-page iteration is crucial:
- PyMuPDF: Can load individual pages without loading entire PDF
- pdfplumber: Automatically handles page iteration efficiently
- pypdf: Load PDF once, iterate through pages

## Installation Commands

```bash
# Option 1: PyMuPDF (recommended)
pip install PyMuPDF

# Option 2: Combination
pip install pdfplumber pypdf

# Option 3: All tools for flexibility
pip install PyMuPDF pdfplumber pypdf pikepdf pdf2image

# Note: pdf2image requires system poppler:
# Ubuntu/Debian: sudo apt-get install poppler-utils
# macOS: brew install poppler
```

## Next Steps for Skills/Commands

Suggested skill/command ideas:
1. **pdf-split**: Split PDF into one-page PDFs
2. **pdf-chunk**: Load and process PDF page by page
3. **pdf-to-text**: Extract text from PDF (page by page or all)
4. **pdf-to-images**: Convert PDF pages to images
5. **pdf-info**: Get PDF metadata (page count, size, etc.)
