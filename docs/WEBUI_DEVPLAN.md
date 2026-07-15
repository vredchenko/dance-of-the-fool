# Web UI Development Plan: Translation Proofreading Interface

**Project:** "Танець недоумка" (The Dance of the Fool) - Translation Review Interface
**Goal:** Server-side-generated static website for side-by-side proofreading of Ukrainian-English translation
**Target:** Static hosting (GitHub Pages, Netlify, Vercel, etc.)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Technology Stack](#technology-stack)
3. [Architecture Overview](#architecture-overview)
4. [Data Structure & Processing](#data-structure--processing)
5. [UI/UX Design](#uiux-design)
6. [Feature Specifications](#feature-specifications)
7. [File Structure](#file-structure)
8. [Build Pipeline](#build-pipeline)
9. [Development Phases](#development-phases)
10. [Deployment Strategy](#deployment-strategy)
11. [Future Enhancements](#future-enhancements)

---

## Executive Summary

Build a modern, responsive static website that presents the complete Ukrainian-to-English translation of "Танець недоумка" in a proofreader-friendly format. The site will display:

- **Ukrainian source text** (from JSON chunks)
- **English translation** (from markdown files)
- **Translation uncertainties** (from uncertainty markdown files)

All content will be generated at build time (SSG - Static Site Generation) for optimal performance and easy hosting.

---

## Technology Stack

### Core Framework: **Astro** (Recommended)

**Why Astro:**
- Zero JavaScript by default (fast page loads)
- Excellent markdown support (can import .md directly)
- Built-in SSG capabilities
- Component-based architecture (can use React/Vue/Svelte if needed)
- Outstanding DX (developer experience)
- Perfect for content-heavy sites
- Built-in syntax highlighting for code blocks

**Alternative Options:**
1. **Next.js** (SSG mode) - More complex but powerful, good for future interactivity
2. **Eleventy (11ty)** - Minimal, flexible, JavaScript-based
3. **Hugo** - Extremely fast, Go-based, steeper learning curve

### Styling: **Tailwind CSS**

**Why Tailwind:**
- Utility-first CSS for rapid UI development
- Excellent responsive design support
- Dark mode built-in
- Small bundle size with PurgeCSS
- Great typography plugin for long-form text

### Additional Dependencies

```json
{
  "dependencies": {
    "astro": "^4.0.0",
    "tailwindcss": "^3.4.0",
    "@astrojs/tailwind": "^5.0.0",
    "@astrojs/mdx": "^2.0.0"
  },
  "devDependencies": {
    "gray-matter": "^4.0.3",      // Parse markdown frontmatter
    "marked": "^11.0.0",          // Additional markdown processing if needed
    "prettier": "^3.1.0",
    "prettier-plugin-astro": "^0.12.0"
  }
}
```

---

## Architecture Overview

### High-Level Flow

```
Source Data (Git Repo)
├── chunk_*.json (39 files)           → Ukrainian text by page
├── translation_chunk_*.md (39 files) → English translations
└── translation_chunk_*_uncertainty.md (39 files) → Translation notes

                    ↓

Build Script (Python/Node.js)
├── Parse all JSON chunks
├── Parse all markdown files
├── Combine into structured data
└── Generate index/manifest JSON

                    ↓

Astro SSG Build
├── Read manifest data
├── Generate HTML pages
│   ├── Homepage (overview)
│   ├── Chunk pages (01-39)
│   └── Full continuous reading view
└── Apply styling/responsive design

                    ↓

Static Output (dist/)
└── Deployable HTML/CSS/JS bundle
```

### Page Structure

1. **Homepage** (`/`)
   - Overview of the book
   - Translation progress (39/39 complete)
   - Navigation to chunks
   - Search functionality

2. **Chunk Pages** (`/chunk/01` through `/chunk/39`)
   - Side-by-side Ukrainian/English view
   - Uncertainty panel (if applicable)
   - Navigation between chunks
   - Per-page breakdown

3. **Continuous Reading View** (`/read/full`)
   - All English text in reading order
   - Optional: All Ukrainian text view
   - Printable format

4. **Uncertainty Index** (`/uncertainties`)
   - Compiled list of all translation questions
   - Organized by chunk and page
   - Quick navigation to specific issues

---

## Data Structure & Processing

### Step 1: Data Aggregation Script

Create `scripts/build-data.py` (or `.mjs` for Node.js):

```python
#!/usr/bin/env python3
"""
Aggregate translation data into structured JSON for Astro
"""
import json
import re
from pathlib import Path
from typing import List, Dict, Any

OUTPUT_FILE = "src/data/translation-data.json"

def parse_chunk_json(chunk_num: int) -> Dict[str, Any]:
    """Parse Ukrainian source from chunk_XX.json"""
    path = Path(f"chunk_{chunk_num:02d}.json")
    with open(path, 'r', encoding='utf-8') as f:
        pages = json.load(f)

    return {
        "chunk_number": chunk_num,
        "pages": [
            {
                "page_number": p["page"],
                "ukrainian_text": p["text"],
                "char_count": p["char_count"],
                "word_count": p["word_count"]
            }
            for p in pages
        ]
    }

def parse_translation_md(chunk_num: int) -> Dict[str, Any]:
    """Parse English translation from markdown"""
    path = Path(f"translation_chunk_{chunk_num:02d}.md")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract page sections
    # Pattern: ### Page N followed by content until next ### Page or end
    pages = []
    page_pattern = re.compile(r'### Page (\d+)\n\n(.*?)(?=### Page|\Z)', re.DOTALL)

    for match in page_pattern.finditer(content):
        page_num = int(match.group(1))
        page_content = match.group(2).strip()
        pages.append({
            "page_number": page_num,
            "english_text": page_content
        })

    return pages

def parse_uncertainty_md(chunk_num: int) -> List[Dict[str, str]]:
    """Parse uncertainty notes from markdown"""
    path = Path(f"translation_chunk_{chunk_num:02d}_uncertainty.md")

    if not path.exists():
        return []

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    uncertainties = []
    # Pattern: ## Page N ... **Original:** ... **Question:** ... **Current translation:**
    page_pattern = re.compile(
        r'## Page (\d+)\n\*\*Original:\*\* "(.*?)"\n\*\*Question:\*\* (.*?)\n\*\*Current translation:\*\* "(.*?)"',
        re.DOTALL
    )

    for match in page_pattern.finditer(content):
        uncertainties.append({
            "page_number": int(match.group(1)),
            "original_text": match.group(2),
            "question": match.group(3),
            "current_translation": match.group(4)
        })

    return uncertainties

def build_complete_data() -> List[Dict[str, Any]]:
    """Build complete translation dataset"""
    chunks = []

    for chunk_num in range(1, 40):  # 1-39
        print(f"Processing chunk {chunk_num:02d}...")

        # Get Ukrainian source
        ukrainian_data = parse_chunk_json(chunk_num)

        # Get English translation
        english_pages = parse_translation_md(chunk_num)

        # Get uncertainties
        uncertainties = parse_uncertainty_md(chunk_num)

        # Merge data by page number
        page_map = {}

        # Add Ukrainian text
        for page in ukrainian_data["pages"]:
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

        chunks.append({
            "chunk_number": chunk_num,
            "page_range": f"{start_page}-{end_page}",
            "start_page": start_page,
            "end_page": end_page,
            "pages": [page_map[pn] for pn in page_numbers]
        })

    return chunks

def main():
    """Main entry point"""
    print("Building translation data...")

    chunks = build_complete_data()

    # Create output directory
    Path("src/data").mkdir(parents=True, exist_ok=True)

    # Write JSON
    output_data = {
        "book_title": "Танець недоумка / The Dance of the Fool",
        "author": "Ілларіон Павлюк / Illarion Pavlyuk",
        "total_chunks": len(chunks),
        "total_pages": 468,
        "chunks": chunks
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"✓ Written {len(chunks)} chunks to {OUTPUT_FILE}")
    print(f"  Total pages: {sum(len(c['pages']) for c in chunks)}")

if __name__ == "__main__":
    main()
```

### Step 2: Generated Data Format

Output: `src/data/translation-data.json`

```json
{
  "book_title": "Танець недоумка / The Dance of the Fool",
  "author": "Ілларіон Павлюк / Illarion Pavlyuk",
  "total_chunks": 39,
  "total_pages": 468,
  "chunks": [
    {
      "chunk_number": 1,
      "page_range": "1-12",
      "start_page": 1,
      "end_page": 12,
      "pages": [
        {
          "page_number": 1,
          "ukrainian_text": "",
          "char_count": 0,
          "word_count": 0,
          "english_text": "*(Cover page - no text)*",
          "uncertainties": []
        },
        {
          "page_number": 2,
          "ukrainian_text": "Annotation\n...",
          "char_count": 669,
          "word_count": 95,
          "english_text": "**Annotation**\n\nSpace biologist Gil...",
          "uncertainties": [
            {
              "original": "планеті Іш-Чель",
              "question": "Planet name transliteration...",
              "translation": "planet Ix-Chel"
            }
          ]
        }
      ]
    }
  ]
}
```

---

## UI/UX Design

### Design Principles

1. **Readability First**: Large, comfortable fonts; ample whitespace
2. **Side-by-Side Comparison**: Ukrainian and English in parallel columns
3. **Non-Intrusive Annotations**: Uncertainties visible but not distracting
4. **Responsive**: Works on desktop (primary) and mobile
5. **Dark Mode Support**: For extended reading sessions
6. **Printable**: Clean print stylesheet for physical proofreading

### Layout Wireframes

#### Desktop Layout (Chunk Page)

```
┌─────────────────────────────────────────────────────────────┐
│ [Header: Book Title + Navigation]                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Chunk 01 • Pages 1-12                      [< Prev | Next >]│
│                                                             │
├──────────────────────┬──────────────────────────────────────┤
│                      │                                      │
│  UKRAINIAN (UK)      │  ENGLISH (EN)                       │
│  Page 2              │  Page 2                             │
│  ─────────           │  ─────────                          │
│                      │                                      │
│  Annotation          │  **Annotation**                     │
│  Космічний біолог... │  Space biologist Gil...             │
│  ...                 │  ...                                │
│                      │                                      │
│  [1 uncertainty]     │  [Show note]                        │
│                      │                                      │
├──────────────────────┴──────────────────────────────────────┤
│                                                             │
│ [Uncertainty Panel - Expandable]                           │
│ ⚠ планеті Іш-Чель                                          │
│   Q: Planet name transliteration - using "Ix-Chel"         │
│   Translation: "planet Ix-Chel"                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Mobile Layout (Stacked)

```
┌─────────────────────┐
│ [☰ Menu]            │
│ Chunk 01 (1-12)     │
├─────────────────────┤
│ [UK] [EN] [Both]    │← Tab switcher
├─────────────────────┤
│                     │
│ Page 2              │
│ ───────             │
│                     │
│ Annotation          │
│ Космічний біолог... │
│ ...                 │
│                     │
│ [Show English ↓]    │
│                     │
├─────────────────────┤
│ ⚠ 1 uncertainty     │
└─────────────────────┘
```

### Color Scheme

**Light Mode:**
- Background: `#FAFAFA` (warm gray)
- Ukrainian column: `#FFFFFF` (white)
- English column: `#F8F9FA` (light gray)
- Uncertainty panel: `#FFF3CD` (soft yellow)
- Text: `#1A1A1A` (dark gray)
- Accent: `#2563EB` (blue)

**Dark Mode:**
- Background: `#1A1A1A`
- Ukrainian column: `#2A2A2A`
- English column: `#232323`
- Uncertainty panel: `#3D3929`
- Text: `#E5E5E5`
- Accent: `#60A5FA`

### Typography

```css
/* Ukrainian Text */
font-family: 'Georgia', 'Times New Roman', serif;
font-size: 18px;
line-height: 1.7;

/* English Text */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
font-size: 17px;
line-height: 1.6;

/* Headings */
font-family: 'Inter', sans-serif;
font-weight: 600;

/* Code/Technical */
font-family: 'JetBrains Mono', 'Consolas', monospace;
```

---

## Feature Specifications

### 1. Homepage Features

- [ ] Book metadata (title, author, total pages)
- [ ] Translation completion status (39/39 chunks)
- [ ] Visual chunk navigator (grid of clickable chunk cards)
- [ ] Quick stats (total words, total uncertainties)
- [ ] Search bar (search across all content)
- [ ] Dark mode toggle

### 2. Chunk Page Features

- [ ] Split-pane layout (Ukrainian | English)
- [ ] Page-by-page breakdown within chunk
- [ ] Uncertainty indicators (icon/badge on pages with notes)
- [ ] Expandable uncertainty panel
- [ ] Previous/Next chunk navigation
- [ ] Jump to specific page
- [ ] Copy text button (for each column)
- [ ] Highlight matching paragraphs on scroll
- [ ] Bookmark/annotation support (localStorage)

### 3. Navigation Features

- [ ] Sticky header with chunk selector dropdown
- [ ] Keyboard shortcuts:
  - `←/→` Previous/Next chunk
  - `[/]` Previous/Next page within chunk
  - `D` Toggle dark mode
  - `/` Focus search
  - `?` Show keyboard shortcuts help

### 4. Search Feature

- [ ] Full-text search across Ukrainian and English
- [ ] Highlight search results in context
- [ ] Navigate between search results
- [ ] Filter by language (UK/EN/Both)
- [ ] Search within uncertainties

### 5. Reading View Features

- [ ] Continuous scroll of all English text
- [ ] Table of contents sidebar
- [ ] Reading progress indicator
- [ ] Adjustable font size
- [ ] Export to PDF/EPUB (future)

### 6. Uncertainty Management

- [ ] Visual indicators on pages with translation questions
- [ ] Expandable detail panels
- [ ] Categorization by severity (if added to source)
- [ ] Comment/resolution tracking (future interactive feature)

---

## File Structure

```
dance-of-the-fool/
├── public/                      # Static assets
│   ├── favicon.ico
│   └── fonts/
│       ├── inter.woff2
│       └── jetbrains-mono.woff2
│
├── src/
│   ├── components/              # Astro/React components
│   │   ├── Header.astro
│   │   ├── ChunkNavigator.astro
│   │   ├── PageView.astro
│   │   ├── UncertaintyPanel.astro
│   │   ├── SearchBar.astro
│   │   └── DarkModeToggle.astro
│   │
│   ├── layouts/
│   │   ├── BaseLayout.astro    # Base HTML structure
│   │   └── ChunkLayout.astro   # Layout for chunk pages
│   │
│   ├── pages/
│   │   ├── index.astro         # Homepage
│   │   ├── chunk/
│   │   │   └── [id].astro      # Dynamic chunk pages
│   │   ├── read/
│   │   │   └── full.astro      # Continuous reading view
│   │   └── uncertainties/
│   │       └── index.astro     # Uncertainty index
│   │
│   ├── data/
│   │   └── translation-data.json  # Generated by build script
│   │
│   └── styles/
│       └── global.css          # Global styles + Tailwind
│
├── scripts/
│   ├── build-data.py           # Aggregate source data
│   └── validate-data.py        # Data integrity checks
│
├── astro.config.mjs            # Astro configuration
├── tailwind.config.mjs         # Tailwind configuration
├── package.json
└── WEBUI_DEVPLAN.md           # This file
```

---

## Build Pipeline

### Development Workflow

```bash
# 1. Install dependencies
npm install

# 2. Build data from source files
python scripts/build-data.py

# 3. Start dev server
npm run dev
# → Opens http://localhost:4321

# 4. Build for production
npm run build
# → Outputs to dist/

# 5. Preview production build
npm run preview
```

### package.json Scripts

```json
{
  "name": "dance-of-the-fool-translation",
  "version": "1.0.0",
  "scripts": {
    "prebuild": "python3 scripts/build-data.py",
    "dev": "npm run prebuild && astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "validate": "python3 scripts/validate-data.py",
    "format": "prettier --write ."
  }
}
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Build data
        run: python3 scripts/build-data.py

      - name: Build site
        run: npm run build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## Development Phases

### Phase 1: Foundation (Week 1)

**Goal:** Basic structure and data pipeline

- [ ] Set up Astro project
- [ ] Configure Tailwind CSS
- [ ] Write `build-data.py` script
- [ ] Generate `translation-data.json`
- [ ] Create base layout component
- [ ] Implement homepage with chunk list
- [ ] Set up routing for chunk pages

**Deliverable:** Static site with navigable chunks (no styling)

---

### Phase 2: Core UI (Week 2)

**Goal:** Polished reading experience

- [ ] Design and implement split-pane layout
- [ ] Style Ukrainian and English columns
- [ ] Implement page-by-page rendering within chunks
- [ ] Add navigation controls (prev/next)
- [ ] Implement dark mode toggle
- [ ] Responsive design for mobile

**Deliverable:** Functional, styled chunk reading interface

---

### Phase 3: Uncertainty Integration (Week 3)

**Goal:** Display translation notes

- [ ] Create UncertaintyPanel component
- [ ] Add uncertainty indicators to pages
- [ ] Implement expandable detail view
- [ ] Build uncertainties index page
- [ ] Link from chunk pages to uncertainty details

**Deliverable:** Complete uncertainty tracking system

---

### Phase 4: Enhanced Features (Week 4)

**Goal:** Search and reading improvements

- [ ] Implement full-text search
- [ ] Create continuous reading view
- [ ] Add keyboard shortcuts
- [ ] Implement bookmark/notes (localStorage)
- [ ] Add copy-text functionality
- [ ] Print stylesheet

**Deliverable:** Feature-complete proofreading interface

---

### Phase 5: Polish & Deploy (Week 5)

**Goal:** Production-ready site

- [ ] Performance optimization
- [ ] Accessibility audit (WCAG 2.1)
- [ ] Cross-browser testing
- [ ] Mobile testing
- [ ] Write user documentation
- [ ] Set up CI/CD pipeline
- [ ] Deploy to GitHub Pages/Netlify

**Deliverable:** Live, publicly accessible website

---

## Deployment Strategy

### Hosting Options

1. **GitHub Pages** (Recommended for simplicity)
   - Free for public repos
   - Easy CI/CD with GitHub Actions
   - Custom domain support
   - URL: `https://username.github.io/dance-of-the-fool/`

2. **Netlify** (Recommended for features)
   - Free tier with 100GB bandwidth
   - Automatic deployments from Git
   - Branch previews
   - Form handling (for feedback)
   - URL: `https://dance-of-the-fool.netlify.app`

3. **Vercel**
   - Similar to Netlify
   - Excellent DX
   - Fast global CDN

### Deployment Checklist

- [ ] Configure base path in `astro.config.mjs`
- [ ] Set up custom domain (optional)
- [ ] Enable HTTPS
- [ ] Add `sitemap.xml` generation
- [ ] Configure analytics (optional, privacy-friendly)
- [ ] Set up error tracking (optional)
- [ ] Add meta tags for social sharing (OG tags)

### Custom Domain Setup (Optional)

If deploying to custom domain (e.g., `translation.example.com`):

1. Purchase domain
2. Add DNS records:
   ```
   CNAME translation username.github.io
   ```
3. Configure in repo settings
4. Update `astro.config.mjs`:
   ```js
   export default defineConfig({
     site: 'https://translation.example.com'
   });
   ```

---

## Future Enhancements

### Phase 6+ (Post-Launch)

1. **Interactive Features**
   - User comments/annotations (requires backend or GitHub integration)
   - Collaborative proofreading mode
   - Version history/changelog

2. **Advanced Search**
   - Fuzzy search
   - Regular expression support
   - Search result export

3. **Export Options**
   - Generate EPUB from translation
   - PDF export (with proper formatting)
   - DOCX export for editors

4. **Analytics**
   - Reading time estimates
   - Most-viewed chunks
   - Uncertainty resolution tracking

5. **Accessibility**
   - Text-to-speech integration
   - High-contrast mode
   - Screen reader optimization
   - Translation quality metrics

6. **AI Integration**
   - Alternative translation suggestions
   - Consistency checker (terminology)
   - Style guide enforcement

---

## Technical Considerations

### Performance Targets

- Lighthouse score: 95+ across all categories
- First Contentful Paint (FCP): < 1.0s
- Time to Interactive (TTI): < 2.0s
- Total bundle size: < 200KB (excluding fonts)
- Image optimization: WebP with fallbacks

### SEO Optimization

- Semantic HTML structure
- Meta descriptions for each chunk
- Structured data (Book schema)
- Sitemap generation
- Canonical URLs

### Accessibility (WCAG 2.1 AA)

- Keyboard navigation support
- ARIA labels for dynamic content
- Sufficient color contrast (4.5:1 for text)
- Focus indicators
- Skip navigation links
- Alt text for all images

### Browser Support

- Chrome/Edge (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Mobile browsers (iOS Safari, Chrome Android)

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Data parsing errors | High | Write comprehensive validation script |
| Large page load times | Medium | Implement pagination, lazy loading |
| Markdown rendering inconsistencies | Medium | Use tested markdown parser, preview all chunks |
| Mobile layout issues | Medium | Test early and often on real devices |
| Unicode/Cyrillic display issues | Low | Use web-safe fonts with Cyrillic support |

---

## Success Metrics

1. **Functionality**
   - All 39 chunks render correctly
   - All uncertainties are visible and accessible
   - Navigation works smoothly
   - Search returns accurate results

2. **Performance**
   - Page load time < 2 seconds on 3G
   - Lighthouse score > 90

3. **Usability**
   - Can proofread entire book without friction
   - Easy to compare Ukrainian and English side-by-side
   - Mobile-friendly for on-the-go review

4. **Maintainability**
   - Easy to update translation data
   - Clear build process
   - Well-documented codebase

---

## Open Questions

1. **Paragraph Alignment**: Should we attempt to align Ukrainian and English paragraphs for easier comparison?
2. **Comments/Feedback**: Do we need a feedback mechanism for proofreaders? (Could use GitHub Issues)
3. **Print Layout**: Should we provide a special "print-optimized" view?
4. **Multi-column on Mobile**: Should tablets (portrait) show side-by-side or stacked layout?
5. **Progressive Web App**: Would offline access be valuable? (PWA features)

---

## Appendix: Quick Start Commands

Once this plan is approved and development begins:

```bash
# Initialize Astro project
npm create astro@latest dance-translation -- --template minimal --typescript

# Add Tailwind
npx astro add tailwind

# Add MDX (for markdown processing)
npx astro add mdx

# Install additional dependencies
npm install gray-matter marked

# Create scripts directory
mkdir -p scripts

# Create data aggregation script
# (Copy build-data.py from this plan)

# Build and run
python3 scripts/build-data.py
npm run dev
```

---

**Document Version:** 1.0
**Last Updated:** 2025-11-15
**Status:** Draft - Awaiting Approval
**Author:** Claude (AI Assistant)
**Reviewer:** Valerii Redchenko
