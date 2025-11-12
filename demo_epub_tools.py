#!/usr/bin/env python3
"""
Demonstration of EPUB handling - yes, EPUB is an open format!
"""

from ebooklib import epub
from ebooklib import ITEM_DOCUMENT
import os

def get_epub_info(epub_path):
    """Get basic EPUB information"""
    book = epub.read_epub(epub_path)

    print(f"\n📚 EPUB Information")
    print("=" * 60)
    print(f"File: {os.path.basename(epub_path)}")
    print(f"Title: {book.get_metadata('DC', 'title')}")
    print(f"Author: {book.get_metadata('DC', 'creator')}")
    print(f"Language: {book.get_metadata('DC', 'language')}")
    print(f"Publisher: {book.get_metadata('DC', 'publisher')}")

    # Count chapters/documents
    documents = list(book.get_items_of_type(ITEM_DOCUMENT))
    print(f"Number of HTML documents: {len(documents)}")
    print(f"File size: {os.path.getsize(epub_path) / 1024:.2f} KB")

def chunk_load_epub_chapters(epub_path, max_chapters=3):
    """Load EPUB chapters one by one"""
    book = epub.read_epub(epub_path)
    documents = list(book.get_items_of_type(ITEM_DOCUMENT))

    print(f"\n📖 Loading chapters one by one")
    print("=" * 60)
    print(f"Total documents: {len(documents)}\n")

    for i, item in enumerate(documents[:max_chapters]):
        content = item.get_content().decode('utf-8')
        # Remove HTML tags for preview
        import re
        text = re.sub('<[^<]+?>', '', content)
        text = re.sub(r'\s+', ' ', text).strip()

        print(f"Chapter/Document {i+1}:")
        print(f"  - ID: {item.get_id()}")
        print(f"  - Size: {len(content)} bytes")
        print(f"  - Preview: {text[:100]}...")
        print()

def extract_epub_structure(epub_path):
    """Show EPUB internal structure (it's just a ZIP!)"""
    import zipfile

    print(f"\n🔍 EPUB Internal Structure (it's a ZIP archive!)")
    print("=" * 60)

    with zipfile.ZipFile(epub_path, 'r') as zip_ref:
        files = zip_ref.namelist()
        print(f"Total files in EPUB: {len(files)}\n")

        # Group by type
        types = {}
        for f in files:
            ext = os.path.splitext(f)[1] or 'no_ext'
            types[ext] = types.get(ext, 0) + 1

        print("File types:")
        for ext, count in sorted(types.items()):
            print(f"  {ext}: {count} files")

        print("\nFirst 10 files:")
        for f in files[:10]:
            print(f"  - {f}")

if __name__ == "__main__":
    epub_file = "pavlyuk_tanets_nedoumka_e27087_470337.epub"

    # 1. Get info
    get_epub_info(epub_file)

    # 2. Load chapters
    chunk_load_epub_chapters(epub_file, max_chapters=3)

    # 3. Show structure
    extract_epub_structure(epub_file)

    print("\n" + "=" * 60)
    print("✅ EPUB is indeed an open format!")
    print("   It's a ZIP containing HTML, CSS, images, and metadata.")
    print("=" * 60)
