# GitHub Actions Workflows

CI/CD for building and publishing the translation outputs.

## Workflows

### `release.yml` — Release (primary)

**Trigger:** pushing a `vX.Y.Z` tag (or manual dispatch with a version input).

Builds every output and publishes a **GitHub Release** with the files attached.
It verifies the pushed tag matches the root `VERSION` file, then builds:

| Asset (stable name) | Contents |
|---------------------|----------|
| `dance-of-the-fool.pdf` | Translation, clean |
| `dance-of-the-fool-annotated.pdf` | Translation + translator's notes |
| `dance-of-the-fool.epub` | Translation, clean |
| `dance-of-the-fool-annotated.epub` | Translation + translator's notes |
| `dance-of-the-fool-web.zip` | Static web reader bundle |

Because the asset names are stable, `releases/latest/download/<name>` always
resolves to the newest build. See [`docs/VERSIONING.md`](../../docs/VERSIONING.md)
for the version scheme and how to cut a release.

### `deploy-pages.yml` — Deploy web reader to GitHub Pages

**Trigger:** push to `main` (or manual dispatch).

Builds the `webui/` Astro app with the Pages base path and deploys it to
GitHub Pages (<https://vredchenko.github.io/dance-of-the-fool/>).

### `build-webui.yml` — Build WebUI bundle (ad-hoc)

**Trigger:** manual dispatch.

Builds only the static webui bundle and uploads it as a 90-day artifact. Handy
for previewing a build without deploying or cutting a release.

## Local testing

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
./regenerate-all.sh   # or: python3 tools/regenerate_all.py
```

## Dependencies (installed automatically in CI)

- Python 3.11 · ReportLab (PDF) · ebooklib (EPUB)
- Node.js 20 (webui build)
- DejaVu fonts (Cyrillic support in PDFs)
