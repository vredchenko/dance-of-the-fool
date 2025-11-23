#!/usr/bin/env python3
"""
Generate Ukrainian original content in markdown format from JSON chunks.

This script reads the Ukrainian text from chunk_*.json files and formats it
as markdown, matching the structure of the English translation files.

Output files: book/translations/v1/original_chunk_XX.md
"""

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
CHUNKS_DIR = REPO_ROOT / "book" / "originals" / "chunks"
OUTPUT_DIR = REPO_ROOT / "book" / "translations" / "v1"


def format_ukrainian_text(text: str) -> str:
    """
    Format Ukrainian text with proper paragraph breaks.

    The JSON text uses \xa0 (non-breaking spaces) as section markers.
    We'll convert these to paragraph breaks and clean up spacing.
    """
    if not text or text.strip() == "":
        return "*(Cover page - no text)*"

    # Replace non-breaking spaces with regular spaces for processing
    text = text.replace('\xa0', ' ')

    # Clean up multiple spaces
    text = re.sub(r' {2,}', ' ', text)

    # Try to detect paragraph boundaries by looking for sentence endings
    # followed by capital letters or common paragraph starters
    # This is a heuristic approach

    # Split on periods followed by space and capital letter
    # But preserve abbreviations and numbers
    paragraphs = []
    current = []
    sentences = re.split(r'(?<=[.!?…])\s+(?=[А-ЯІЇЄҐ])', text)

    for sentence in sentences:
        current.append(sentence)
        # If we have a few sentences, consider it a paragraph
        # This is arbitrary but helps break up long text
        if len(current) >= 3:
            paragraphs.append(' '.join(current))
            current = []

    # Add remaining sentences
    if current:
        paragraphs.append(' '.join(current))

    # If we only got one paragraph but it's very long, try to split more aggressively
    if len(paragraphs) == 1 and len(text) > 500:
        # Split on sentence boundaries
        sentences = re.split(r'(?<=[.!?…])\s+', text)
        paragraphs = []
        current = []
        for sentence in sentences:
            current.append(sentence)
            if len(' '.join(current)) > 300:
                paragraphs.append(' '.join(current))
                current = []
        if current:
            paragraphs.append(' '.join(current))

    # Join paragraphs with double newlines
    return '\n\n'.join(p.strip() for p in paragraphs if p.strip())


def get_page_range(chunk_num: int) -> tuple[int, int]:
    """Calculate page range for a chunk (12 pages per chunk)."""
    start_page = (chunk_num - 1) * 12 + 1
    end_page = min(chunk_num * 12, 468)  # Max 468 pages
    return start_page, end_page


def generate_ukrainian_markdown(chunk_num: int) -> str:
    """Generate Ukrainian markdown content for a chunk."""
    json_path = CHUNKS_DIR / f"chunk_{chunk_num:02d}.json"

    if not json_path.exists():
        print(f"⚠ Warning: {json_path} not found")
        return None

    # Read JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        pages = json.load(f)

    # Get page range
    start_page, end_page = get_page_range(chunk_num)

    # Build markdown content
    lines = []
    lines.append(f"# Оригінал: Сторінки {start_page}-{end_page} (Частина {chunk_num:02d}/39)")
    lines.append("")

    for page_data in pages:
        page_num = page_data["page"]
        text = page_data["text"]

        lines.append(f"## Сторінка {page_num}")
        lines.append("")

        # Format the text with paragraphs
        formatted_text = format_ukrainian_text(text)
        lines.append(formatted_text)
        lines.append("")

    return '\n'.join(lines)


def main():
    """Generate all Ukrainian markdown files."""
    print("=" * 60)
    print("Generating Ukrainian markdown from JSON chunks...")
    print("=" * 60)
    print()

    # Create output directory if needed
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = 0
    skipped = 0

    for chunk_num in range(1, 40):  # 1-39
        print(f"Processing chunk {chunk_num:02d}...", end=" ")

        output_path = OUTPUT_DIR / f"original_chunk_{chunk_num:02d}.md"

        # Generate markdown
        markdown = generate_ukrainian_markdown(chunk_num)

        if markdown is None:
            print("SKIPPED (no JSON)")
            skipped += 1
            continue

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"✓ Created {output_path.name}")
        generated += 1

    print()
    print("=" * 60)
    print(f"✓ Generated {generated} Ukrainian markdown files")
    if skipped > 0:
        print(f"  Skipped {skipped} chunks (no source JSON)")
    print(f"  Output directory: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
