#!/usr/bin/env python3
"""
EPUB Split - Extract individual chapters/documents from EPUB

Usage:
    python -m spastics_dance.epub_split <file.epub> [output_dir]
    epub-split <file.epub> [output_dir]
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

try:
    from ebooklib import epub, ITEM_DOCUMENT
except ImportError:
    print("Error: ebooklib not installed. Install with: pip install ebooklib", file=sys.stderr)
    sys.exit(1)


def sanitize_filename(name: str) -> str:
    """
    Convert a title/name into a safe filename.

    Args:
        name: Original name

    Returns:
        Sanitized filename
    """
    # Remove or replace unsafe characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace spaces with underscores
    name = re.sub(r'\s+', '_', name)
    # Remove leading/trailing underscores and dots
    name = name.strip('._')
    # Limit length
    name = name[:100]
    return name or "untitled"


def extract_text_from_html(html_content: bytes) -> str:
    """
    Extract plain text from HTML content.

    Args:
        html_content: HTML as bytes

    Returns:
        Plain text content
    """
    try:
        text = html_content.decode('utf-8', errors='ignore')
    except Exception:
        return ""

    # Simple HTML tag removal (basic approach)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)

    # Decode HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")

    # Clean up whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)

    return text.strip()


def split_epub(
    epub_path: Path,
    output_dir: Optional[Path] = None,
    format: str = "html",
    prefix: str = "chapter",
    verbose: bool = False,
) -> list[Path]:
    """
    Extract chapters/documents from EPUB to individual files.

    Args:
        epub_path: Path to input EPUB file
        output_dir: Directory to save extracted chapters (default: 'chapters' in current dir)
        format: Output format - 'html', 'text'
        prefix: Prefix for output filenames (default: 'chapter')
        verbose: Print progress messages

    Returns:
        List of paths to created files

    Raises:
        FileNotFoundError: If input EPUB doesn't exist
        Exception: If EPUB cannot be opened or processed
    """
    if not epub_path.exists():
        raise FileNotFoundError(f"EPUB file not found: {epub_path}")

    # Open EPUB
    try:
        book = epub.read_epub(str(epub_path))
    except Exception as e:
        raise Exception(f"Failed to open EPUB: {e}") from e

    # Get all document items (chapters)
    documents = list(book.get_items_of_type(ITEM_DOCUMENT))

    if not documents:
        raise Exception("No documents found in EPUB")

    # Set default output directory
    if output_dir is None:
        output_dir = Path.cwd() / "chapters"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"Extracting EPUB: {epub_path.name}")
        print(f"Documents found: {len(documents)}")
        print(f"Output format: {format}")
        print(f"Output directory: {output_dir}")
        print()

    created_files = []

    # Extract each document
    for i, doc in enumerate(documents):
        doc_num = i + 1
        content = doc.get_content()

        # Generate filename
        doc_name = doc.get_name() or f"{prefix}_{doc_num:03d}"
        # Clean up the name
        if '/' in doc_name:
            doc_name = Path(doc_name).stem
        doc_name = sanitize_filename(doc_name)

        # Determine file extension
        if format == "text":
            ext = ".txt"
            output_content = extract_text_from_html(content)
        else:  # html
            ext = ".html"
            try:
                output_content = content.decode('utf-8', errors='ignore')
            except Exception:
                output_content = str(content)

        # Create output filename
        output_filename = f"{doc_num:03d}_{doc_name}{ext}"
        output_path = output_dir / output_filename

        # Write the file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
            created_files.append(output_path)

            if verbose:
                size = len(output_content)
                print(f"  Created: {output_filename} ({size} bytes)")
        except Exception as e:
            if verbose:
                print(f"  ⚠️  Failed to write {output_filename}: {e}")

    if verbose:
        print()
        print(f"✅ Successfully extracted {len(created_files)} documents to: {output_dir}")

    return created_files


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Extract individual chapters/documents from EPUB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract all chapters as HTML
  epub-split book.epub

  # Extract to custom directory
  epub-split book.epub output/

  # Extract as plain text
  epub-split book.epub --format text

  # Custom filename prefix
  epub-split book.epub --prefix part
        """,
    )

    parser.add_argument(
        "epub_file",
        type=Path,
        help="Path to EPUB file",
    )

    parser.add_argument(
        "output_dir",
        type=Path,
        nargs="?",
        default=None,
        help="Output directory (default: ./chapters/)",
    )

    parser.add_argument(
        "--format",
        choices=["html", "text"],
        default="html",
        help="Output format (default: html)",
    )

    parser.add_argument(
        "--prefix",
        type=str,
        default="chapter",
        help="Prefix for output filenames (default: 'chapter')",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show progress messages",
    )

    args = parser.parse_args()

    try:
        created_files = split_epub(
            epub_path=args.epub_file,
            output_dir=args.output_dir,
            format=args.format,
            prefix=args.prefix,
            verbose=args.verbose,
        )

        if not args.verbose:
            print(f"✅ Extracted {len(created_files)} documents to: {args.output_dir or 'chapters/'}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
