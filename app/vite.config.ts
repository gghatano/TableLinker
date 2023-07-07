import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  plugins: [vue()],
  define: {
    'process.env': {},
  },
  server: {
    hmr: {
      clientPort: 8080,
    },
    port: 8080,
    proxy: {
      '/graphql': {
        //target: 'http://localhost:18000',
        target: 'http://api:8000',
        changeOrigin: false,
      },
      '/download': {
        //target: 'http://localhost:18000',
        target: 'http://api:8000',
        changeOrigin: false,
      },
    },
  },
})
