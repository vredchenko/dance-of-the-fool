import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://vredchenko.github.io',
  // Comment out base path for local development
  // base: '/dance-of-the-fool',
  output: 'static',
});
