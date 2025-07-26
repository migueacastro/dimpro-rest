import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit(), purgeCss()],
  ssr: {
			noExternal: process.env.NODE_ENV === 'production' ? ['@carbon/charts'] : []
	},
  server: {
    allowedHosts:['castroworks.lat'],
    host: "0.0.0.0",
    port: 3000,
  },
  preview: {
    allowedHosts:['castroworks.lat'],
    host: "0.0.0.0",
    port: 3000,
  },
});
