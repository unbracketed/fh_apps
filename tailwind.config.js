/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')
module.exports = {
  content: ["./apps/**/app.py", "./apps/**/components/**/*.py"],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Karla', 'sans-serif'],
        'heading': ['Inconsolata', 'sans-serif'],
      },
    },
  },
  plugins: [require('@tailwindcss/forms'),],
}

