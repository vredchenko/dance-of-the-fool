#!/usr/bin/env python3
"""
PDF Chunk - Process PDF page-by-page in a memory-efficient manner

Usage:
    python -m spastics_dance.pdf_chunk <file.pdf> [options]
    pdf-chunk <file.pdf> [options]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Callable, Generator, Optional, Any

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Install with: pip install PyMuPDF", file=sys.stderr)
    sys.exit(1)


def chunk_pdf(
    pdf_path: Path,
    start_page: Optional[int] = None,
    end_page: Optional[int] = None,
) -> Generator[tuple[int, Any], None, None]:
    """
    Iterate through PDF pages one at a time (memory efficient).

    Args:
        pdf_path: Path to PDF file
        start_page: First page to process (1-indexed, default: 1)
        end_page: Last page to process (1-indexed, default: last page)

    Yields:
        Tuple of (page_number, page_object) for each page

    Raises:
        FileNotFoundError: If PDF file doesn't exist
        Exception: If PDF cannot be opened
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise Exception(f"Failed to open PDF: {e}") from e

    total_pages = len(doc)

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

    try:
        for page_idx in range(start_idx, end_idx + 1):
            page = doc[page_idx]
            yield (page_idx + 1, page)  # Yield 1-indexed page number
    finally:
        doc.close()


def extract_text_action(pdf_path: Path, output_format: str = "text", **kwargs) -> None:
    """
    Extract text from each page.

    Args:
        pdf_path: Path to PDF file
        output_format: Output format (text, json)
        **kwargs: Additional arguments (start_page, end_page, verbose)
    """
    verbose = kwargs.get("verbose", False)
    start_page = kwargs.get("start_page")
    end_page = kwargs.get("end_page")

    results = []

    for page_num, page in chunk_pdf(pdf_path, start_page, end_page):
        text = page.get_text()
        char_count = len(text)
        word_count = len(text.split())

        if output_format == "json":
            results.append({
                "page": page_num,
                "text": text,
                "char_count": char_count,
                "word_count": word_count,
            })
        else:  # text format
            if verbose:
                print(f"{'='*70}")
                print(f"Page {page_num}")
                print(f"{'='*70}")
                print(text)
                print()
            else:
                print(f"Page {page_num}: {char_count} chars, {word_count} words")

    if output_format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))


def analyze_action(pdf_path: Path, **kwargs) -> None:
    """
    Analyze each page structure.

    Args:
        pdf_path: Path to PDF file
        **kwargs: Additional arguments (start_page, end_page, verbose)
    """
    verbose = kwargs.get("verbose", False)
    start_page = kwargs.get("start_page")
    end_page = kwargs.get("end_page")

    print(f"{'='*70}")
    print(f"PDF Analysis: {pdf_path.name}")
    print(f"{'='*70}")
    print()

    for page_num, page in chunk_pdf(pdf_path, start_page, end_page):
        text = page.get_text()
        char_count = len(text)
        word_count = len(text.split())

        # Get page dimensions
        rect = page.rect
        width = rect.width
        height = rect.height

        # Count images
        image_list = page.get_images()
        image_count = len(image_list)

        # Count links
        links = page.get_links()
        link_count = len(links)

        print(f"Page {page_num}:")
        print(f"  Dimensions:  {width:.1f} x {height:.1f} points ({width/72:.2f} x {height/72:.2f} inches)")
        print(f"  Text:        {char_count} characters, {word_count} words")
        print(f"  Images:      {image_count}")
        print(f"  Links:       {link_count}")

        if verbose and text:
            preview = text[:200].replace("\n", " ").strip()
            print(f"  Preview:     {preview}...")

        print()


def count_action(pdf_path: Path, **kwargs) -> None:
    """
    Count statistics for each page.

    Args:
        pdf_path: Path to PDF file
        **kwargs: Additional arguments (start_page, end_page)
    """
    start_page = kwargs.get("start_page")
    end_page = kwargs.get("end_page")

    total_chars = 0
    total_words = 0
    total_images = 0
    page_count = 0

    print(f"Processing pages", end="", flush=True)

    for page_num, page in chunk_pdf(pdf_path, start_page, end_page):
        text = page.get_text()
        char_count = len(text)
        word_count = len(text.split())
        image_count = len(page.get_images())

        total_chars += char_count
        total_words += word_count
        total_images += image_count
        page_count += 1

        print(".", end="", flush=True)

    print(" Done!\n")

    print(f"{'='*70}")
    print(f"Statistics Summary")
    print(f"{'='*70}")
    print(f"Pages processed:     {page_count}")
    print(f"Total characters:    {total_chars:,}")
    print(f"Total words:         {total_words:,}")
    print(f"Total images:        {total_images}")
    print(f"Avg chars per page:  {total_chars / page_count:.0f}")
    print(f"Avg words per page:  {total_words / page_count:.0f}")
    print(f"{'='*70}")


# Action mapping
ACTIONS = {
    "extract": extract_text_action,
    "analyze": analyze_action,
    "count": count_action,
}


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Process PDF page-by-page in a memory-efficient manner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Actions:
  extract    Extract text from each page
  analyze    Analyze page structure (dimensions, images, links)
  count      Count statistics across pages

Examples:
  # Extract text from all pages
  pdf-chunk book.pdf --action extract

  # Analyze specific page range
  pdf-chunk book.pdf --action analyze --start 10 --end 20

  # Count statistics with progress
  pdf-chunk book.pdf --action count

  # Extract text in JSON format
  pdf-chunk book.pdf --action extract --format json

  # Show full text for each page
  pdf-chunk book.pdf --action extract --verbose
        """,
    )

    parser.add_argument(
        "pdf_file",
        type=Path,
        help="Path to PDF file",
    )

    parser.add_argument(
        "--action",
        choices=list(ACTIONS.keys()),
        default="analyze",
        help="Action to perform (default: analyze)",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for extract action (default: text)",
    )

    parser.add_argument(
        "--start",
        type=int,
        default=None,
        help="First page to process (1-indexed)",
    )

    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="Last page to process (1-indexed)",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output",
    )

    args = parser.parse_args()

    try:
        action_func = ACTIONS[args.action]
        action_func(
            pdf_path=args.pdf_file,
            output_format=args.format,
            start_page=args.start,
            end_page=args.end,
            verbose=args.verbose,
        )
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
