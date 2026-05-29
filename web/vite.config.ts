import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath, URL } from 'node:url'

const backendBaseUrl = process.env.VITE_BACKEND_BASE_URL || 'http://localhost:9100'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 9101,
    proxy: {
      '/v1': {
        target: backendBaseUrl,
        changeOrigin: true,
      },
      '/auth': {
        target: backendBaseUrl,
        changeOrigin: true,
      },
      '/health': {
        target: backendBaseUrl,
        changeOrigin: true,
      },
    },
  },
})
