const { nextui } = require("@nextui-org/react");

/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Noto Sans KR", "sans-serif"],
        kopub: ["KoPubDotum", "sans-serif"],
        chosun: ["ChosunNm", "serif"],
        gothic: ["Noto Serif KR", "serif"],
      },
    },
  },
  darkMode: "class",
  plugins: [nextui()],
};
