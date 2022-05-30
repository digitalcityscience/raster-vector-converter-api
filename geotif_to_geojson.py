import os
import json
import math
import rasterio.features
import geopandas

# converts tif to geojson and returns feature array
def convert_raster_to_gdf(tif_path, crs) -> geopandas.GeoDataFrame:
    features = []
    
    dataset = rasterio.open(tif_path)
    # Read the dataset's valid data mask as a ndarray.
    mask = dataset.read(1)

    # Extract feature shapes and values from the array.
    for geom, val in rasterio.features.shapes(
            mask, transform=dataset.transform):

        if math.isnan(val):
            # ignore no values
            continue
        
        # create geojson like feature
        feature = {
            "type": "Feature",
            "geometry": geom,
            "properties": {"value": round(val)}
        }   
        # append feature to geojson
        features.append(feature)

    # create gdf from feature array
    gdf = geopandas.GeoDataFrame.from_features(features, crs=crs,
                                               columns=["geometry", "value"])
    # geopandas also automatically merges all polygons with same values
    gdf = gdf.dissolve(by="value")

    return gdf


# make GeoDataFrame from project area
def get_project_area_as_gdf():
    project_area_file_name = "project_area_utm.geojson"
    project_area_path = os.getcwd() + "/" + project_area_file_name

    with open(project_area_path, "r") as f:
        project_area_json = json.load(f)

    project_area_gdf = geopandas.GeoDataFrame.from_features(
        project_area_json["features"],
        crs=project_area_json["crs"]["properties"]["name"]
    )

    return project_area_gdf


if __name__ == "__main__":
    
    # data folder
    data_path = os.getcwd() + "/" + "data"
    
    # tif file to convert
    input_tif = data_path + "/" + "input.tif"

    # convert to geopandas geodataframe
    gdf = convert_raster_to_gdf(input_tif) 

    # clip result geojson to project area
    gdf = geopandas.clip(gdf, get_project_area_as_gdf())

    # Use Geopandas to reproject all features to EPSG:4326
    gdf = gdf.to_crs("EPSG:4326")

    # save as geojson
    gdf.to_file(data_path + "/" + 'output.geojson', driver='GeoJSON')

    print("finished conversion")