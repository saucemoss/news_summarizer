/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}" // Ensures Tailwind scans all components
  ],
  darkMode: "class", // Enables dark mode with a toggle
  theme: {
    extend: {
      colors: {
        background: "#121212", // Deep dark background
        card: "#1e1e1e", // Dark gray for cards
        border: "#333", // Border color
        primary: "#3b82f6", // Blue accent color
        text: "#ffffff", // White text
        mutedText: "#9ca3af" // Lighter gray for descriptions
      },
      boxShadow: {
        card: "0 4px 10px rgba(0, 0, 0, 0.2)", // Custom shadow for cards
        hover: "0 6px 12px rgba(59, 130, 246, 0.3)" // Blue glow on hover
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"], // Use Inter for a modern look
      },
      transitionProperty: {
        width: "width", // Enables width transition
      }
    }
  },
  plugins: [],
};
