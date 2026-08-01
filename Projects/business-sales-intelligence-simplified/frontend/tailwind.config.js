/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#0B0E14",        // page background
        panel: "#11161F",      // card background
        panel2: "#161C28",     // slightly raised panel
        line: "#242C3B",       // hairline borders
        signal: "#FFB000",     // amber accent -- the one bold color
        signal2: "#FFD066",    // lighter amber for hover/highlight
        up: "#39D98A",         // positive movement
        down: "#FF5C5C",       // negative movement
        muted: "#7A8699",      // secondary text
        paper: "#E8ECF1",      // primary text on dark
      },
      fontFamily: {
        mono: ["'IBM Plex Mono'", "ui-monospace", "SFMono-Regular", "monospace"],
        sans: ["'Space Grotesk'", "ui-sans-serif", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
