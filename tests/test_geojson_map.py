import json
import pytest
from pathlib import Path
from datasette.app import Datasette
from geojson_to_sqlite.utils import import_features
from datasette_geojson_map import PLUGIN

DATA = Path(__file__).parent / "data"
NEIGHBORHOODS = DATA / "Boston_Neighborhoods.geojson"
TABLE_NAME = "neighborhoods"


@pytest.fixture
def feature_collection():
    return json.loads(NEIGHBORHOODS.read_text())


@pytest.fixture
def database(tmp_path, feature_collection):
    db_path = tmp_path / "test.db"
    import_features(db_path, TABLE_NAME, feature_collection["features"])
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
    url = ds.urls.table(database.stem, TABLE_NAME)
    response = await ds.client.get(url)

    assert response.status_code == 200

    css = ds.urls.static_plugins(PLUGIN, "map.css")

    assert css in response.text


@pytest.mark.asyncio
async def test_has_js(database):
    ds = Datasette([str(database)])
    url = ds.urls.table(database.stem, TABLE_NAME)
    response = await ds.client.get(url)

    assert response.status_code == 200

    js = ds.urls.static_plugins(PLUGIN, "map.js")

    assert js in response.text
