/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          primary: '#1E1E1E',
          secondary: '#2D2D2D',
          accent: '#404040',
          text: '#E0E0E0',
          'text-secondary': '#A0A0A0',
          'spotify-green': '#1DB954',
          'spotify-hover': '#1ed760'
        }
      }
    },
  },
  plugins: [],
} 