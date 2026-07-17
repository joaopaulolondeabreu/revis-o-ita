import { defineConfig } from "astro/config";

// A "base" é ajustada pelo GitHub Pages na publicação (nome do repositório).
// Em desenvolvimento local, fica na raiz.
export default defineConfig({
  output: "static",
  site: process.env.SITE_URL || "http://localhost:4321",
  base: process.env.BASE_PATH || "/",
});
