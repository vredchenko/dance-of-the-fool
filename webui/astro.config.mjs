import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://vredchenko.github.io',
  base: '/spastics-dance',
  output: 'static',
});
