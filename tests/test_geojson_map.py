import json
import pytest
import textwrap
from pathlib import Path
from urllib.parse import urlencode

from datasette import Request
from datasette.app import Datasette
from datasette.filters import FilterArguments
from datasette.utils import await_me_maybe
from geojson_to_sqlite.utils import import_features
from datasette_geojson_map import PLUGIN, filters_from_request, get_geometry_column

DATA = Path(__file__).parent / "data"
NEIGHBORHOODS = DATA / "neighborhoods.geojson"
SCHOOLS = DATA / "schools.geojson"
TABLE_NEIGHBORHOODS = "neighborhoods"
TABLE_SCHOOLS = "schools"


@pytest.fixture
def neighborhoods():
    return json.loads(NEIGHBORHOODS.read_text())


@pytest.fixture
def schools():
    return json.loads(SCHOOLS.read_text())


@pytest.fixture
def database(tmp_path, neighborhoods):
    db_path = tmp_path / "test.db"
    import_features(db_path, TABLE_NEIGHBORHOODS, neighborhoods["features"])
    return db_path


@pytest.fixture
def spatial_database(tmp_path, neighborhoods, schools):
    db_path = tmp_path / "test_spatial.db"
    import_features(
        db_path, TABLE_NEIGHBORHOODS, neighborhoods["features"], spatial_index=True
    )
    import_features(db_path, TABLE_SCHOOLS, schools["features"], spatial_index=True)
    return db_path


@pytest.mark.asyncio
async def test_plugin_is_installed():
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/plugins.json")
    assert response.status_code == 200
    installed_plugins = {p["name"] for p in response.json()}
    assert "datasette-geojson-map" in installed_plugins


@pytest.mark.asyncio
async def test_has_css(database):
    ds = Datasette([str(database)])
    url = ds.urls.table(database.stem, TABLE_NEIGHBORHOODS)
    response = await ds.client.get(url)

    assert response.status_code == 200

    css = ds.urls.static_plugins(PLUGIN, "map.css")

    assert css in response.text


@pytest.mark.asyncio
async def test_has_js(database):
    ds = Datasette([str(database)])
    url = ds.urls.table(database.stem, TABLE_NEIGHBORHOODS)
    response = await ds.client.get(url)

    assert response.status_code == 200

    js = ds.urls.static_plugins(PLUGIN, "map.js")

    assert js in response.text


@pytest.mark.asyncio
async def test_get_geometry_column(spatial_database):
    ds = Datasette([spatial_database])
    db = ds.get_database(spatial_database.stem)
    geometry_column, spatial_index = await get_geometry_column(db, TABLE_SCHOOLS)
    assert "geometry", True == (geometry_column, spatial_index)


@pytest.mark.asyncio
async def test_filter_bbox(spatial_database):
    ds = Datasette([spatial_database])
    bbox = [-71.16, 42.32, -70.99, 42.37]  # Boston-ish
    path = ds.urls.table(spatial_database.stem, TABLE_SCHOOLS)
    qs = urlencode({"_bbox": ",".join(map(str, bbox))})
    url = f"{path}?{qs}"
    request = Request.fake(
        url,
        url_vars={
            "database": spatial_database.stem,
            "table": TABLE_SCHOOLS,
        },
    )
    filters = await await_me_maybe(
        filters_from_request(
            request=request,
            database=spatial_database.stem,
            table=TABLE_SCHOOLS,
            datasette=ds,
        )
    )

    assert isinstance(filters, FilterArguments)
    assert 2 == len(filters.where_clauses)

    assert (
        f"Intersects(BuildMbr(:x1, :y1, :x2, :y2), [geometry])" in filters.where_clauses
    )

    assert (
        textwrap.dedent(
            f"""
            [{TABLE_SCHOOLS}].rowid in
            (select rowid from SpatialIndex where f_table_name = :table
            and search_frame = BuildMbr(:x1, :y1, :x2, :y2))"""
        ).strip()
        in filters.where_clauses
    )

    assert filters.params["table"] == TABLE_SCHOOLS
