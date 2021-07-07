from setuptools import setup
import os

VERSION = "0.3.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-geojson-map",
    description="Render a map for any query with a geometry column",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Chris Amico",
    url="https://github.com/eyeseast/datasette-geojson-map",
    project_urls={
        "Issues": "https://github.com/eyeseast/datasette-geojson-map/issues",
        "CI": "https://github.com/eyeseast/datasette-geojson-map/actions",
        "Changelog": "https://github.com/eyeseast/datasette-geojson-map/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_geojson_map"],
    entry_points={"datasette": ["geojson_map = datasette_geojson_map"]},
    install_requires=["datasette", "datasette-geojson", "datasette-leaflet"],
    extras_require={"test": ["pytest", "pytest-asyncio", "geojson-to-sqlite"]},
    tests_require=["datasette-geojson-map[test]"],
    package_data={"datasette_geojson_map": ["static/*", "templates/*"]},
    python_requires=">=3.6",
)
