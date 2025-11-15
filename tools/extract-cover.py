#!/usr/bin/env python3
"""
Extract book cover from PDF page 1 as an image for webui background.
"""

import fitz  # PyMuPDF
from pathlib import Path

PDF_PATH = Path(__file__).parent.parent / "book" / "originals" / "pavlyuk_tanets_nedoumka_e27087_470337.pdf"
OUTPUT_DIR = Path(__file__).parent.parent / "webui" / "public"

def extract_cover():
    """Extract page 1 of PDF as high-quality PNG image."""

    print(f"📖 Opening PDF: {PDF_PATH.name}")
    doc = fitz.open(str(PDF_PATH))

    # Get first page (page 0)
    page = doc[0]
    print(f"   Page size: {page.rect.width} x {page.rect.height}")

    # Render at 2x resolution for better quality
    zoom = 2.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)

    # Save as PNG
    output_path = OUTPUT_DIR / "book-cover.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(str(output_path))

    doc.close()

    print(f"✓ Cover extracted: {output_path}")
    print(f"  Size: {pix.width} x {pix.height} pixels")
    print(f"  File size: {output_path.stat().st_size / 1024:.1f} KB")

if __name__ == '__main__':
    extract_cover()
