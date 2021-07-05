/*
Render a map based on a query or table view by fetching its GeoJSON representation
*/

async function render() {
	console.debug("Rendering GeoJSON map");
	// window.datasette.leaflet.JAVASCRIPT_URL
	const L = await import(window.datasette.leaflet.JAVASCRIPT_URL);
	const geojson = await fetch(location.pathname + ".geojson").then(r => r.json());

	const parent = document.querySelector(".table-wrapper");
	const container = document.createElement("DIV");

	Object.assign(container, {
		id: "map",
	});

	parent.insertBefore(container, parent.firstElementChild);

	const map = createMap(L, container);
	const layer = L.geoJSON(geojson).addTo(map);
	const bounds = layer.getBounds();

	map.fitBounds(bounds);
}

function createMap(L, container) {
	const map = L.map(container);

	L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
		attribution:
			'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	}).addTo(map);

	return map;
}

window.addEventListener("load", render);
