/*
Render a map based on a query or table view by fetching its GeoJSON representation
*/

async function render() {
	console.debug("Rendering GeoJSON map");
	// window.datasette.leaflet.JAVASCRIPT_URL
	const L = await import(window.datasette.leaflet.JAVASCRIPT_URL);

	// simplestyle
	await import('./leaflet-simplestyle.min.js');

	const geojson = await fetch(geojsonURL(window.location)).then(r => r.json());

	const parent = document.querySelector(".table-wrapper");
	const container = document.createElement("DIV");

	Object.assign(container, {
		id: "map",
	});

	parent.insertBefore(container, parent.firstElementChild);

	const map = createMap(L, container);
	const layer = L.geoJSON(geojson, { useSimpleStyle: true, useMakiMarkers: false })
		.addTo(map)
		.bindPopup(popup);
	const bounds = layer.getBounds();

	map.fitBounds(bounds);

	// make debugging easier
	window.map = map;
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

window.addEventListener("load", render);
//# sourceMappingURL=map.js.map
