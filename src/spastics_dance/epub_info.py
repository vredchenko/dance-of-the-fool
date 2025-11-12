#!/usr/bin/env python3
"""
EPUB Info - Display EPUB metadata and structure

Usage:
    python -m spastics_dance.epub_info <file.epub>
    epub-info <file.epub>
"""

import argparse
import sys
import zipfile
from pathlib import Path
from typing import Any

try:
    from ebooklib import epub, ITEM_DOCUMENT, ITEM_IMAGE, ITEM_STYLE, ITEM_NAVIGATION
except ImportError:
    print("Error: ebooklib not installed. Install with: pip install ebooklib", file=sys.stderr)
    sys.exit(1)


def get_epub_info(epub_path: Path) -> dict[str, Any]:
    """
    Extract metadata and structure from an EPUB file.

    Args:
        epub_path: Path to the EPUB file

    Returns:
        Dictionary containing EPUB information

    Raises:
        FileNotFoundError: If EPUB file doesn't exist
        Exception: If EPUB cannot be opened or is corrupted
    """
    if not epub_path.exists():
        raise FileNotFoundError(f"EPUB file not found: {epub_path}")

    try:
        book = epub.read_epub(str(epub_path))
    except Exception as e:
        raise Exception(f"Failed to open EPUB: {e}") from e

    # Extract metadata
    def get_meta(namespace: str, name: str) -> str:
        """Helper to get metadata value."""
        result = book.get_metadata(namespace, name)
        if result and len(result) > 0:
            return result[0][0] if isinstance(result[0], tuple) else result[0]
        return ""

    # Count different item types
    documents = list(book.get_items_of_type(ITEM_DOCUMENT))
    images = list(book.get_items_of_type(ITEM_IMAGE))
    styles = list(book.get_items_of_type(ITEM_STYLE))

    # Calculate file size
    file_size_bytes = epub_path.stat().st_size
    file_size_mb = file_size_bytes / (1024 * 1024)
    file_size_kb = file_size_bytes / 1024

    # Get internal file structure
    file_count = 0
    file_types = {}
    try:
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            files = zip_ref.namelist()
            file_count = len(files)
            for f in files:
                ext = Path(f).suffix or 'no_ext'
                file_types[ext] = file_types.get(ext, 0) + 1
    except Exception:
        pass  # Not critical if we can't read ZIP structure

    info = {
        'filename': epub_path.name,
        'path': str(epub_path.absolute()),
        'file_size_bytes': file_size_bytes,
        'file_size_mb': file_size_mb,
        'file_size_kb': file_size_kb,
        'metadata': {
            'title': get_meta('DC', 'title'),
            'author': get_meta('DC', 'creator'),
            'language': get_meta('DC', 'language'),
            'publisher': get_meta('DC', 'publisher'),
            'date': get_meta('DC', 'date'),
            'identifier': get_meta('DC', 'identifier'),
            'description': get_meta('DC', 'description'),
            'rights': get_meta('DC', 'rights'),
        },
        'structure': {
            'documents': len(documents),
            'images': len(images),
            'stylesheets': len(styles),
            'total_files': file_count,
            'file_types': file_types,
        },
        'chapters': [],
    }

    # Try to get chapter information from TOC
    try:
        toc = book.toc
        if toc:
            info['chapters'] = extract_toc_info(toc)
    except Exception:
        pass  # TOC might not be available

    # If no TOC, use documents as chapters
    if not info['chapters']:
        for i, doc in enumerate(documents):
            info['chapters'].append({
                'number': i + 1,
                'title': doc.get_name() or f"Chapter {i + 1}",
                'id': doc.get_id(),
                'size': len(doc.get_content()),
            })

    return info


def extract_toc_info(toc, level: int = 1) -> list[dict]:
    """
    Recursively extract TOC information.

    Args:
        toc: Table of contents (can be nested)
        level: Current nesting level

    Returns:
        List of chapter information dictionaries
    """
    chapters = []

    if isinstance(toc, list):
        for item in toc:
            chapters.extend(extract_toc_info(item, level))
    elif isinstance(toc, tuple):
        # TOC entry is (Section, [nested items])
        if len(toc) == 2:
            section, nested = toc
            if hasattr(section, 'title'):
                chapters.append({
                    'title': section.title,
                    'level': level,
                    'href': getattr(section, 'href', ''),
                })
            if nested:
                chapters.extend(extract_toc_info(nested, level + 1))
    elif hasattr(toc, 'title'):
        # Single section
        chapters.append({
            'title': toc.title,
            'level': level,
            'href': getattr(toc, 'href', ''),
        })

    return chapters


def format_info(info: dict[str, Any], verbose: bool = False) -> str:
    """
    Format EPUB info for display.

    Args:
        info: EPUB information dictionary
        verbose: Show detailed information

    Returns:
        Formatted string for display
    """
    lines = []
    lines.append("=" * 70)
    lines.append("EPUB INFORMATION")
    lines.append("=" * 70)
    lines.append("")

    # Basic info
    lines.append(f"Filename:     {info['filename']}")
    if verbose:
        lines.append(f"Path:         {info['path']}")

    # File size (adaptive formatting)
    if info['file_size_mb'] >= 1:
        lines.append(f"Size:         {info['file_size_mb']:.2f} MB")
    else:
        lines.append(f"Size:         {info['file_size_kb']:.2f} KB")

    # Metadata
    meta = info['metadata']
    if meta['title']:
        lines.append(f"Title:        {meta['title']}")
    if meta['author']:
        lines.append(f"Author:       {meta['author']}")
    if meta['language']:
        lines.append(f"Language:     {meta['language']}")
    if meta['publisher']:
        lines.append(f"Publisher:    {meta['publisher']}")

    if verbose:
        if meta['date']:
            lines.append(f"Date:         {meta['date']}")
        if meta['identifier']:
            lines.append(f"Identifier:   {meta['identifier']}")
        if meta['description']:
            lines.append(f"Description:  {meta['description'][:100]}...")
        if meta['rights']:
            lines.append(f"Rights:       {meta['rights']}")

    # Structure
    lines.append("")
    lines.append("Structure:")
    lines.append("-" * 70)
    struct = info['structure']
    lines.append(f"Documents:    {struct['documents']} HTML/XHTML files")
    lines.append(f"Images:       {struct['images']}")
    lines.append(f"Stylesheets:  {struct['stylesheets']}")
    lines.append(f"Chapters:     {len(info['chapters'])}")

    if verbose and struct['total_files'] > 0:
        lines.append(f"Total files:  {struct['total_files']}")
        lines.append("")
        lines.append("File types in EPUB archive:")
        for ext, count in sorted(struct['file_types'].items()):
            lines.append(f"  {ext}: {count}")

    # Chapters/TOC
    if info['chapters']:
        lines.append("")
        lines.append("Chapters/Documents:")
        lines.append("-" * 70)

        max_chapters = 20 if not verbose else len(info['chapters'])
        for i, chapter in enumerate(info['chapters'][:max_chapters]):
            if 'number' in chapter:
                # From documents
                lines.append(f"{chapter['number']:3d}. {chapter['title']}")
                if verbose:
                    lines.append(f"      ID: {chapter['id']}, Size: {chapter['size']} bytes")
            else:
                # From TOC
                indent = "  " * (chapter.get('level', 1) - 1)
                lines.append(f"{indent}- {chapter['title']}")
                if verbose and chapter.get('href'):
                    lines.append(f"{indent}  ({chapter['href']})")

        if len(info['chapters']) > max_chapters:
            lines.append(f"  ... and {len(info['chapters']) - max_chapters} more")

    lines.append("")
    lines.append("=" * 70)
    lines.append("✅ EPUB is an open format (ZIP archive with HTML/CSS/images)")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Display EPUB metadata and structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  epub-info book.epub
  epub-info book.epub --verbose
  python -m spastics_dance.epub_info book.epub
        """,
    )

    parser.add_argument(
        "epub_file",
        type=Path,
        help="Path to EPUB file",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed information",
    )

    args = parser.parse_args()

    try:
        info = get_epub_info(args.epub_file)
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
