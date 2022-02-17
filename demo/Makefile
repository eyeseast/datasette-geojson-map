
install:
	pipenv sync

neighborhoods.geojson:
	wget -O $@ https://opendata.arcgis.com/datasets/3525b0ee6e6b427f9aab5d0a1d0a1a28_0.geojson

schools.geojson:
	wget -O $@ https://bostonopendata-boston.opendata.arcgis.com/datasets/boston::public-schools.geojson

boston.db: neighborhoods.geojson schools.geojson
	pipenv run geojson-to-sqlite $@ neighborhoods neighborhoods.geojson
	pipenv run geojson-to-sqlite $@ schools schools.geojson

run: boston.db
	pipenv run datasette $^ -m metadata.yml

clean:
	rm -f boston.db neighborhoods.geojson schools.geojson
