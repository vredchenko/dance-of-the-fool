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
        translation_file = REPO_ROOT / f"translation_chunk_{chunk_num:02d}.md"
        uncertainty_file = REPO_ROOT / f"translation_chunk_{chunk_num:02d}_uncertainty.md"

        if not translation_file.exists():
            continue

        with open(translation_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract page sections
        pages = []
        page_splits = re.split(r'### Page (\d+)', content)

        for i in range(1, len(page_splits), 2):
            if i + 1 >= len(page_splits):
                break

            page_num = int(page_splits[i])
            page_content = page_splits[i + 1]
            page_content = re.sub(r'\n---+\n', '\n', page_content).strip()

            pages.append({
                "page_number": page_num,
                "content": page_content
            })

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
            "pages": pages,
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

    # CSS for styling
    style = '''
    @namespace epub "http://www.idpf.org/2007/ops";

    body {
        font-family: Georgia, serif;
        line-height: 1.6;
        margin: 1em;
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

    # Create title page
    title_page = epub.EpubHtml(
        title='Title Page',
        file_name='title.xhtml',
        lang='en'
    )

    title_content = f'''
    <html>
    <head>
        <title>The Dance of the Fool</title>
        <link href="style/nav.css" rel="stylesheet" type="text/css"/>
    </head>
    <body>
        <div style="text-align: center; margin-top: 3em;">
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

    # Process each chunk
    for chunk in chunks:
        chunk_num = chunk['chunk_number']
        pages = chunk['pages']
        uncertainties = chunk['uncertainties']

        print(f"   Processing chunk {chunk_num:02d}...")

        # Group uncertainties by page
        unc_by_page = {}
        for unc in uncertainties:
            page_num = unc['page_number']
            if page_num not in unc_by_page:
                unc_by_page[page_num] = []
            unc_by_page[page_num].append(unc)

        # Create chapter for this chunk
        chapter = epub.EpubHtml(
            title=f'Chunk {chunk_num:02d}',
            file_name=f'chunk_{chunk_num:02d}.xhtml',
            lang='en'
        )

        # Build chapter content
        content_parts = [
            '<html>',
            '<head>',
            f'<title>Chunk {chunk_num:02d}</title>',
            '<link href="style/nav.css" rel="stylesheet" type="text/css"/>',
            '</head>',
            '<body>',
            f'<h2 class="chunk-header">Chunk {chunk_num:02d}</h2>'
        ]

        for page in pages:
            page_num = page['page_number']
            page_content = page['content']

            # Page header
            content_parts.append(f'<h3>Page {page_num}</h3>')

            # Convert markdown to HTML
            html_content = markdown_to_html(page_content)
            content_parts.append(html_content)

            # Add uncertainties if requested
            if include_uncertainties and page_num in unc_by_page:
                for unc in unc_by_page[page_num]:
                    unc_html = f'''
                    <div class="uncertainty-box">
                        <p><strong>Translator's Note:</strong></p>
                        <p><strong>Original:</strong> "{unc['original_text']}"</p>
                        <p><strong>Question:</strong> {unc['question']}</p>
                        <p><strong>Translation:</strong> "{unc['current_translation']}"</p>
                    </div>
                    '''
                    content_parts.append(unc_html)

        content_parts.append('</body>')
        content_parts.append('</html>')

        chapter.content = '\n'.join(content_parts)
        book.add_item(chapter)
        all_chapters.append(chapter)

        # Add to TOC (every 5 chunks for cleaner navigation)
        if chunk_num % 5 == 1 or chunk_num == 1:
            toc.append(epub.Link(f'chunk_{chunk_num:02d}.xhtml', f'Chunk {chunk_num:02d}', f'chunk{chunk_num}'))

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
