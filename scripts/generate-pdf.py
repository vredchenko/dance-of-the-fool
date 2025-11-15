#!/usr/bin/env python3
"""
Generate PDF from English translation.

Usage:
    python3 scripts/generate-pdf.py --output translation.pdf
    python3 scripts/generate-pdf.py --output translation.pdf --include-uncertainties
"""

import argparse
import re
from pathlib import Path
from typing import List, Dict, Any

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak,
        Table, TableStyle, KeepTogether
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠ Warning: reportlab not installed. Install with: pip install reportlab")

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


def markdown_to_flowables(text: str, styles) -> List:
    """Convert markdown text to ReportLab flowables."""
    flowables = []
    lines = text.split('\n')
    current_para = []

    def flush_paragraph():
        if current_para:
            para_text = ' '.join(current_para)
            # Simple markdown conversion
            para_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', para_text)
            para_text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', para_text)
            flowables.append(Paragraph(para_text, styles['BookBody']))
            current_para.clear()

    for line in lines:
        line = line.strip()

        if not line:
            flush_paragraph()
            flowables.append(Spacer(1, 0.1 * inch))
            continue

        # Headers
        if line.startswith('#### '):
            flush_paragraph()
            flowables.append(Paragraph(line[5:], styles['Heading4']))
        elif line.startswith('### '):
            flush_paragraph()
            flowables.append(Paragraph(line[4:], styles['Heading3']))
        elif line.startswith('## '):
            flush_paragraph()
            flowables.append(Paragraph(line[3:], styles['Heading2']))
        elif line.startswith('# '):
            flush_paragraph()
            flowables.append(Paragraph(line[2:], styles['Heading1']))
        else:
            current_para.append(line)

    flush_paragraph()
    return flowables


def register_unicode_fonts():
    """Register TrueType fonts with Unicode (Cyrillic) support."""
    try:
        # Register DejaVu Serif fonts (excellent Unicode support including Cyrillic)
        pdfmetrics.registerFont(TTFont('DejaVuSerif', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))

        # Register DejaVu Sans for headers
        pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

        print("   ✓ Registered Unicode fonts (DejaVu) with Cyrillic support")
        return True
    except Exception as e:
        print(f"   ⚠ Warning: Could not register Unicode fonts: {e}")
        print("   Ukrainian characters may not display correctly")
        return False


def generate_pdf(output_path: Path, include_uncertainties: bool = False):
    """Generate PDF from English translation."""
    if not REPORTLAB_AVAILABLE:
        print("❌ Error: reportlab is required for PDF generation")
        print("   Install with: pip install reportlab")
        return

    print(f"📄 Generating PDF: {output_path}")
    print(f"   Include uncertainties: {include_uncertainties}")

    # Register Unicode fonts
    register_unicode_fonts()

    # Load translation data
    print("   Loading translation chunks...")
    chunks = load_translation_chunks()
    print(f"   Loaded {len(chunks)} chunks")

    # Create PDF
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=0.75*inch
    )

    # Styles
    styles = getSampleStyleSheet()

    # Custom styles with Unicode font support
    styles.add(ParagraphStyle(
        name='BookTitle',
        parent=styles['Heading1'],
        fontName='DejaVuSans-Bold',
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        name='BookSubtitle',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=24,
        textColor=colors.grey
    ))

    styles.add(ParagraphStyle(
        name='ChunkHeader',
        parent=styles['Heading2'],
        fontName='DejaVuSans-Bold',
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#2563EB')
    ))

    styles.add(ParagraphStyle(
        name='PageHeader',
        parent=styles['Heading3'],
        fontName='DejaVuSans-Bold',
        fontSize=12,
        spaceAfter=8,
        textColor=colors.HexColor('#4B5563')
    ))

    styles.add(ParagraphStyle(
        name='BookBody',
        parent=styles['Normal'],
        fontName='DejaVuSerif',
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name='UncertaintyNote',
        parent=styles['Normal'],
        fontName='DejaVuSerif',
        fontSize=9,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=8,
        textColor=colors.HexColor('#92400E'),
        backColor=colors.HexColor('#FEF3C7')
    ))

    # Build document
    story = []

    # Title page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("The Dance of the Fool", styles['BookTitle']))
    story.append(Paragraph("Танець недоумка", styles['BookTitle']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("by Illarion Pavlyuk", styles['BookSubtitle']))
    story.append(Paragraph("Ілларіон Павлюк", styles['BookSubtitle']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("English Translation", styles['BookSubtitle']))
    if include_uncertainties:
        story.append(Paragraph("(with translator notes)", styles['BookSubtitle']))
    story.append(PageBreak())

    # Process each chunk - natural reading flow without chunk/page headers
    for chunk in chunks:
        chunk_num = chunk['chunk_number']
        content = chunk['content']
        uncertainties = chunk['uncertainties']

        print(f"   Processing chunk {chunk_num:02d}...")

        # Skip empty chunks
        if not content.strip():
            continue

        # Convert markdown to flowables (continuous text)
        flowables = markdown_to_flowables(content, styles)
        story.extend(flowables)

        # Add uncertainties at end of chunk if requested
        if include_uncertainties and uncertainties:
            story.append(Spacer(1, 0.2*inch))

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
                    unc_text = f"""
                    <b>Translator's Note (page {page_num}):</b><br/>
                    <b>Original:</b> "{unc['original_text']}"<br/>
                    <b>Question:</b> {unc['question']}<br/>
                    <b>Translation:</b> "{unc['current_translation']}"
                    """
                    story.append(Paragraph(unc_text, styles['UncertaintyNote']))
                    story.append(Spacer(1, 0.1*inch))

            story.append(Spacer(1, 0.2*inch))

    # Build PDF
    print("   Building PDF...")
    doc.build(story)
    print(f"✓ PDF generated: {output_path}")
    print(f"  File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")


def main():
    parser = argparse.ArgumentParser(
        description='Generate PDF from English translation'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=REPO_ROOT / 'translation_english.pdf',
        help='Output PDF file path'
    )
    parser.add_argument(
        '--include-uncertainties',
        action='store_true',
        help='Include translator notes/uncertainties in the PDF'
    )

    args = parser.parse_args()

    generate_pdf(args.output, args.include_uncertainties)


if __name__ == '__main__':
    main()
