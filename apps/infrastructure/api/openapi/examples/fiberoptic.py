"""
OpenAPI Examples for `FiberOpticViewSet`.

This module defines reusable OpenAPI examples for documenting the responses of
fiber optics API endpoints using `drf-spectacular`.

Attributes:
    fiberoptic_response_only (Dict[str, Any]):
        A detailed representation of a single fiber optic in GeoJSON format.

    fiberoptic_list_response_only (OpenApiExample):
        An OpenAPI example for the list endpoint response in GeoJSON
        FeatureCollection format.

    fiberoptic_retrieve_response_only (OpenApiExample):
        An OpenAPI example for the retrieve endpoint response in GeoJSON
        Feature format.

See Also:
    `drf_spectacular.utils.OpenApiExample`
"""

from typing import Any, Dict

from drf_spectacular.utils import OpenApiExample

#: A detailed GeoJSON representation of a single fiber optic.
fiberoptic_response_only: Dict[str, Any] = {
    "id": "f29ea7c2-9755-464f-8d18-88a93fa59185",
    "type": "Feature",
    "geometry": {
        "type": "MultiLineString",
        "coordinates": [
            [
                [34.01543159, -11.46017801],
                [34.00156918, -11.42873615],
                [34.00000348, -11.42732043],
                [33.95142826, -11.39383968],
                [33.89836295, -11.38842839],
                [33.87761936, -11.36120956],
                [33.88494056, -11.30957967],
                [33.8810946, -11.27857485],
                [33.87008113, -11.24026372],
                [33.89273643, -11.10202403],
                [33.93082708, -11.03605542],
                [33.97084294, -10.96614783],
                [33.98501954, -10.9361468],
                [34.04431801, -10.89759413],
                [34.08297167, -10.83536036],
                [34.11068924, -10.80314134],
                [34.14029674, -10.74699501],
                [34.16997588, -10.70180313],
                [34.18775996, -10.67404665],
                [34.19678994, -10.64412588],
                [34.18436999, -10.61509913],
                [34.17172755, -10.60131766],
                [34.1690071, -10.57691633],
                [34.20329337, -10.54986566],
                [34.20491277, -10.5260413],
                [34.21116028, -10.38778504],
                [34.19716681, -10.34333042],
                [34.15423815, -10.32392206],
                [34.11883876, -10.29997713],
                [34.10681225, -10.25899959],
                [34.10275809, -10.22360672],
                [34.04588781, -10.17935315],
                [34.00784679, -10.14545944],
                [33.96240863, -10.04406191],
                [33.95539354, -10.0198067],
                [33.91581694, -9.97655263],
                [33.9304048, -9.93449644],
                [33.92894453, -9.89900386],
                [33.88790213, -9.86335897],
                [33.87371256, -9.8106083],
                [33.86599673, -9.70599884],
                [33.81343814, -9.65902093],
                [33.81086438, -9.63797239],
                [33.80681891, -9.6276243],
                [33.79750032, -9.61412648],
                [33.77643251, -9.5946116],
                [33.77584855, -9.5892313],
            ]
        ],
    },
    "properties": {
        "country": "MW",
        "name": "Malawi Telecommunications Ltd (MTL) - STM16",
        "description": "Malawi Telecommunications Ltd (MTL) - STM16",
        "created_at": "2025-01-11T09:59:51.840226Z",
        "updated_at": "2025-01-11T09:59:51.840265Z",
        "extras": {
            "live": True,
            "phase_name": "STM16",
        },
    },
}


#: OpenAPI example for the list endpoint response (FeatureCollection).
fiberoptic_list_response_only: OpenApiExample = OpenApiExample(
    name="Successful Response",
    value={
        "type": "FeatureCollection",
        "count": 123,
        "next": "/api/infrastructure/fiberoptics/?page=3",
        "previous": "/api/infrastructure/fiberoptics/?page=1",
        "features": [fiberoptic_response_only],
    },
    response_only=True,
)

#: OpenAPI example for the retrieve endpoint response (single Feature).
fiberoptic_retrieve_response_only: OpenApiExample = OpenApiExample(
    name="Successful Response",
    value=fiberoptic_response_only,
    response_only=True,
)
