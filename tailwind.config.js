/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Playfair Display"', 'serif'],
        script: ['"Dancing Script"', 'cursive'],
        body: ['"Poppins"', 'sans-serif'],
      },
      colors: {
        blush: {
          50: '#fdf2f6',
          100: '#fbe6ee',
          200: '#f6c9db',
        },
        rose: {
          400: '#ec7ba3',
          500: '#e2568a',
          600: '#c73d70',
          700: '#a12c58',
        },
        burgundy: {
          600: '#7a1f3d',
          700: '#5e1730',
          800: '#4a1226',
        },
        gold: {
          400: '#e8c675',
          500: '#d4af37',
        },
      },
      boxShadow: {
        soft: '0 10px 40px -12px rgba(122, 31, 61, 0.25)',
      },
      keyframes: {
        marquee: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
      },
      animation: {
        marquee: 'marquee 32s linear infinite',
      },
    },
  },
  plugins: [],
}
