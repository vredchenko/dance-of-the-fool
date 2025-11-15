#!/usr/bin/env python3
"""
Normalize all translation markdown files to consistent format.

Target format:
# Translation: Pages X-Y (Chunk NN/39)

## Page N

content

## Page M

content
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

def normalize_markdown(chunk_num: int, content: str) -> str:
    """Normalize markdown to consistent format."""

    # Extract page range from header (works for all current formats)
    page_range_match = re.search(r'Pages?\s+(\d+)-(\d+)', content)
    if not page_range_match:
        print(f"   ⚠ Warning: Could not extract page range from chunk {chunk_num:02d}")
        return content

    start_page = int(page_range_match.group(1))
    end_page = int(page_range_match.group(2))

    # Remove everything up to and including first separator or page marker
    # This handles all formats (book title, translation header, etc.)
    content = re.sub(r'^.*?(?=##?\s+Page\s+\d+|\n[^#])', '', content, flags=re.DOTALL)

    # Normalize page headers
    # Convert "### Page N" to "## Page N"
    content = re.sub(r'^###\s+Page\s+(\d+)', r'## Page \1', content, flags=re.MULTILINE)

    # For chunks without page markers, we need to insert them based on separators
    # First check if we already have page markers
    if not re.search(r'^##\s+Page\s+\d+', content, flags=re.MULTILINE):
        # No page markers - need to insert them
        # Split by separators and track page numbers
        parts = content.split('\n---\n')
        normalized_parts = []
        current_page = start_page

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Add page header
            normalized_parts.append(f"## Page {current_page}\n\n{part}")
            current_page += 1

        content = '\n\n'.join(normalized_parts)
    else:
        # Already has page markers - just clean up separators
        content = re.sub(r'\n---+\n', '\n\n', content)

    # Remove chapter annotations like "(Chapter N)"
    content = re.sub(r'\s*\(Chapter\s+\d+\)', '', content)

    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Build final normalized content
    header = f"# Translation: Pages {start_page}-{end_page} (Chunk {chunk_num:02d}/39)"
    normalized = f"{header}\n\n{content.strip()}\n"

    return normalized

def main():
    """Normalize all translation chunk markdown files."""
    print("📝 Normalizing translation markdown format...")
    print()

    for chunk_num in range(1, 40):
        file_path = REPO_ROOT / f"translation_chunk_{chunk_num:02d}.md"

        if not file_path.exists():
            print(f"   ⚠ Skipping chunk {chunk_num:02d} - file not found")
            continue

        print(f"   Processing chunk {chunk_num:02d}...")

        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        normalized_content = normalize_markdown(chunk_num, original_content)

        # Only write if content changed
        if normalized_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(normalized_content)
            print(f"      ✓ Updated")
        else:
            print(f"      • No changes needed")

    print()
    print("✓ Markdown normalization complete!")

if __name__ == '__main__':
    main()
