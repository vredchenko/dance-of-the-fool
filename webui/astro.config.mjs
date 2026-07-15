import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://vredchenko.github.io',
  // Empty base for local dev; CI sets BASE_PATH=/dance-of-the-fool/ for GitHub Pages.
  base: process.env.BASE_PATH || '/',
  output: 'static',
});
