#!/usr/bin/env python3
"""
Demonstration of PDF chunking/splitting tools using PyMuPDF
"""

import fitz  # PyMuPDF
import os

def get_pdf_info(pdf_path):
    """Get basic PDF information"""
    doc = fitz.open(pdf_path)
    info = {
        'filename': os.path.basename(pdf_path),
        'page_count': len(doc),
        'metadata': doc.metadata,
        'file_size_mb': os.path.getsize(pdf_path) / (1024 * 1024)
    }
    doc.close()
    return info

def chunk_load_pages(pdf_path, max_pages=3):
    """Demonstrate loading pages one by one (memory efficient)"""
    doc = fitz.open(pdf_path)
    print(f"\n📄 Loading pages one by one from: {os.path.basename(pdf_path)}")
    print(f"Total pages: {len(doc)}\n")

    for page_num in range(min(max_pages, len(doc))):
        page = doc[page_num]
        text = page.get_text()
        word_count = len(text.split())
        char_count = len(text)

        print(f"Page {page_num + 1}:")
        print(f"  - Characters: {char_count}")
        print(f"  - Words: {word_count}")
        print(f"  - First 100 chars: {text[:100].strip()!r}")
        print()

    doc.close()

def split_pdf_to_single_pages(pdf_path, output_dir="pages"):
    """Split PDF into individual one-page PDFs"""
    doc = fitz.open(pdf_path)
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n✂️  Splitting PDF into {len(doc)} single-page PDFs...")

    for page_num in range(len(doc)):
        # Create new PDF with just this page
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

        output_path = os.path.join(output_dir, f"page_{page_num + 1:03d}.pdf")
        new_doc.save(output_path)
        new_doc.close()

        print(f"  Created: {output_path}")

    doc.close()
    print(f"\n✅ Done! Created {len(doc)} single-page PDFs in '{output_dir}/'")

def extract_page_range(pdf_path, start_page, end_page, output_path):
    """Extract a specific page range to new PDF"""
    doc = fitz.open(pdf_path)
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=start_page-1, to_page=end_page-1)
    new_doc.save(output_path)
    new_doc.close()
    doc.close()
    print(f"✅ Extracted pages {start_page}-{end_page} to: {output_path}")

if __name__ == "__main__":
    pdf_file = "pavlyuk_tanets_nedoumka_e27087_470337.pdf"

    # 1. Get PDF info
    print("=" * 60)
    print("1. PDF INFORMATION")
    print("=" * 60)
    info = get_pdf_info(pdf_file)
    print(f"File: {info['filename']}")
    print(f"Pages: {info['page_count']}")
    print(f"Size: {info['file_size_mb']:.2f} MB")
    print(f"Title: {info['metadata'].get('title', 'N/A')}")
    print(f"Author: {info['metadata'].get('author', 'N/A')}")

    # 2. Demonstrate page-by-page loading
    print("\n" + "=" * 60)
    print("2. PAGE-BY-PAGE LOADING (First 3 pages)")
    print("=" * 60)
    chunk_load_pages(pdf_file, max_pages=3)

    # 3. Ask before splitting (to avoid cluttering)
    print("=" * 60)
    print("3. SPLIT PDF INTO SINGLE PAGES")
    print("=" * 60)
    print("To split the entire PDF, uncomment the line below:")
    print("# split_pdf_to_single_pages(pdf_file, output_dir='pages')")
    print("\nOr to split just first 5 pages:")
    # split_pdf_to_single_pages(pdf_file, output_dir='pages')  # Uncomment to run
