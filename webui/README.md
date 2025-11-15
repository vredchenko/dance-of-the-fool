# Translation Proofreading Web UI

Static website for proofreading the Ukrainian-to-English translation of "Танець недоумка" (The Dance of the Fool) by Ілларіон Павлюк.

## Features

- **Side-by-side view**: Ukrainian source and English translation in parallel columns
- **Translation notes**: Highlighted uncertainties and translation questions
- **Dark mode**: Toggle with 'D' key or the moon/sun icon
- **Keyboard navigation**: Use arrow keys to move between chunks
- **Responsive design**: Works on desktop, tablet, and mobile
- **Static generation**: Fast loading, works offline, easy to deploy

## Development

### Prerequisites

- Node.js 18+ (for Astro)
- Python 3.11+ (for data aggregation script)

### Setup

```bash
# Install dependencies
cd webui
npm install

# Build data from translation files (runs automatically with dev/build)
npm run prebuild

# Start development server
npm run dev
# → Opens http://localhost:4321

# Build for production
npm run build
# → Outputs to dist/

# Preview production build
npm run preview
```

### Data Pipeline

The build process:

1. **Python script** (`scripts/build-webui-data.py`) reads:
   - `chunk_*.json` (39 files) - Ukrainian source text
   - `translation_chunk_*.md` (39 files) - English translations
   - `translation_chunk_*_uncertainty.md` (39 files) - Translation notes

2. **Aggregates** into `src/data/translation-data.json`

3. **Astro** generates static HTML from the data

### Project Structure

```
webui/
├── public/              # Static assets
│   └── favicon.svg
├── src/
│   ├── components/      # Reusable components
│   │   ├── Header.astro
│   │   └── UncertaintyPanel.astro
│   ├── layouts/
│   │   └── BaseLayout.astro
│   ├── pages/
│   │   ├── index.astro       # Homepage
│   │   └── chunk/
│   │       └── [id].astro    # Dynamic chunk pages
│   ├── data/
│   │   └── translation-data.json  # Generated
│   └── styles/
│       └── global.css
├── package.json
├── astro.config.mjs
└── tailwind.config.mjs
```

## Keyboard Shortcuts

- **D** - Toggle dark mode
- **← →** - Navigate between chunks (on chunk pages)
- **?** - Show shortcuts help (in console)

## Deployment

### GitHub Pages

1. Update `astro.config.mjs` with your repo name
2. Push to GitHub
3. Enable GitHub Pages in repo settings
4. Set up GitHub Actions workflow (see WEBUI_DEVPLAN.md)

### Netlify/Vercel

1. Connect your Git repo
2. Build command: `npm run build`
3. Publish directory: `dist`
4. Done! Auto-deploys on push

## License

Same as parent project.
