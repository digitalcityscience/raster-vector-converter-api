FROM python:3.9

LABEL org.opencontainers.image.authors="andre.landwehr@hcu-hamburg.de"

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "geotif_to_geojson.py"]