#!/usr/bin/env python3
"""
PDF Info - Display PDF metadata and information

Usage:
    python -m spastics_dance.pdf_info <file.pdf>
    pdf-info <file.pdf>
"""

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Install with: pip install PyMuPDF", file=sys.stderr)
    sys.exit(1)


def get_pdf_info(pdf_path: Path) -> dict[str, Any]:
    """
    Extract metadata and basic information from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Dictionary containing PDF information

    Raises:
        FileNotFoundError: If PDF file doesn't exist
        Exception: If PDF cannot be opened or is corrupted
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise Exception(f"Failed to open PDF: {e}") from e

    metadata = doc.metadata or {}

    # Calculate file size
    file_size_bytes = pdf_path.stat().st_size
    file_size_mb = file_size_bytes / (1024 * 1024)
    file_size_kb = file_size_bytes / 1024

    info = {
        'filename': pdf_path.name,
        'path': str(pdf_path.absolute()),
        'pages': len(doc),
        'file_size_bytes': file_size_bytes,
        'file_size_mb': file_size_mb,
        'file_size_kb': file_size_kb,
        'encrypted': doc.is_encrypted,
        'metadata': {
            'title': metadata.get('title', ''),
            'author': metadata.get('author', ''),
            'subject': metadata.get('subject', ''),
            'keywords': metadata.get('keywords', ''),
            'creator': metadata.get('creator', ''),
            'producer': metadata.get('producer', ''),
            'creation_date': metadata.get('creationDate', ''),
            'modification_date': metadata.get('modDate', ''),
        }
    }

    # Get first page dimensions for reference
    if len(doc) > 0:
        first_page = doc[0]
        rect = first_page.rect
        info['page_dimensions'] = {
            'width': rect.width,
            'height': rect.height,
            'width_inches': rect.width / 72,  # PDF points to inches
            'height_inches': rect.height / 72,
        }

    doc.close()
    return info


def format_info(info: dict[str, Any], verbose: bool = False) -> str:
    """
    Format PDF info for display.

    Args:
        info: PDF information dictionary
        verbose: Show detailed metadata

    Returns:
        Formatted string for display
    """
    lines = []
    lines.append("=" * 70)
    lines.append("PDF INFORMATION")
    lines.append("=" * 70)
    lines.append("")

    # Basic info
    lines.append(f"Filename:     {info['filename']}")
    if verbose:
        lines.append(f"Path:         {info['path']}")
    lines.append(f"Pages:        {info['pages']}")

    # File size (adaptive formatting)
    if info['file_size_mb'] >= 1:
        lines.append(f"Size:         {info['file_size_mb']:.2f} MB")
    else:
        lines.append(f"Size:         {info['file_size_kb']:.2f} KB")

    lines.append(f"Encrypted:    {'Yes' if info['encrypted'] else 'No'}")

    # Page dimensions
    if 'page_dimensions' in info:
        dims = info['page_dimensions']
        lines.append(f"Page Size:    {dims['width']:.1f} x {dims['height']:.1f} points")
        lines.append(f"              ({dims['width_inches']:.2f} x {dims['height_inches']:.2f} inches)")

    # Metadata
    meta = info['metadata']
    if any(meta.values()):
        lines.append("")
        lines.append("Metadata:")
        lines.append("-" * 70)

        if meta['title']:
            lines.append(f"Title:        {meta['title']}")
        if meta['author']:
            lines.append(f"Author:       {meta['author']}")
        if meta['subject']:
            lines.append(f"Subject:      {meta['subject']}")
        if meta['keywords']:
            lines.append(f"Keywords:     {meta['keywords']}")

        if verbose:
            if meta['creator']:
                lines.append(f"Creator:      {meta['creator']}")
            if meta['producer']:
                lines.append(f"Producer:     {meta['producer']}")
            if meta['creation_date']:
                lines.append(f"Created:      {meta['creation_date']}")
            if meta['modification_date']:
                lines.append(f"Modified:     {meta['modification_date']}")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Display PDF metadata and information",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdf-info book.pdf
  pdf-info book.pdf --verbose
  python -m spastics_dance.pdf_info book.pdf
        """,
    )

    parser.add_argument(
        "pdf_file",
        type=Path,
        help="Path to PDF file",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed metadata",
    )

    args = parser.parse_args()

    try:
        info = get_pdf_info(args.pdf_file)
        output = format_info(info, verbose=args.verbose)
        print(output)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
