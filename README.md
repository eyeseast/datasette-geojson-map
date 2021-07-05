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

Usage instructions go here.

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
