import json
import numpy as np
from fastapi import FastAPI, HTTPException
from typing import TypedDict

from geotif_to_geojson import convert_raster_to_gdf
from vector_to_raster import get_bounds_coords_list, get_south_west_corner_coords_gdf, make_gdf_from_geojson, raster_to_base64_png, rasterize_gdf

app = FastAPI()


class PngResponse(TypedDict):
        bbox_sw_corner: list
        img_width: int
        img_height: int
        bbox_coordinates: list
        image_base64_string: str

class GeoJSONFeature(TypedDict):
    type: str
    geometry: dict
    properties: dict

class GeoJSON(TypedDict):
    features: list[GeoJSONFeature]
    crs: dict



class RequestObject(TypedDict):
    geojson: GeoJSON
    resolution: int
    property_to_burn: str


@app.post("/geojson_to_png")
# TODO async def geojson_to_png(
def geojson_to_png(
    request_obj: RequestObject
) -> PngResponse:

    geojson =  request_obj["geojson"]  # TODO GeoJSON
    resolution= request_obj["resolution"]
    property_to_burn = request_obj["property_to_burn"]

    gdf = make_gdf_from_geojson(geojson)
    gdf = gdf.to_crs("EPSG:25832")

    # rasterize data to np.ndarray
    raster = rasterize_gdf(gdf, property_to_burn, resolution)
    img_width, img_height = raster.shape

    response_object = {
        "bbox_sw_corner": get_south_west_corner_coords_gdf(gdf.total_bounds),
        "img_width": img_width,
        "img_height": img_height,
        "bbox_coordinates": get_bounds_coords_list(gdf.total_bounds),
        "image_base64_string": raster_to_base64_png(raster)
    }

    return response_object



""" 
TODO GEOJSON TO GEOTIFF


# returns a binary GeoTIFF 
https://fastapi.tiangolo.com/advanced/custom-response/ --> FileResponse

# TODO HOw to set headers
# TODO actually convert to GeoTIFF 
def geojson_to_geotiff(
    geojson: dict,
    resolution: int,
    property_to_burn: str,
)-> PngResponse: 
    
    # TOODO check_input() , crs, is valid geojson, ...
    gdf = make_gdf_from_geojson(geojson)

    # rasterize data to np.ndarray
    raster = rasterize_gdf(gdf, property_to_burn, resolution)
    geotiff = raster_to_geotiff(raster)

    return geotiff """


"""
# TODO RASTER TO GEOJSON
# todo RECEIVE A TIF FILE: https://fastapi.tiangolo.com/tutorial/request-forms-and-files/

def raster_to_geojson(
    raster_data: np.ndarray,
    crs: str
):
    # convert to geopandas geodataframe
    gdf = convert_raster_to_gdf(raster_data) 

    # Use Geopandas to reproject all features to EPSG:4326
    gdf = gdf.to_crs(crs)

    # save as geojson

    return json.loads(gdf.to_json())


"""
