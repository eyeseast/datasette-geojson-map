import json
import sqlite3
import textwrap

from datasette import hookimpl
from datasette.filters import FilterArguments
from datasette_geojson import can_render_geojson

PLUGIN = "datasette-geojson-map"

DEFAULT_TILE_LAYER = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
DEFAULT_TILE_LAYER_OPTIONS = {
    "maxZoom": 19,
    "detectRetina": True,
    "attribution": '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    "use_maki_icons": True,
    "use_simplestyle": True,
}


@hookimpl
def extra_css_urls(template, database, table, columns, view_name, request, datasette):
    if not can_render_geojson(datasette, columns or []):
        return []

    return [
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
    # TILE_LAYER_OPTIONS = config.get("tile_layer_options", DEFAULT_TILE_LAYER_OPTIONS)
    TILE_LAYER_OPTIONS = DEFAULT_TILE_LAYER_OPTIONS.copy()
    TILE_LAYER_OPTIONS.update(config.get("tile_layer_options", {}))

    js = f"""
    window.TILE_LAYER = {json.dumps(TILE_LAYER)}
    window.TILE_LAYER_OPTIONS = {json.dumps(TILE_LAYER_OPTIONS)}
    """

    return textwrap.dedent(js)


@hookimpl
def filters_from_request(request, database, table, datasette):
    "Filter by bounding box, if _bbox is in request"

    async def inner():
        db = datasette.get_database(database)
        bbox = request.args.get("_bbox", "").split(",")

        if not bbox or len(bbox) != 4:
            return None

        x1, y1, x2, y2 = tuple(map(float, bbox))
        params = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}

        geometry_column, spatial_index_enabled = await get_geometry_column(db, table)
        if not geometry_column:
            return None

        # write this once and insert it
        mbr = "BuildMbr(cast(:x1 as numeric), cast(:y1 as numeric), cast(:x2 as numeric), cast(:y2 as numeric))"
        where_clauses = [f"Intersects({mbr}, [{geometry_column}])"]

        if spatial_index_enabled:
            spatial_lookup = textwrap.dedent(
                f"""
            [{table}].rowid in
            (select rowid from SpatialIndex where f_table_name = :table
            and search_frame = {mbr})"""
            ).strip()

            where_clauses.append(spatial_lookup)
            params["table"] = table

        return FilterArguments(
            where_clauses,
            params=params,
            human_descriptions=[f"{table}.{geometry_column} intersects map area"],
        )

    return inner


async def get_geometry_column(db, table):
    "Get a two-tuple of (column, indexed) for the first geometry column in this table"
    sql = textwrap.dedent(
        """select f_geometry_column, spatial_index_enabled 
    from geometry_columns 
    where f_table_name = ?"""
    )
    try:
        results = await db.execute(sql, [table])
        row = results.first()
        if row:
            return row["f_geometry_column"], bool(row["spatial_index_enabled"])
        return "", False

    except sqlite3.OperationalError:
        return "", False
