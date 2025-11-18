#!/usr/bin/env python3
"""
Generate EPUB from English translation.

Usage:
    python3 scripts/generate-epub.py --output translation.epub
    python3 scripts/generate-epub.py --output translation.epub --include-uncertainties
"""

import argparse
import re
from pathlib import Path
from typing import List, Dict, Any

try:
    from ebooklib import epub
    EBOOKLIB_AVAILABLE = True
except ImportError:
    EBOOKLIB_AVAILABLE = False
    print("⚠ Warning: ebooklib not installed. Install with: pip install ebooklib")

REPO_ROOT = Path(__file__).parent.parent


def load_translation_chunks() -> List[Dict[str, Any]]:
    """Load English translation from markdown files."""
    chunks = []

    for chunk_num in range(1, 40):  # 1-39
        translation_file = REPO_ROOT / "book" / "translations" / "v1" / f"translation_chunk_{chunk_num:02d}.md"
        uncertainty_file = REPO_ROOT / "book" / "translations" / "v1" / f"translation_chunk_{chunk_num:02d}_uncertainty.md"

        if not translation_file.exists():
            continue

        with open(translation_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # For reader-friendly output, get clean content without chunk/page headers
        # Remove the main header (# Translation: Pages X-Y (Chunk N/39))
        content = re.sub(r'^#\s+Translation:.*?\n', '', content, flags=re.MULTILINE, count=1)

        # Remove page markers (## Page N)
        content = re.sub(r'^##\s+Page\s+\d+\n', '', content, flags=re.MULTILINE)

        # Clean up excess whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = content.strip()

        # Load uncertainties if file exists
        uncertainties = []
        if uncertainty_file.exists():
            with open(uncertainty_file, 'r', encoding='utf-8') as f:
                unc_content = f.read()

            # Parse uncertainties by page
            page_sections = re.split(r'## Page (\d+)', unc_content)
            for i in range(1, len(page_sections), 2):
                if i + 1 >= len(page_sections):
                    break

                page_num = int(page_sections[i])
                section_content = page_sections[i + 1]

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

        chunks.append({
            "chunk_number": chunk_num,
            "content": content,
            "uncertainties": uncertainties
        })

    return chunks


def markdown_to_html(text: str) -> str:
    """Convert simple markdown to HTML."""
    html = text

    # Headers
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Bold and italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Paragraphs (double newline)
    paragraphs = html.split('\n\n')
    html_parts = []
    for para in paragraphs:
        para = para.strip()
        if para:
            # Check if it's already a tag
            if para.startswith('<h') or para.startswith('<ul') or para.startswith('<ol'):
                html_parts.append(para)
            else:
                html_parts.append(f'<p>{para}</p>')

    return '\n'.join(html_parts)


def generate_epub(output_path: Path, include_uncertainties: bool = False):
    """Generate EPUB from English translation."""
    if not EBOOKLIB_AVAILABLE:
        print("❌ Error: ebooklib is required for EPUB generation")
        print("   Install with: pip install ebooklib")
        return

    print(f"📖 Generating EPUB: {output_path}")
    print(f"   Include uncertainties: {include_uncertainties}")

    # Load translation data
    print("   Loading translation chunks...")
    chunks = load_translation_chunks()
    print(f"   Loaded {len(chunks)} chunks")

    # Create EPUB book
    book = epub.EpubBook()

    # Metadata
    book.set_identifier('dance-of-the-fool-translation')
    book.set_title('The Dance of the Fool')
    book.add_author('Illarion Pavlyuk')
    book.set_language('en')

    # Add description
    if include_uncertainties:
        description = 'English translation of "Танець недоумка" by Ілларіон Павлюк, including translator notes and uncertainties.'
    else:
        description = 'English translation of "Танець недоумка" by Ілларіон Павлюк.'

    book.add_metadata('DC', 'description', description)

    # CSS for styling - font stack with Cyrillic support
    style = '''
    @namespace epub "http://www.idpf.org/2007/ops";

    body {
        font-family: "DejaVu Serif", "Liberation Serif", Georgia, "Times New Roman", serif;
        font-size: 1em;
        line-height: 1.6;
        margin: 1em;
        page-break-before: always;
    }

    h1 {
        font-size: 2em;
        margin-top: 1em;
        margin-bottom: 0.5em;
        text-align: center;
    }

    h2 {
        font-size: 1.5em;
        margin-top: 1em;
        margin-bottom: 0.5em;
        color: #2563EB;
    }

    h3 {
        font-size: 1.2em;
        margin-top: 0.8em;
        margin-bottom: 0.4em;
        color: #4B5563;
    }

    h4 {
        font-size: 1.1em;
        margin-top: 0.6em;
        margin-bottom: 0.3em;
    }

    p {
        margin-bottom: 1em;
        text-align: justify;
    }

    .uncertainty-box {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1em;
        margin: 1em 0;
        font-size: 0.9em;
    }

    .uncertainty-box strong {
        color: #92400E;
    }

    .page-break {
        page-break-after: always;
    }

    .chunk-header {
        margin-top: 2em;
        border-bottom: 2px solid #2563EB;
        padding-bottom: 0.3em;
    }
    '''

    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style
    )
    book.add_item(nav_css)

    # Add cover image from webui
    cover_path = REPO_ROOT / "webui" / "public" / "book-cover.png"
    has_cover = False
    if cover_path.exists():
        with open(cover_path, 'rb') as f:
            cover_content = f.read()
        # Add cover image as a regular item for use in title page
        cover_image = epub.EpubImage(
            uid="cover_image",
            file_name="images/cover.png",
            media_type="image/png",
            content=cover_content
        )
        book.add_item(cover_image)
        has_cover = True

    # Create title page
    title_page = epub.EpubHtml(
        title='Title Page',
        file_name='title.xhtml',
        lang='en'
    )

    # Include cover image in title page if it exists
    cover_img_html = ''
    if has_cover:
        cover_img_html = '<img src="images/cover.png" alt="Book Cover" style="max-width: 80%; height: auto; margin-bottom: 2em;"/>'

    title_content = f'''
    <html>
    <head>
        <title>The Dance of the Fool</title>
        <link href="style/nav.css" rel="stylesheet" type="text/css"/>
    </head>
    <body>
        <div style="text-align: center; margin-top: 3em;">
            {cover_img_html}
            <h1>The Dance of the Fool</h1>
            <h1 style="font-style: italic;">Танець недоумка</h1>
            <p style="margin-top: 2em; font-size: 1.2em;">by</p>
            <p style="font-size: 1.5em;">Illarion Pavlyuk</p>
            <p style="font-size: 1.2em; font-style: italic;">Ілларіон Павлюк</p>
            <p style="margin-top: 3em; color: #666;">English Translation</p>
            {'<p style="font-size: 0.9em; color: #666;">(with translator notes)</p>' if include_uncertainties else ''}
        </div>
    </body>
    </html>
    '''
    title_page.content = title_content
    book.add_item(title_page)

    # Track all chapters for spine and TOC
    all_chapters = [title_page]
    toc = []

    # Process each chunk, combining content naturally without chunk headers
    # Group into larger chapters (every 6-7 chunks)
    chapter_size = 7
    chapter_num = 1

    for chunk_start in range(0, len(chunks), chapter_size):
        chunk_group = chunks[chunk_start:min(chunk_start + chapter_size, len(chunks))]

        first_chunk = chunk_group[0]['chunk_number']
        last_chunk = chunk_group[-1]['chunk_number']

        print(f"   Creating chapter {chapter_num} (chunks {first_chunk:02d}-{last_chunk:02d})...")

        # Create chapter
        chapter = epub.EpubHtml(
            title=f'Chapter {chapter_num}',
            file_name=f'chapter_{chapter_num:02d}.xhtml',
            lang='en'
        )

        # Build chapter content - collect all text first
        all_content = []

        for chunk in chunk_group:
            content = chunk['content']
            uncertainties = chunk['uncertainties']
            print(f"      Processing chunk {chunk['chunk_number']:02d}")

            # Skip empty chunks
            if not content.strip():
                continue

            # Convert markdown to HTML
            html_content = markdown_to_html(content)
            if html_content.strip():
                all_content.append(html_content)

            # Add uncertainties at end of chunk if requested
            if include_uncertainties and uncertainties:
                # Group uncertainties by page
                unc_by_page = {}
                for unc in uncertainties:
                    page_num = unc['page_number']
                    if page_num not in unc_by_page:
                        unc_by_page[page_num] = []
                    unc_by_page[page_num].append(unc)

                # Add all uncertainties for this chunk
                for page_num in sorted(unc_by_page.keys()):
                    for unc in unc_by_page[page_num]:
                        unc_html = f'''<div class="uncertainty-box">
<p><strong>Translator's Note (page {page_num}):</strong></p>
<p><strong>Original:</strong> "{unc['original_text']}"</p>
<p><strong>Question:</strong> {unc['question']}</p>
<p><strong>Translation:</strong> "{unc['current_translation']}"</p>
</div>'''
                        all_content.append(unc_html)

        # Build the complete HTML
        body_content = ''.join(all_content)
        chapter_html = f'''<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Chapter {chapter_num}</title>
<link href="style/nav.css" rel="stylesheet" type="text/css"/>
</head>
<body>
{body_content}
</body>
</html>'''

        chapter.content = chapter_html
        print(f"      Chapter has {len(all_content)} content sections, {len(body_content)} chars")
        book.add_item(chapter)
        all_chapters.append(chapter)

        # Add to TOC
        toc.append(epub.Link(f'chapter_{chapter_num:02d}.xhtml', f'Chapter {chapter_num}', f'chapter{chapter_num}'))

        chapter_num += 1

    # Define TOC
    book.toc = tuple(toc)

    # Add NCX and Nav files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define spine (reading order)
    book.spine = all_chapters

    # Build EPUB
    print("   Building EPUB...")
    epub.write_epub(str(output_path), book)

    print(f"✓ EPUB generated: {output_path}")
    print(f"  File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")


def main():
    parser = argparse.ArgumentParser(
        description='Generate EPUB from English translation'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=REPO_ROOT / 'translation_english.epub',
        help='Output EPUB file path'
    )
    parser.add_argument(
        '--include-uncertainties',
        action='store_true',
        help='Include translator notes/uncertainties in the EPUB'
    )

    args = parser.parse_args()

    generate_epub(args.output, args.include_uncertainties)


if __name__ == '__main__':
    main()
