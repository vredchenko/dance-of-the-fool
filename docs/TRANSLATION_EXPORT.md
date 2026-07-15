# Translation Export Tools

Scripts for exporting the English translation to PDF and EPUB formats.

## Prerequisites

Install the required dependencies:

```bash
# For PDF generation
pip install reportlab

# For EPUB generation
pip install ebooklib

# Or install the export-tools group from pyproject.toml
pip install -e ".[export-tools]"
```

## PDF Generation

Generate a PDF of the English translation:

```bash
# Basic PDF (without translator notes)
python3 scripts/generate-pdf.py

# With translator notes/uncertainties
python3 scripts/generate-pdf.py --include-uncertainties

# Custom output path
python3 scripts/generate-pdf.py --output my_translation.pdf
```

### PDF Features

- **Title page** with book title in English and Ukrainian
- **Formatted text** with proper paragraph spacing
- **Page breaks** after each chunk for easier navigation
- **Headers** for chunks and pages
- **Translator notes** (optional) highlighted in yellow boxes
- **Letter size** (8.5" x 11") pages

### PDF Output

- **Without uncertainties**: ~140KB, clean reading experience
- **With uncertainties**: ~150KB, includes all translation notes and questions

## EPUB Generation

Generate an EPUB e-book of the English translation:

```bash
# Basic EPUB (without translator notes)
python3 scripts/generate-epub.py

# With translator notes/uncertainties
python3 scripts/generate-epub.py --include-uncertainties

# Custom output path
python3 scripts/generate-epub.py --output my_translation.epub
```

### EPUB Features

- **Proper metadata** (title, author, language, description)
- **Table of contents** with chapter navigation
- **Styled content** using embedded CSS
- **Responsive** formatting for e-readers
- **Translator notes** (optional) in highlighted boxes
- **EPUB 3** compatible

### EPUB Output

- **Without uncertainties**: ~70KB, clean reading version
- **With uncertainties**: ~70KB, includes all translation notes

## Usage Examples

### Generate all formats at once

```bash
# Clean versions (no uncertainties)
python3 scripts/generate-pdf.py --output translation_english.pdf
python3 scripts/generate-epub.py --output translation_english.epub

# Versions with translator notes
python3 scripts/generate-pdf.py --output translation_with_notes.pdf --include-uncertainties
python3 scripts/generate-epub.py --output translation_with_notes.epub --include-uncertainties
```

### Quick generation script

Create a script `generate-all.sh`:

```bash
#!/bin/bash
echo "Generating English translation exports..."

python3 scripts/generate-pdf.py --output translation_english.pdf
echo "✓ PDF (clean) generated"

python3 scripts/generate-pdf.py --output translation_english_with_notes.pdf --include-uncertainties
echo "✓ PDF (with notes) generated"

python3 scripts/generate-epub.py --output translation_english.epub
echo "✓ EPUB (clean) generated"

python3 scripts/generate-epub.py --output translation_english_with_notes.epub --include-uncertainties
echo "✓ EPUB (with notes) generated"

echo "Done!"
```

Then run:

```bash
chmod +x generate-all.sh
./generate-all.sh
```

## File Structure

The scripts read from:
- `translation_chunk_01.md` through `translation_chunk_39.md` - English translations
- `translation_chunk_01_uncertainty.md` through `translation_chunk_39_uncertainty.md` - Translation notes

## Translator Notes Format

When `--include-uncertainties` is used, each note includes:

- **Original:** The Ukrainian phrase in question
- **Question:** The translator's question or context
- **Translation:** The chosen English translation

These appear as:
- **PDF:** Yellow-highlighted boxes with clear formatting
- **EPUB:** Styled div elements with border and background

## Output Quality

### PDF Quality
- Professional typography using standard fonts
- Justified text alignment for readability
- Proper page margins (0.75" - 1")
- Clear visual hierarchy with headers
- Print-ready format

### EPUB Quality
- Clean HTML structure
- Embedded CSS for consistent styling
- Proper semantic markup
- E-reader compatible
- Works on Kindle, Nook, Apple Books, etc.

## Troubleshooting

### "reportlab not installed"

```bash
pip install reportlab
```

### "ebooklib not installed"

```bash
pip install ebooklib
```

### Encoding errors with Ukrainian text

The scripts use UTF-8 encoding. Make sure your terminal and Python environment support UTF-8:

```bash
export PYTHONIOENCODING=utf-8
```

### Missing translation files

Make sure you're running the scripts from the repository root:

```bash
cd /path/to/dance-of-the-fool
python3 scripts/generate-pdf.py
```

## Customization

### Modify PDF styling

Edit `scripts/generate-pdf.py` and adjust the ParagraphStyle definitions:

```python
styles.add(ParagraphStyle(
    name='BookBody',
    fontSize=11,        # Change font size
    alignment=TA_JUSTIFY,  # Or TA_LEFT, TA_CENTER, TA_RIGHT
    spaceAfter=8
))
```

### Modify EPUB styling

Edit `scripts/generate-epub.py` and update the CSS:

```python
style = '''
body {
    font-family: Georgia, serif;  /* Change font */
    line-height: 1.6;              /* Adjust line spacing */
}
'''
```

## Advanced Options

### Custom page size for PDF

Edit `generate-pdf.py`:

```python
from reportlab.lib.pagesizes import A4, letter

# Change to A4 (international standard)
doc = SimpleDocTemplate(
    str(output_path),
    pagesize=A4,  # Instead of letter
    ...
)
```

### Add cover image to EPUB

The EPUB script can be extended to include cover images. See ebooklib documentation:
https://github.com/aerkalov/ebooklib

## Notes

- Generated files are gitignored by default
- Each script processes all 39 chunks (468 pages)
- Processing time: ~5-10 seconds per format
- Scripts are idempotent (safe to run multiple times)

## See Also

- `WEBUI_DEVPLAN.md` - Web-based proofreading interface
- `WEBUI_SETUP.md` - Web UI setup instructions
- `CLAUDE.md` - Overall project documentation
