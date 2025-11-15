#!/bin/bash
#
# Regenerate all translation output formats
#
# This script runs all generation scripts to rebuild:
# - Webui data (translation-data.json)
# - PDF without uncertainties
# - PDF with uncertainties
# - EPUB without uncertainties
# - EPUB with uncertainties
#

set -e  # Exit on error

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/scripts" && pwd)"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "============================================================"
echo "REGENERATING ALL TRANSLATION FORMATS"
echo "============================================================"
echo ""

cd "$PROJECT_ROOT"

# 1. Webui data
echo ""
echo "============================================================"
echo "Running: build-webui-data.py"
echo "============================================================"
echo ""
python3 "$SCRIPTS_DIR/build-webui-data.py"
echo ""
echo "✓ Completed: Webui data"

# 2. PDF without uncertainties
echo ""
echo "============================================================"
echo "Running: generate-pdf.py --output translation.pdf"
echo "============================================================"
echo ""
python3 "$SCRIPTS_DIR/generate-pdf.py" --output translation.pdf
echo ""
echo "✓ Completed: PDF (no uncertainties)"

# 3. PDF with uncertainties
echo ""
echo "============================================================"
echo "Running: generate-pdf.py --output translation-with-notes.pdf --include-uncertainties"
echo "============================================================"
echo ""
python3 "$SCRIPTS_DIR/generate-pdf.py" --output translation-with-notes.pdf --include-uncertainties
echo ""
echo "✓ Completed: PDF (with uncertainties)"

# 4. EPUB without uncertainties
echo ""
echo "============================================================"
echo "Running: generate-epub.py --output translation.epub"
echo "============================================================"
echo ""
python3 "$SCRIPTS_DIR/generate-epub.py" --output translation.epub
echo ""
echo "✓ Completed: EPUB (no uncertainties)"

# 5. EPUB with uncertainties
echo ""
echo "============================================================"
echo "Running: generate-epub.py --output translation-with-notes.epub --include-uncertainties"
echo "============================================================"
echo ""
python3 "$SCRIPTS_DIR/generate-epub.py" --output translation-with-notes.epub --include-uncertainties
echo ""
echo "✓ Completed: EPUB (with uncertainties)"

# Summary
echo ""
echo "============================================================"
echo "SUMMARY"
echo "============================================================"
echo "✓ Webui data"
echo "✓ PDF (no uncertainties)"
echo "✓ PDF (with uncertainties)"
echo "✓ EPUB (no uncertainties)"
echo "✓ EPUB (with uncertainties)"
echo "============================================================"
echo ""
echo "✓ All formats regenerated successfully!"
echo ""
