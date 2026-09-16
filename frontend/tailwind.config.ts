import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0A0E1A",
        foreground: "#E6F1FF",
        cyan: {
          accent: "#00D9FF",
        },
        violet: {
          accent: "#7B61FF",
        },
      },
      boxShadow: {
        glow: "0 0 20px -5px rgba(0, 217, 255, 0.4)",
        glowViolet: "0 0 20px -5px rgba(123, 97, 255, 0.4)",
      },
    },
  },
  plugins: [],
};
export default config;
