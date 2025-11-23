#!/usr/bin/env python3
"""
Aggregate translation data into structured JSON for the web UI.

This script reads:
- original_chunk_*.md files (Ukrainian source text in markdown)
- translation_chunk_*.md files (English translations)
- translation_chunk_*_uncertainty.md files (translation notes)

And outputs:
- webui/src/data/translation-data.json (structured data for Astro)
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any

# Paths
REPO_ROOT = Path(__file__).parent.parent
OUTPUT_FILE = REPO_ROOT / "webui" / "src" / "data" / "translation-data.json"

def parse_ukrainian_md(chunk_num: int) -> List[Dict[str, Any]]:
    """Parse Ukrainian source from original_chunk_XX.md"""
    path = REPO_ROOT / "book" / "translations" / "v1" / f"original_chunk_{chunk_num:02d}.md"

    if not path.exists():
        print(f"⚠ Warning: {path} not found")
        return []

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract page sections
    # Pattern: ## Сторінка N followed by content until next ## Сторінка
    pages = []

    # Split by ## Сторінка markers
    page_splits = re.split(r'^##\s+Сторінка\s+(\d+)', content, flags=re.MULTILINE)

    # Skip the header (before first page)
    for i in range(1, len(page_splits), 2):
        if i + 1 >= len(page_splits):
            break

        page_num = int(page_splits[i])
        page_content = page_splits[i + 1]

        # Clean up the content
        page_content = page_content.strip()

        # Calculate stats
        char_count = len(page_content)
        word_count = len(page_content.split()) if page_content else 0

        pages.append({
            "page_number": page_num,
            "ukrainian_text": page_content,
            "char_count": char_count,
            "word_count": word_count
        })

    return pages

def parse_translation_md(chunk_num: int) -> List[Dict[str, Any]]:
    """Parse English translation from markdown"""
    path = REPO_ROOT / "book" / "translations" / "v1" / f"translation_chunk_{chunk_num:02d}.md"

    if not path.exists():
        print(f"⚠ Warning: {path} not found")
        return []

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract page sections
    # Pattern: ## Page N followed by content until next ## Page
    pages = []

    # Split by ## Page markers
    page_splits = re.split(r'^##\s+Page\s+(\d+)', content, flags=re.MULTILINE)

    # Skip the header (before first page)
    for i in range(1, len(page_splits), 2):
        if i + 1 >= len(page_splits):
            break

        page_num = int(page_splits[i])
        page_content = page_splits[i + 1]

        # Clean up the content
        page_content = page_content.strip()

        pages.append({
            "page_number": page_num,
            "english_text": page_content
        })

    return pages

def parse_uncertainty_md(chunk_num: int) -> List[Dict[str, Any]]:
    """Parse uncertainty notes from markdown"""
    path = REPO_ROOT / "book" / "translations" / "v1" / f"translation_chunk_{chunk_num:02d}_uncertainty.md"

    if not path.exists():
        return []

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # If file is empty or only has headers, return empty
    if len(content.strip()) < 50:
        return []

    uncertainties = []

    # Pattern: ## Page N ... **Original:** ... **Question:** ... **Current translation:**
    # Using a more flexible pattern to handle multiline content
    page_sections = re.split(r'## Page (\d+)', content)

    for i in range(1, len(page_sections), 2):
        if i + 1 >= len(page_sections):
            break

        page_num = int(page_sections[i])
        section_content = page_sections[i + 1]

        # Extract individual uncertainty entries within this page
        # Each entry has **Original:** **Question:** **Current translation:**
        entries = re.finditer(
            r'\*\*Original:\*\* ["\"](.+?)["\"]\s*\n\*\*Question:\*\* (.+?)\s*\n\*\*Current translation:\*\* ["\"](.+?)["\"]',
            section_content,
            re.DOTALL
        )

        for match in entries:
            uncertainties.append({
                "page_number": page_num,
                "original_text": match.group(1).strip(),
                "question": match.group(2).strip(),
                "current_translation": match.group(3).strip()
            })

    return uncertainties

def build_complete_data() -> List[Dict[str, Any]]:
    """Build complete translation dataset"""
    chunks = []

    for chunk_num in range(1, 40):  # 1-39
        print(f"Processing chunk {chunk_num:02d}...")

        # Get Ukrainian source (from markdown)
        ukrainian_pages = parse_ukrainian_md(chunk_num)

        # Get English translation
        english_pages = parse_translation_md(chunk_num)

        # Get uncertainties
        uncertainties = parse_uncertainty_md(chunk_num)

        # Merge data by page number
        page_map = {}

        # Add Ukrainian text
        for page in ukrainian_pages:
            page_num = page["page_number"]
            page_map[page_num] = {
                "page_number": page_num,
                "ukrainian_text": page["ukrainian_text"],
                "char_count": page["char_count"],
                "word_count": page["word_count"],
                "english_text": "",
                "uncertainties": []
            }

        # Add English text
        for page in english_pages:
            page_num = page["page_number"]
            if page_num in page_map:
                page_map[page_num]["english_text"] = page["english_text"]
            else:
                # Page exists in translation but not in source
                page_map[page_num] = {
                    "page_number": page_num,
                    "ukrainian_text": "",
                    "char_count": 0,
                    "word_count": 0,
                    "english_text": page["english_text"],
                    "uncertainties": []
                }

        # Add uncertainties
        for unc in uncertainties:
            page_num = unc["page_number"]
            if page_num in page_map:
                page_map[page_num]["uncertainties"].append({
                    "original": unc["original_text"],
                    "question": unc["question"],
                    "translation": unc["current_translation"]
                })

        # Calculate page range
        page_numbers = sorted(page_map.keys())
        start_page = page_numbers[0] if page_numbers else 0
        end_page = page_numbers[-1] if page_numbers else 0

        # Count uncertainties
        total_uncertainties = sum(len(page_map[pn]["uncertainties"]) for pn in page_numbers)

        chunks.append({
            "chunk_number": chunk_num,
            "page_range": f"{start_page}-{end_page}",
            "start_page": start_page,
            "end_page": end_page,
            "page_count": len(page_numbers),
            "uncertainty_count": total_uncertainties,
            "pages": [page_map[pn] for pn in page_numbers]
        })

    return chunks

def main():
    """Main entry point"""
    print("=" * 60)
    print("Building translation data for web UI...")
    print("=" * 60)

    chunks = build_complete_data()

    # Calculate statistics
    total_pages = sum(len(c['pages']) for c in chunks)
    total_uncertainties = sum(c['uncertainty_count'] for c in chunks)

    # Create output directory
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON
    output_data = {
        "book_title": "Танець недоумка / The Dance of the Fool",
        "author": "Ілларіон Павлюк / Illarion Pavlyuk",
        "total_chunks": len(chunks),
        "total_pages": 468,
        "actual_pages_with_content": total_pages,
        "total_uncertainties": total_uncertainties,
        "chunks": chunks
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print()
    print("=" * 60)
    print(f"✓ Successfully processed {len(chunks)} chunks")
    print(f"  Pages: {total_pages}")
    print(f"  Uncertainties: {total_uncertainties}")
    print(f"  Output: {OUTPUT_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    main()
