import json
import textwrap

from datasette import hookimpl
from datasette_geojson import can_render_geojson
from datasette_leaflet import CSS_FILE

PLUGIN = "datasette-geojson-map"

DEFAULT_TILE_LAYER = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
DEFAULT_TILE_LAYER_OPTIONS = {
    "maxZoom": 19,
    "detectRetina": True,
    "attribution": '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}


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


@hookimpl
def extra_body_script(
    template, database, table, columns, view_name, request, datasette
):
    if not can_render_geojson(datasette, columns or []):
        return ""

    config = datasette.plugin_config(PLUGIN, database=database, table=table) or {}

    TILE_LAYER = config.get("tile_layer", DEFAULT_TILE_LAYER)
    TILE_LAYER_OPTIONS = config.get("tile_layer_options", DEFAULT_TILE_LAYER_OPTIONS)

    js = f"""
    window.TILE_LAYER = {json.dumps(TILE_LAYER)}
    window.TILE_LAYER_OPTIONS = {json.dumps(TILE_LAYER_OPTIONS)}
    """

    return textwrap.dedent(js)
