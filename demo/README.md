# Boston Neighborhoods

This is a demo of [datasette-geojson-map](https://github.com/eyeseast/datasette-geojson-map). It uses [pipenv](https://pipenv.pypa.io/en/latest/) to install dependencies.

To get started, use the following `make` commands:

```sh
make install
make boston.db
make run
```

That will install all Python dependences, build a database of Boston neighborhoods and run a local Datasette instance.
