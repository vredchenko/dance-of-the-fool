# GitHub Actions Workflows

This directory contains CI/CD workflows for building translation outputs.

## Available Workflows

All workflows are **manual dispatch only** - they must be triggered manually from the GitHub Actions tab.

### 1. Build All Outputs (`build-outputs.yml`)

**Trigger:** Manual dispatch with options

Builds all translation outputs in parallel jobs. You can selectively enable/disable each output type.

**Options:**
- `build_webui` - Build WebUI static bundle (default: true)
- `build_pdf` - Build PDF exports (default: true)
- `build_epub` - Build EPUB exports (default: true)

**Outputs:**
- `webui-bundle-<sha>` - Static webui bundle in `webui/dist/`
- `pdf-exports-<sha>` - Both PDF files in `dist/`:
  - `Illarion_Pavlyuk_Fools_Dance_translation_<sha>.pdf`
  - `Illarion_Pavlyuk_Fools_Dance_translation_with_annotations_<sha>.pdf`
- `epub-exports-<sha>` - Both EPUB files in `dist/`:
  - `Illarion_Pavlyuk_Fools_Dance_translation_<sha>.epub`
  - `Illarion_Pavlyuk_Fools_Dance_translation_with_annotations_<sha>.epub`

### 2. Build WebUI Only (`build-webui.yml`)

**Trigger:** Manual dispatch

Builds only the static webui bundle. The generated bundle includes a commit SHA badge in the header that links back to the commit on GitHub.

**Outputs:**
- `webui-bundle-<sha>` - Static bundle ready for deployment

### 3. Build PDF Only (`build-pdf.yml`)

**Trigger:** Manual dispatch

Builds both PDF versions (with and without translator annotations).

**Outputs:**
- `pdf-exports-<sha>` containing both PDFs with commit SHA in filename

### 4. Build EPUB Only (`build-epub.yml`)

**Trigger:** Manual dispatch

Builds both EPUB versions (with and without translator annotations).

**Outputs:**
- `epub-exports-<sha>` containing both EPUBs with commit SHA in filename

## How to Trigger Workflows

1. Go to the **Actions** tab in GitHub
2. Select the workflow you want to run from the left sidebar
3. Click **Run workflow** button (top right)
4. For `build-outputs.yml`, you can toggle which outputs to build
5. Click **Run workflow** to start

## Commit SHA Encoding

All generated artifacts encode the commit SHA they were built from:

- **PDFs & EPUBs**: Included in filename (first 7 characters)
  - Example: `Illarion_Pavlyuk_Fools_Dance_translation_a1b2c3d.pdf`
- **WebUI**: Badge in header linking to commit on GitHub
  - Only visible when built via CI/CD (uses `PUBLIC_COMMIT_SHA` env var)

## Artifacts

All artifacts are retained for **90 days** and can be downloaded from:
- The workflow run summary page
- The Actions tab → Select the workflow run → Scroll to "Artifacts"

## Dependencies

Workflows automatically install required dependencies:
- Python 3.11
- ReportLab (for PDF generation)
- ebooklib (for EPUB generation)
- Node.js 20 (for webui build)
- DejaVu fonts (for Ukrainian/Cyrillic support in PDFs)

## Local Testing

To test builds locally before pushing:

```bash
# WebUI
python3 tools/build-webui-data.py
cd webui && npm ci && npm run build

# PDF
python3 tools/generate-pdf.py --output dist/test.pdf
python3 tools/generate-pdf.py --output dist/test-notes.pdf --include-uncertainties

# EPUB
python3 tools/generate-epub.py --output dist/test.epub
python3 tools/generate-epub.py --output dist/test-notes.epub --include-uncertainties

# Or regenerate everything
./regenerate-all.sh
# or
python3 tools/regenerate_all.py
```
