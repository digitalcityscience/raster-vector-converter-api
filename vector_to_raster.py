import base64
import os

# vector data
import geopandas
from shapely.geometry import Polygon, Point

# rasterization
import numpy as np
from numpy.typing import NDArray

from geocube.rasterize import rasterize_image
from odc.geo.geobox import GeoBox
from rasterio.enums import MergeAlg

# to raster
from io import BytesIO
from PIL import Image

from typing import Literal

pic_format_options = Literal["png", "tiff"]


# returns an np_array raster with png img like data [0-255]
def rasterize_gdf(
    gdf:geopandas.GeoDataFrame,
    property_to_burn:str,
    resolution: int
    ) -> NDArray:

    raster_data = rasterize_image(
        geometry_array = gdf.geometry,  # A geometry array of points.
        data_values = gdf[property_to_burn].to_numpy(),
        geobox=GeoBox.from_bbox(gdf.total_bounds, gdf.crs, resolution=resolution),
        fill=0,
        merge_alg=MergeAlg.add
    )

    # create a np array with dtype uint8 from rasterized data
    img = raster_data.astype(np.uint8)
    print("unique values in image data ", np.unique(img))

    return img


def make_gdf_from_geojson(geojson) -> geopandas.GeoDataFrame:
    gdf_cols = ["geometry"]
    crs = geojson["crs"]["properties"]["name"]

    # add all properties to gdf cols
    for property_key in geojson["features"][0]["properties"].keys():
        gdf_cols.append(property_key)

    gdf = geopandas.GeoDataFrame.from_features(geojson["features"], crs=crs, columns=gdf_cols)

    return gdf

# gets [x,y] of the south west corner of the bbox.
# might only work for european quadrant of the world
def get_south_west_corner_coords_gdf(gdf_bounds) -> list:
    left, bottom, = gdf_bounds
    
    sw_point = Point([left, bottom])

    return list(sw_point.coords)


# returns a list of coordinates for the bounding box polygon
def get_bounds_coords_list(bounds) -> list:
    left, bottom, right, top = bounds

    pol = Polygon([
        [left, top],
        [right, top],
        [right, bottom],
        [left, bottom],
        [left, top]
        ]
    )

    return list(pol.exterior.coords)

def raster_to_base64_png(np_array) -> str:
    # create a pillow image, save it and convert to base64 string
    im = Image.fromarray(np_array)
    output_buffer = BytesIO()
    im.save(output_buffer, "PNG")
    byte_data = output_buffer.getvalue()
    base64_bytes = base64.b64encode(byte_data)
    base64_string = base64_bytes.decode('utf-8')

    return base64_string

