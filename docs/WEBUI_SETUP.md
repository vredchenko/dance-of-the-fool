# Web UI Setup Instructions

Quick start guide for running the translation proofreading web UI locally.

## Prerequisites

1. **Node.js 18+** - Download from [nodejs.org](https://nodejs.org/)
2. **Python 3.11+** - Should already be installed for this project

## Installation

```bash
# Navigate to web UI directory
cd webui

# Install Node.js dependencies
npm install
```

## Running Locally

```bash
# Start development server (from webui/ directory)
npm run dev

# This will:
# 1. Run the Python data aggregation script
# 2. Start Astro dev server on http://localhost:4321
# 3. Open your browser automatically
```

Visit **http://localhost:4321** to see the translation interface.

## Making Changes

### Updating Translation Data

If you modify any translation files (`chunk_*.json`, `translation_chunk_*.md`, etc.):

```bash
# Rebuild the data
npm run prebuild

# Or restart the dev server (it runs prebuild automatically)
npm run dev
```

### Editing UI Code

The dev server has hot-reload enabled. Edit any file in `webui/src/` and see changes instantly:

- `src/pages/index.astro` - Homepage
- `src/pages/chunk/[id].astro` - Chunk pages
- `src/components/` - Reusable components
- `src/styles/global.css` - Global styles

### Dark Mode

- Click the sun/moon icon in the header
- Or press **D** key
- Preference is saved in browser localStorage

### Keyboard Shortcuts

- **D** - Toggle dark mode
- **← →** - Navigate between chunks (when viewing a chunk)
- **?** - Show help (logs to console)

## Building for Production

```bash
# Create optimized static build
npm run build

# The output will be in webui/dist/
# You can deploy this folder to any static hosting service
```

## Testing Production Build Locally

```bash
# Build first
npm run build

# Preview the production build
npm run preview

# Opens at http://localhost:4321
```

## Troubleshooting

### "Module not found" errors

```bash
# Make sure you're in the webui/ directory
cd webui

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### "translation-data.json not found"

```bash
# Run the data build script manually
python3 ../scripts/build-webui-data.py

# Or run prebuild
npm run prebuild
```

### Port 4321 already in use

```bash
# Kill the process using the port
lsof -ti:4321 | xargs kill

# Or use a different port
npm run dev -- --port 3000
```

### Styling looks broken

Make sure Tailwind CSS is working:

```bash
# Check that @astrojs/tailwind is installed
npm list @astrojs/tailwind

# If missing, reinstall
npm install @astrojs/tailwind
```

## Project Structure

```
webui/
├── src/
│   ├── pages/              # Routes
│   │   ├── index.astro     # Homepage (/)
│   │   └── chunk/
│   │       └── [id].astro  # Chunk pages (/chunk/01, /chunk/02, etc.)
│   ├── components/         # Reusable UI components
│   ├── layouts/            # Page layouts
│   ├── styles/             # Global CSS
│   └── data/               # Generated data (gitignored)
├── public/                 # Static assets
├── package.json            # Node.js dependencies
└── astro.config.mjs        # Astro configuration
```

## Performance

- First page load: ~500ms
- Navigation between chunks: instant (static pages)
- Dark mode toggle: instant (CSS only)
- Bundle size: ~100KB (gzipped)

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## Next Steps

After confirming everything works locally:

1. Review the UI and test different chunks
2. Check that all 39 chunks render correctly
3. Verify uncertainties are displayed properly
4. Test dark mode
5. Test on mobile device (responsive design)

If everything looks good, you can deploy to GitHub Pages, Netlify, or Vercel (see `WEBUI_DEVPLAN.md` for deployment instructions).

## Questions?

See the full development plan in `WEBUI_DEVPLAN.md` or the web UI README at `webui/README.md`.
