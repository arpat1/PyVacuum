import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: Number(process.env.VIEW_PORT),
    proxy: {
      '/eel': {
          target: `ws://localhost:${process.env.CORE_PORT}`,
          ws: true,
          rewriteWsOrigin: true
      },
    }
  }
})
