
install:
	pipenv sync

neighborhoods.geojson:
	wget -O $@ https://bostonopendata-boston.opendata.arcgis.com/api/download/v1/items/fefd5fb156d9419e80a3944a62bd64ab/geojson?layers=1

schools.geojson:
	wget -O $@ https://bostonopendata-boston.opendata.arcgis.com/datasets/boston::public-schools.geojson

boston.db: neighborhoods.geojson schools.geojson
	pipenv run geojson-to-sqlite $@ neighborhoods neighborhoods.geojson
	pipenv run geojson-to-sqlite $@ schools schools.geojson

run: boston.db
	pipenv run datasette .

clean:
	rm -f boston.db neighborhoods.geojson schools.geojson
