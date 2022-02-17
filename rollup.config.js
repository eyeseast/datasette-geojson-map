import resolve from "@rollup/plugin-node-resolve";

// `npm run build` -> `production` is true
// `npm run dev` -> `production` is false
const production = !process.env.ROLLUP_WATCH;

export default {
	input: "src/map.js",
	output: {
		dir: "datasette_geojson_map/static/",
		chunkFileNames: "[name].js",
		format: "esm",
		sourcemap: true,
	},
	plugins: [resolve()],
};
