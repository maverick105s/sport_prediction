import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: '/sport_prediction/',
  plugins: [react()],
  server: {
    allowedHosts: true,
    proxy: {
      '/matches': 'http://localhost:8000',
      '/predictions': 'http://localhost:8000',
      '/games': 'http://localhost:8000',
      '/users': 'http://localhost:8000',
    }
  }
})