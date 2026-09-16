import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: '/discourse-atlas/',
  plugins: [react()],
  build: {
    sourcemap: true,
  },
});
