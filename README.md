# geotiff_to_geojson

Converts a local tif file into a geojson

- place your "input.tif" into the data folder
- run the script
- Results are saved as "output.geojson" in data folder

## Run directly on your machine
### Install plainly on your machine
- Create venv with python3  (Python 3.10 currently not working yet)
- Activate the venv
- Install requirements with 'python -m pip install -r requirements.txt'
- create new folder "data"

### Run on your machine
- Activate the venv
- Run 'python geotiff_to_geojson.py'


## Run with Docker
### Install as docker
- Run 'docker build -t geotiff_to_geojson_img .'

### Run as docker
- Run 'docker run -d --name geotiff_to_geojson -v ${PWD}/data:/app/data geotiff_to_geojson_img'