# datasette-geojson-map

[![PyPI](https://img.shields.io/pypi/v/datasette-geojson-map.svg)](https://pypi.org/project/datasette-geojson-map/)
[![Changelog](https://img.shields.io/github/v/release/eyeseast/datasette-geojson-map?include_prereleases&label=changelog)](https://github.com/eyeseast/datasette-geojson-map/releases)
[![Tests](https://github.com/eyeseast/datasette-geojson-map/workflows/Test/badge.svg)](https://github.com/eyeseast/datasette-geojson-map/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/eyeseast/datasette-geojson-map/blob/main/LICENSE)

Render a map for any query with a geometry column

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-geojson-map

## Usage

Start by loading a GIS file.

For example, you might use [geojson-to-sqlite](https://pypi.org/project/geojson-to-sqlite/) or [shapefile-to-sqlite](https://pypi.org/project/shapefile-to-sqlite/) to load [neighborhood boundaries](https://bostonopendata-boston.opendata.arcgis.com/datasets/3525b0ee6e6b427f9aab5d0a1d0a1a28_0/explore) into a SQLite database.

```sh
wget -O neighborhoods.geojson https://opendata.arcgis.com/datasets/3525b0ee6e6b427f9aab5d0a1d0a1a28_0.geojson
geojson-to-sqlite boston.db neighborhoods neighborhoods.geojson
```

(The command above uses Spatialite, but that's not required.)

Start up `datasette` and navigate to the `neighborhoods` table.

```sh
datasette serve boston.db

# in another terminal tab
open http://localhost:8001/boston/neighborhoods
```

You should see a map centered on Boston with each neighborhood outlined. Clicking a boundary will bring up a popup with details on that feature.

![Boston neighbhorhoods map](img/boston-neighborhoods-map.png)

This plugin relies on (and will install) [datasette-geojson](https://github.com/eyeseast/datasette-geojson). Any query that includes a `geometry` column will produce a map of the results. This also includes single row views.

Run the included `demo` project to see it live.

## Configuration

This project uses the same map configuration as [datasette-cluster-map](https://github.com/simonw/datasette-cluster-map). Here's how you would use [Stamen's terrain tiles](http://maps.stamen.com/terrain/#12/37.7706/-122.3782):

```yaml
plugins:
  datasette-geojson-map:
    tile_layer: https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.{ext}
    tile_layer_options:
      attribution: >-
        Map tiles by <a href="http://stamen.com">Stamen Design</a>, 
        under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. 
        Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, 
        under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.
      subdomains: abcd
      minZoom: 1
      maxZoom: 16
      ext: jpg
```

Options:

- `tile_layer`: Use a URL template that can be passed to a [Leaflet Tilelayer](https://leafletjs.com/reference-1.7.1.html#tilelayer)
- `tile_layer_options`: All options will be passed to the tile layer. See [Leaflet documentation](https://leafletjs.com/reference-1.7.1.html#tilelayer) for more on possible values here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-geojson-map
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
