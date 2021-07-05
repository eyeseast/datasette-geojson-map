from datasette import hookimpl
from datasette_geojson import can_render_geojson
from datasette_leaflet import CSS_FILE

PLUGIN = "datasette-geojson-map"


@hookimpl
def extra_css_urls(template, database, table, columns, view_name, request, datasette):
    if not can_render_geojson(datasette, columns or []):
        return []

    return [
        datasette.urls.static_plugins("datasette-leaflet", CSS_FILE),
        datasette.urls.static_plugins(PLUGIN, "map.css"),
    ]


@hookimpl
def extra_js_urls(template, database, table, columns, view_name, request, datasette):
    if not can_render_geojson(datasette, columns or []):
        return []

    return [{"url": datasette.urls.static_plugins(PLUGIN, "map.js"), "module": True}]
