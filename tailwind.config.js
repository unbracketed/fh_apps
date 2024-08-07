/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./apps/**/app.py}", "./apps/**/components/**/*.py"],
  theme: {
    extend: {},
  },
  plugins: [require('@tailwindcss/forms'),],
}

