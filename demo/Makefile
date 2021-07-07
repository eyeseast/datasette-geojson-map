
install:
	pipenv sync

neighborhoods.geojson:
	wget -O $@ https://opendata.arcgis.com/datasets/3525b0ee6e6b427f9aab5d0a1d0a1a28_0.geojson

boston.db: neighborhoods.geojson
	pipenv run geojson-to-sqlite $@ neighborhoods $^

run: boston.db
	pipenv run datasette $^ -m metadata.yml
