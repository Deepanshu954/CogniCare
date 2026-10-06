/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        elderly: {
          bg: "#0B1320",
          card: "#152238",
          cardHover: "#1C2E4C",
          text: "#FFFFFF",
          textMuted: "#CBD5E1",
          primary: "#38BDF8", // High-contrast sky blue
          success: "#4ADE80", // High-contrast green
          warning: "#FBBF24", // Warm amber
          danger: "#F87171",  // Bold crimson
          accent: "#A78BFA",
        },
        caregiver: {
          primary: "#4F46E5",
          accent: "#06B6D4",
          surface: "#0F172A",
          card: "#1E293B",
          border: "#334155",
        }
      },
      fontSize: {
        'elderly-base': ['1.375rem', { lineHeight: '2rem' }], // 22px
        'elderly-lg': ['1.625rem', { lineHeight: '2.25rem' }], // 26px
        'elderly-xl': ['2rem', { lineHeight: '2.5rem' }],     // 32px
        'elderly-2xl': ['2.5rem', { lineHeight: '3rem' }],    // 40px
      },
    },
  },
  plugins: [],
};
