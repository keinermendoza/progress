/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.html", "./**/templates/**/snipets/*.html"],
  theme: {
    extend: {
      screens: {
      'nano': '380px'
    },
  },
  plugins: [],
}
}
