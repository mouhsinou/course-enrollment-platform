import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/auth': 'https://course-enrollment-platform.onrender.com',
      '/users': 'https://course-enrollment-platform.onrender.com',
      '/courses': 'https://course-enrollment-platform.onrender.com',
      '/enrollments': 'https://course-enrollment-platform.onrender.com',
    },
  },
})
