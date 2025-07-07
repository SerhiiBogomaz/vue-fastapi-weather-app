import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      'vue-router': 'vue-router/dist/vue-router.esm-bundler.js',
      '@': path.resolve(__dirname, './src'),
    }
  },
server: {
  host: '0.0.0.0',
  port: 8080,
  strictPort: true,
  proxy: {
    '/api': {
      target: 'http://backend:8000',
      changeOrigin: true,
      secure: false,
    }
  }
},
})
