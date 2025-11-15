/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Light mode
        'light-bg': '#FAFAFA',
        'light-uk': '#FFFFFF',
        'light-en': '#F8F9FA',
        'light-uncertainty': '#FFF3CD',
        // Dark mode
        'dark-bg': '#1A1A1A',
        'dark-uk': '#2A2A2A',
        'dark-en': '#232323',
        'dark-uncertainty': '#3D3929',
      },
      fontFamily: {
        'serif': ['Lora', 'Georgia', 'Times New Roman', 'serif'],
        'ukrainian': ['Literata', 'Georgia', 'Times New Roman', 'serif'],
        'sans': ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        'mono': ['JetBrains Mono', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
};
