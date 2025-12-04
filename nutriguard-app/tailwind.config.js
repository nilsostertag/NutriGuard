import { defineConfig } from "tailwindcss";
import { skeleton } from "@skeletonlabs/tw-plugin";

export default defineConfig({
  content: [
    "./src/**/*.{html,js,svelte,ts,jsx,tsx}",
  ],
  plugins: [
    skeleton({
      themes: {
        preset: "pine"
      }
    })
  ]
});
