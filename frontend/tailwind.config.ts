import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: { extend: { colors: { ink: "#202522", clay: "#b35c3e", paper: "#f4f0e9" } } },
  plugins: [],
};

export default config;
