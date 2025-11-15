#!/usr/bin/env python3
"""
Normalize Ukrainian text line breaks in chunk JSON files.

The PDF extraction includes line breaks from the PDF layout that aren't
actual paragraph breaks. This script:
1. Joins lines that are part of the same paragraph (single \n)
2. Preserves actual paragraph breaks (double \n)
3. Cleans up excessive whitespace
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

def normalize_text(text: str) -> str:
    """Normalize line breaks in Ukrainian text."""
    if not text or not text.strip():
        return text

    # Step 1: Replace multiple spaces/tabs with single space
    text = re.sub(r'[ \t]+', ' ', text)

    # Step 2: Identify paragraph breaks (double+ newlines) and mark them
    # Replace 2+ newlines with a special marker
    text = re.sub(r'\n\n+', '<<<PARAGRAPH_BREAK>>>', text)

    # Step 3: Join lines that are part of the same paragraph
    # Replace single newlines (sometimes with spaces) with a space
    text = re.sub(r'\n', ' ', text)

    # Step 4: Restore paragraph breaks
    text = text.replace('<<<PARAGRAPH_BREAK>>>', '\n\n')

    # Step 5: Clean up excessive spaces
    text = re.sub(r' +', ' ', text)

    # Step 6: Clean up spaces around paragraph breaks
    text = re.sub(r' *\n\n *', '\n\n', text)

    # Step 7: Remove trailing/leading whitespace on each paragraph
    paragraphs = text.split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    text = '\n\n'.join(paragraphs)

    return text

def normalize_chunk_file(chunk_path: Path) -> dict:
    """Normalize Ukrainian text in a single chunk JSON file."""
    print(f"   Processing: {chunk_path.name}")

    with open(chunk_path, 'r', encoding='utf-8') as f:
        chunk_data = json.load(f)

    changes_made = False
    for page in chunk_data:
        if 'text' in page and page['text']:
            original = page['text']
            normalized = normalize_text(original)

            if original != normalized:
                page['text'] = normalized
                changes_made = True

                # Also update word count (might have changed with normalization)
                page['word_count'] = len(normalized.split())
                page['char_count'] = len(normalized)

    return chunk_data, changes_made

def main():
    """Normalize all chunk JSON files."""
    chunk_files = sorted((REPO_ROOT / "book" / "originals" / "chunks").glob('chunk_*.json'))

    if not chunk_files:
        print("❌ No chunk files found!")
        return

    print(f"📝 Normalizing Ukrainian text in {len(chunk_files)} chunk files...")

    total_changed = 0
    for chunk_file in chunk_files:
        chunk_data, changed = normalize_chunk_file(chunk_file)

        if changed:
            # Write back to file
            with open(chunk_file, 'w', encoding='utf-8') as f:
                json.dump(chunk_data, f, ensure_ascii=False, indent=2)
            total_changed += 1
            print(f"      ✓ Updated {chunk_file.name}")

    print(f"\n✓ Normalization complete!")
    print(f"  {total_changed} files updated")
    print(f"  {len(chunk_files) - total_changed} files unchanged")

if __name__ == '__main__':
    main()
