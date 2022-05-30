from fastapi.testclient import TestClient

from api import app

import json

client = TestClient(app)

test_geojson = {
    "type":
    "FeatureCollection",
    "crs": {
        "type": "name",
        "properties": {
            "name": "EPSG:4326"
        }
    },
    "features": [{
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [10.0046, 53.5405]
        },
        "properties": {
            "some_prop": 45
        }
    }]
}

test_response = {
    'bbox_sw_corner': [(566573.1185048405, 5932868.863374766)],
    'img_width': 1,
    'img_height': 1,
    'bbox_coordinates': [(566573.1185048405, 5932868.863374766),
                         (566573.1185048405, 5932868.863374766),
                         (566573.1185048405, 5932868.863374766),
                         (566573.1185048405, 5932868.863374766),
                         (566573.1185048405, 5932868.863374766)],
    'image_base64_string':
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVR4nGPQBQAALwAuo1OSiAAAAABJRU5ErkJggg=='
}


def test_input_geojson_without_crs():
    broken_geojson = test_geojson.copy()
    del broken_geojson["crs"]

    headers = {"Content-Type":"application/json"}

    response = client.post(
        "/geojson_to_png",
        json = {
            "resolution": 10,
            "property_to_burn": "some_prop",
            "geojson": broken_geojson
        },
        headers = headers
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['body', 'geojson', 'crs'], 
            'msg': 'field required', 
            'type': 'value_error.missing'}
        ]
    }


def test_conversion():
    headers = {"Content-Type":"application/json"}

    response = client.post(
        "/geojson_to_png",
        json = {
            "resolution": 10,
            "property_to_burn": "some_prop",
            "geojson": test_geojson
        },
        headers = headers
    )

    print(response.text)

    assert response.status_code == 200
    assert json.loads(json.dumps(response.json())) == json.loads(json.dumps(test_response))