"""
OpenAPI Examples for `CellTowerViewSet`.

This module defines reusable OpenAPI examples for documenting the responses of
cell towers API endpoints using `drf-spectacular`.

Attributes:
    cell_tower_response_only (Dict[str, Any]):
        A detailed representation of a single cell tower in GeoJSON format.

    cell_tower_list_response_only (OpenApiExample):
        An OpenAPI example for the list endpoint response in GeoJSON
        FeatureCollection format.

    cell_tower_retrieve_response_only (OpenApiExample):
        An OpenAPI example for the retrieve endpoint response in GeoJSON
        Feature format.

See Also:
    `drf_spectacular.utils.OpenApiExample`
"""

from typing import Any, Dict

from drf_spectacular.utils import OpenApiExample

#: A detailed GeoJSON representation of a single cell tower.
cell_tower_response_only: Dict[str, Any] = {
    "id": "a5137eb2-c867-42c1-9cda-0809f3306547",
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [28.330438, -15.394306]},
    "properties": {
        "administrative_area": {
            "uuid": "7d18bc44-c76f-4512-82bf-2a77f7a4bda3",
            "name": "Lusaka",
            "country": "ZM",
        },
        "network_type": "GSM",
        "mcc": 645,
        "location_is_approximate": True,
        "range": 5216,
        "src_created_at": "2015-03-14T16:44:20Z",
        "src_updated_at": "2017-05-09T10:02:29Z",
        "created_at": "2025-01-08T03:56:24.320893Z",
        "updated_at": "2025-01-08T03:56:24.320916Z",
        "extras": {
            "measurements": 316,
        },
    },
}

#: OpenAPI example for the list endpoint response (FeatureCollection).
cell_tower_list_response_only: OpenApiExample = OpenApiExample(
    name="Successful Response",
    value={
        "type": "FeatureCollection",
        "features": [cell_tower_response_only],
    },
    response_only=True,
)

#: OpenAPI example for the retrieve endpoint response (single Feature).
cell_tower_retrieve_response_only: OpenApiExample = OpenApiExample(
    name="Successful Response",
    value=cell_tower_response_only,
    response_only=True,
)
