
install:
	pipenv sync

neighborhoods.geojson:
	wget -O $@ https://opendata.arcgis.com/datasets/3525b0ee6e6b427f9aab5d0a1d0a1a28_0.geojson

schools.geojson:
	wget -O $@ https://bostonopendata-boston.opendata.arcgis.com/datasets/boston::public-schools.geojson

boston.db: data/neighborhoods.geojson data/schools.geojson
	pipenv run geojson-to-sqlite $@ neighborhoods data/neighborhoods.geojson
	pipenv run geojson-to-sqlite $@ schools data/schools.geojson

places.db: data/innout.geojson data/starbucks.geojson
	pipenv run geojson-to-sqlite $@ places data/innout.geojson --spatial-index --properties
	pipenv run geojson-to-sqlite $@ places data/starbucks.geojson --spatial-index --properties
	pipenv run geojson-to-sqlite $@ neighborhoods data/neighborhoods.geojson --spatial-index
	pipenv run geojson-to-sqlite $@ schools data/schools.geojson --spatial-index

run:
	pipenv run datasette serve . --load-extension spatialite

databases: boston.db places.db

clean:
	rm -f *.db
