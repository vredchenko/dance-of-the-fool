# Proposed Skills/Commands for PDF & EPUB Processing

Based on the research, here are suggested skills we can build:

## PDF Skills

### 1. **pdf-split** - Split PDF into single-page files
```
Usage: /pdf-split <input.pdf> [output_dir]
Description: Splits a PDF into individual one-page PDFs
Technology: PyMuPDF (fast, efficient)
Output: pages/page_001.pdf, pages/page_002.pdf, etc.
```

### 2. **pdf-chunk** - Process PDF page-by-page
```
Usage: /pdf-chunk <input.pdf> [--pages 1-10] [--action extract|analyze]
Description: Load and process PDF pages one at a time (memory efficient)
Technology: PyMuPDF
Options:
  - Extract text from each page
  - Analyze structure
  - Custom processing per page
```

### 3. **pdf-extract** - Extract content from PDF
```
Usage: /pdf-extract <input.pdf> [--output text|json|markdown]
Description: Extract text, preserving structure
Technology: pdfplumber (best for layout) or PyMuPDF (fastest)
Features:
  - Extract tables
  - Preserve formatting
  - Output to different formats
```

### 4. **pdf-info** - Get PDF metadata
```
Usage: /pdf-info <input.pdf>
Description: Display PDF information (pages, size, metadata, etc.)
Technology: PyMuPDF
Output: Page count, file size, author, title, creation date
```

### 5. **pdf-range** - Extract page range
```
Usage: /pdf-range <input.pdf> <start-end> <output.pdf>
Example: /pdf-range book.pdf 10-20 chapter2.pdf
Description: Extract specific page range to new PDF
Technology: PyMuPDF or pikepdf
```

### 6. **pdf-to-images** - Convert pages to images
```
Usage: /pdf-to-images <input.pdf> [--dpi 300] [--format png|jpg]
Description: Convert each page to an image file
Technology: PyMuPDF (fitz can render directly) or pdf2image
Use case: OCR preprocessing, thumbnails
```

## EPUB Skills

### 7. **epub-info** - Get EPUB metadata
```
Usage: /epub-info <input.epub>
Description: Display EPUB information and structure
Technology: ebooklib
Output: Title, author, chapter count, file structure
```

### 8. **epub-extract** - Extract EPUB content
```
Usage: /epub-extract <input.epub> [--output dir|single-file]
Description: Extract EPUB chapters to HTML or plain text
Technology: ebooklib
Features:
  - Extract each chapter separately
  - Convert to plain text
  - Preserve images
```

### 9. **epub-to-pdf** - Convert EPUB to PDF
```
Usage: /epub-to-pdf <input.epub> <output.pdf>
Description: Convert EPUB to PDF format
Technology: ebooklib + reportlab or weasyprint
Note: Requires HTML-to-PDF conversion
```

## Combined Skills

### 10. **book-chunk** - Universal book chunking
```
Usage: /book-chunk <input.pdf|epub> [--chunk-size pages|chapters]
Description: Smart chunking for both PDF and EPUB
Technology: Detects format, uses appropriate tool
Features:
  - Auto-detect format
  - Consistent output format
  - Memory-efficient streaming
```

### 11. **book-info** - Universal book metadata
```
Usage: /book-info <input.pdf|epub>
Description: Get metadata from any book format
Technology: Auto-detect and use appropriate library
```

## Installation Requirements

```bash
# Core PDF tools (recommended)
pip install PyMuPDF

# For advanced text extraction
pip install pdfplumber

# For EPUB support
pip install ebooklib

# For PDF repair/advanced manipulation
pip install pikepdf

# For image conversion (optional)
pip install pdf2image  # Also needs: apt-get install poppler-utils
```

## Priority Recommendations

**Start with these 3:**
1. **pdf-split** - Most immediately useful for chunking
2. **pdf-chunk** - Core page-by-page processing
3. **pdf-info** - Quick metadata viewer

**Then add:**
4. **epub-info** - Since you have EPUB files
5. **book-chunk** - Universal solution

## Implementation Notes

- All skills should have `--help` option
- Progress indicators for large files
- Error handling for corrupted files
- Memory-efficient streaming for large PDFs (468 pages like yours!)
- Support for Ukrainian and other Unicode text (important for your book!)

## Example Use Cases

For your 468-page Ukrainian PDF:
```bash
# Get info
/pdf-info pavlyuk_tanets_nedoumka_e27087_470337.pdf

# Split into chapters (e.g., pages 1-50)
/pdf-range pavlyuk_tanets_nedoumka_e27087_470337.pdf 1-50 chapter1.pdf

# Process page by page without loading all in memory
/pdf-chunk pavlyuk_tanets_nedoumka_e27087_470337.pdf --action extract

# Split entire book into single pages (creates 468 files)
/pdf-split pavlyuk_tanets_nedoumka_e27087_470337.pdf output/
```

Ready to build any of these! Which ones would you like to start with?
