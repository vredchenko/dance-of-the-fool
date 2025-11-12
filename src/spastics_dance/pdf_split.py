#!/usr/bin/env python3
"""
PDF Split - Split PDF into individual one-page PDF files

Usage:
    python -m spastics_dance.pdf_split <file.pdf> [output_dir]
    pdf-split <file.pdf> [output_dir]
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Install with: pip install PyMuPDF", file=sys.stderr)
    sys.exit(1)


def split_pdf(
    pdf_path: Path,
    output_dir: Optional[Path] = None,
    prefix: str = "page",
    start_page: Optional[int] = None,
    end_page: Optional[int] = None,
    verbose: bool = False,
) -> list[Path]:
    """
    Split a PDF into individual one-page PDF files.

    Args:
        pdf_path: Path to input PDF file
        output_dir: Directory to save split pages (default: 'pages' in current dir)
        prefix: Prefix for output filenames (default: 'page')
        start_page: First page to split (1-indexed, default: 1)
        end_page: Last page to split (1-indexed, default: last page)
        verbose: Print progress messages

    Returns:
        List of paths to created PDF files

    Raises:
        FileNotFoundError: If input PDF doesn't exist
        Exception: If PDF cannot be opened or processed
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Open source PDF
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise Exception(f"Failed to open PDF: {e}") from e

    total_pages = len(doc)

    # Set default output directory
    if output_dir is None:
        output_dir = Path.cwd() / "pages"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine page range
    start_idx = (start_page - 1) if start_page else 0
    end_idx = (end_page - 1) if end_page else (total_pages - 1)

    # Validate range
    if start_idx < 0 or start_idx >= total_pages:
        doc.close()
        raise ValueError(f"Start page {start_page} is out of range (1-{total_pages})")
    if end_idx < 0 or end_idx >= total_pages:
        doc.close()
        raise ValueError(f"End page {end_page} is out of range (1-{total_pages})")
    if start_idx > end_idx:
        doc.close()
        raise ValueError(f"Start page {start_page} is after end page {end_page}")

    pages_to_split = end_idx - start_idx + 1

    if verbose:
        print(f"Splitting PDF: {pdf_path.name}")
        print(f"Total pages in PDF: {total_pages}")
        print(f"Pages to split: {pages_to_split} (pages {start_idx + 1}-{end_idx + 1})")
        print(f"Output directory: {output_dir}")
        print()

    created_files = []

    # Split each page
    for page_idx in range(start_idx, end_idx + 1):
        # Calculate output number (always sequential starting from 1)
        output_num = page_idx - start_idx + 1

        # Create new PDF with just this page
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=page_idx, to_page=page_idx)

        # Generate output filename
        output_filename = f"{prefix}_{output_num:03d}.pdf"
        output_path = output_dir / output_filename

        # Save the single-page PDF
        new_doc.save(output_path)
        new_doc.close()

        created_files.append(output_path)

        if verbose:
            print(f"  Created: {output_filename} (from page {page_idx + 1})")

    doc.close()

    if verbose:
        print()
        print(f"✅ Successfully split {pages_to_split} pages to: {output_dir}")

    return created_files


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Split PDF into individual one-page PDF files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Split entire PDF to 'pages/' directory
  pdf-split book.pdf

  # Split to custom directory
  pdf-split book.pdf output/

  # Split specific page range
  pdf-split book.pdf --start 10 --end 20

  # Custom filename prefix
  pdf-split book.pdf --prefix chapter1
        """,
    )

    parser.add_argument(
        "pdf_file",
        type=Path,
        help="Path to PDF file",
    )

    parser.add_argument(
        "output_dir",
        type=Path,
        nargs="?",
        default=None,
        help="Output directory (default: ./pages/)",
    )

    parser.add_argument(
        "--prefix",
        type=str,
        default="page",
        help="Prefix for output filenames (default: 'page')",
    )

    parser.add_argument(
        "--start",
        type=int,
        default=None,
        help="First page to split (1-indexed)",
    )

    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="Last page to split (1-indexed)",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show progress messages",
    )

    args = parser.parse_args()

    try:
        created_files = split_pdf(
            pdf_path=args.pdf_file,
            output_dir=args.output_dir,
            prefix=args.prefix,
            start_page=args.start,
            end_page=args.end,
            verbose=args.verbose,
        )

        if not args.verbose:
            print(f"✅ Split {len(created_files)} pages to: {args.output_dir or 'pages/'}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
