#!/usr/bin/env python3
"""
EPUB Chunk - Process EPUB chapter-by-chapter in a memory-efficient manner

Usage:
    python -m spastics_dance.epub_chunk <file.epub> [options]
    epub-chunk <file.epub> [options]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Generator, Any

try:
    from ebooklib import epub, ITEM_DOCUMENT
except ImportError:
    print("Error: ebooklib not installed. Install with: pip install ebooklib", file=sys.stderr)
    sys.exit(1)


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

    # Remove scripts and styles
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Decode common HTML entities
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


def chunk_epub(epub_path: Path) -> Generator[tuple[int, Any, str], None, None]:
    """
    Iterate through EPUB chapters/documents one at a time.

    Args:
        epub_path: Path to EPUB file

    Yields:
        Tuple of (chapter_number, document_item, document_name) for each chapter

    Raises:
        FileNotFoundError: If EPUB file doesn't exist
        Exception: If EPUB cannot be opened
    """
    if not epub_path.exists():
        raise FileNotFoundError(f"EPUB file not found: {epub_path}")

    try:
        book = epub.read_epub(str(epub_path))
    except Exception as e:
        raise Exception(f"Failed to open EPUB: {e}") from e

    documents = list(book.get_items_of_type(ITEM_DOCUMENT))

    if not documents:
        raise Exception("No documents found in EPUB")

    for i, doc in enumerate(documents):
        doc_name = doc.get_name() or f"Chapter {i + 1}"
        yield (i + 1, doc, doc_name)


def extract_text_action(epub_path: Path, output_format: str = "text", **kwargs) -> None:
    """
    Extract text from each chapter.

    Args:
        epub_path: Path to EPUB file
        output_format: Output format (text, json)
        **kwargs: Additional arguments (verbose)
    """
    verbose = kwargs.get("verbose", False)

    results = []

    for chapter_num, doc, doc_name in chunk_epub(epub_path):
        content = doc.get_content()
        text = extract_text_from_html(content)
        char_count = len(text)
        word_count = len(text.split())

        if output_format == "json":
            results.append({
                "chapter": chapter_num,
                "name": doc_name,
                "text": text,
                "char_count": char_count,
                "word_count": word_count,
            })
        else:  # text format
            if verbose:
                print(f"{'='*70}")
                print(f"Chapter {chapter_num}: {doc_name}")
                print(f"{'='*70}")
                print(text)
                print()
            else:
                print(f"Chapter {chapter_num}: {doc_name}")
                print(f"  {char_count} chars, {word_count} words")
                print()

    if output_format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))


def analyze_action(epub_path: Path, **kwargs) -> None:
    """
    Analyze each chapter structure.

    Args:
        epub_path: Path to EPUB file
        **kwargs: Additional arguments (verbose)
    """
    verbose = kwargs.get("verbose", False)

    print(f"{'='*70}")
    print(f"EPUB Analysis: {epub_path.name}")
    print(f"{'='*70}")
    print()

    for chapter_num, doc, doc_name in chunk_epub(epub_path):
        content = doc.get_content()
        text = extract_text_from_html(content)
        char_count = len(text)
        word_count = len(text.split())

        # Count HTML elements
        html_str = content.decode('utf-8', errors='ignore')
        img_count = len(re.findall(r'<img[^>]*>', html_str, re.IGNORECASE))
        link_count = len(re.findall(r'<a[^>]*href', html_str, re.IGNORECASE))
        para_count = len(re.findall(r'<p[^>]*>', html_str, re.IGNORECASE))

        print(f"Chapter {chapter_num}: {doc_name}")
        print(f"  Document ID:  {doc.get_id()}")
        print(f"  HTML size:    {len(content)} bytes")
        print(f"  Text:         {char_count} characters, {word_count} words")
        print(f"  Paragraphs:   {para_count}")
        print(f"  Images:       {img_count}")
        print(f"  Links:        {link_count}")

        if verbose and text:
            preview = text[:200].replace("\n", " ").strip()
            print(f"  Preview:      {preview}...")

        print()


def count_action(epub_path: Path, **kwargs) -> None:
    """
    Count statistics for all chapters.

    Args:
        epub_path: Path to EPUB file
        **kwargs: Additional arguments
    """
    total_chars = 0
    total_words = 0
    total_html_bytes = 0
    chapter_count = 0

    print(f"Processing chapters", end="", flush=True)

    for chapter_num, doc, doc_name in chunk_epub(epub_path):
        content = doc.get_content()
        text = extract_text_from_html(content)

        char_count = len(text)
        word_count = len(text.split())

        total_chars += char_count
        total_words += word_count
        total_html_bytes += len(content)
        chapter_count += 1

        print(".", end="", flush=True)

    print(" Done!\n")

    print(f"{'='*70}")
    print(f"Statistics Summary")
    print(f"{'='*70}")
    print(f"Chapters:             {chapter_count}")
    print(f"Total HTML size:      {total_html_bytes:,} bytes ({total_html_bytes / 1024:.1f} KB)")
    print(f"Total characters:     {total_chars:,}")
    print(f"Total words:          {total_words:,}")
    print(f"Avg chars/chapter:    {total_chars / chapter_count:.0f}")
    print(f"Avg words/chapter:    {total_words / chapter_count:.0f}")
    print(f"{'='*70}")


def list_action(epub_path: Path, **kwargs) -> None:
    """
    List all chapters with basic info.

    Args:
        epub_path: Path to EPUB file
        **kwargs: Additional arguments
    """
    print(f"{'='*70}")
    print(f"Chapter List: {epub_path.name}")
    print(f"{'='*70}")
    print()

    for chapter_num, doc, doc_name in chunk_epub(epub_path):
        content = doc.get_content()
        text = extract_text_from_html(content)
        word_count = len(text.split())

        print(f"{chapter_num:3d}. {doc_name}")
        print(f"      Words: {word_count:,}")


# Action mapping
ACTIONS = {
    "extract": extract_text_action,
    "analyze": analyze_action,
    "count": count_action,
    "list": list_action,
}


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Process EPUB chapter-by-chapter in a memory-efficient manner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Actions:
  extract    Extract text from each chapter
  analyze    Analyze chapter structure (size, images, links)
  count      Count statistics across all chapters
  list       List all chapters with basic info

Examples:
  # List all chapters
  epub-chunk book.epub --action list

  # Analyze all chapters
  epub-chunk book.epub --action analyze

  # Count statistics
  epub-chunk book.epub --action count

  # Extract text in JSON format
  epub-chunk book.epub --action extract --format json

  # Show full text for each chapter
  epub-chunk book.epub --action extract --verbose
        """,
    )

    parser.add_argument(
        "epub_file",
        type=Path,
        help="Path to EPUB file",
    )

    parser.add_argument(
        "--action",
        choices=list(ACTIONS.keys()),
        default="list",
        help="Action to perform (default: list)",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for extract action (default: text)",
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
            epub_path=args.epub_file,
            output_format=args.format,
            verbose=args.verbose,
        )
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
