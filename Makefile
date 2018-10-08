build:
	docker build -t quarterquarter .

run:
	build
	docker run -it -v ./data:/data  quarterquarter --input_shp /data/sample_CO_BLM_PLSS.shp --output_shp /data/quarters.shp --operation q