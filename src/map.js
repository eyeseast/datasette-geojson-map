/*
Render a map based on a query or table view by fetching its GeoJSON representation
*/

async function render() {
	console.debug("Rendering GeoJSON map");

	// load dependencies
	await Promise.all([
		loadCSS(window.datasette.leaflet.CSS_URL),
		import(window.datasette.leaflet.JAVASCRIPT_URL),
	]);

	await import("leaflet-simplestyle");

	const geojson = await fetch(geojsonURL(window.location)).then(r => r.json());

	const parent = document.querySelector(".table-wrapper");
	const container = document.createElement("DIV");

	Object.assign(container, {
		id: "map",
	});

	parent.insertBefore(container, parent.firstElementChild);

	const map = createMap(window.L, container);
	const layer = L.geoJSON(geojson, {
		useSimpleStyle: window.TILE_LAYER_OPTIONS.use_simplestyle,
		useMakiMarkers: window.TILE_LAYER_OPTIONS.use_maki_icons,
	})
		.addTo(map)
		.bindPopup(popup);

	const bounds = getBounds(layer, window.L);

	map.fitBounds(bounds);
	map.on("moveend", updateBounds);

	// make debugging easier
	window.map = map;
}

function loadCSS(href) {
	const link = document.createElement("link");

	Object.assign(link, { href, rel: "stylesheet" });

	document.head.appendChild(link);

	return new Promise((resolve, reject) => {
		link.addEventListener("load", resolve);
		link.addEventListener("error", reject);
	});
}

function createMap(L, container) {
	const map = L.map(container);

	L.tileLayer(window.TILE_LAYER, window.TILE_LAYER_OPTIONS).addTo(map);

	return map;
}

function geojsonURL(location) {
	const url = new URL(location);
	url.pathname = url.pathname + ".geojson";
	return url;
}

function popup(layer) {
	const { properties } = layer.feature;
	const items = Object.entries(properties).map(
		([key, value]) => `
  <dt>${key}</dt>
  <dd class="${typeof value}">${format(value)}</dd>`
	);

	return `<dl class="properties">${items.join("")}</dl>`;
}

function format(value) {
	switch (typeof value) {
		case "number":
			return value.toLocaleString();

		case "string":
			return value;

		default:
			return String(value);
	}
}

function renderBBoxInput() {}

function renderSplitBoundsInput() {}
/**
 * Get bounds for the GeoJSON layer,
 * unless we have a _bbox or other params set
 *
 * @param {*} layer
 */
function getBounds(layer, L) {
	const qs = new URL(window.location).searchParams;

	if (qs.has("_bbox")) {
		const [x1, y1, x2, y2] = qs.get("_bbox").split(",").map(Number);
		return L.latLngBounds([y1, x1], [y2, x2]);
	}

	if (["x1", "y1", "x2", "y2"].every(f => qs.has(f))) {
		const [x1, y1, x2, y2] = ["x1", "y1", "x2", "y2"].map(f => qs.get(f)).map(Number);
		return L.latLngBounds([y1, x1], [y2, x2]);
	}

	return layer.getBounds();
}

function updateBounds(e) {}

window.addEventListener("load", render);
