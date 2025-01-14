"""
OpenAPI Examples for :class:`education.api.views.OwnershipViewSet`.

This module defines reusable OpenAPI examples for documenting the responses of
educational institution ownerships API endpoints using `drf-spectacular`.

Attributes:
    ownership_response_only (Dict[str, Any]):
        A detailed representation of a single educational institution
        ownership in JSON format.

    ownership_list_response_only (OpenApiExample):
        An OpenAPI example for the list endpoint response in JSON paginated object list format.

    ownership_retrieve_response_only (OpenApiExample):
        An OpenAPI example for the retrieve endpoint response in JSON single
        object format.

See Also:
    `drf_spectacular.utils.OpenApiExample`
"""

from typing import Any, Dict

from drf_spectacular.utils import OpenApiExample

#: A detailed JSON representation of a single educational institution ownership.
ownership_response_only: Dict[str, Any] = {
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "name": "public",
    "code": "public",
    "description": "An educational institution operated by local, state, or national governments.",
    "created_at": "2025-01-01T12:00:00Z",
    "updated_at": "2025-01-02T12:00:00Z",
    "extras": {"type": "academic"},
}

#: OpenAPI example for the list endpoint response (paginated object list).
ownership_list_response_only: OpenApiExample = OpenApiExample(
    name="Successful Response",
    value={
        "count": 123,
        "next": "/api/education/ownerships/?page=3",
        "previous": "/api/education/ownerships/?page=1",
        "results": [ownership_response_only],
    },
    response_only=True,
)

#: OpenAPI example for the retrieve endpoint response (single object).
ownership_retrieve_response_only: OpenApiExample = OpenApiExample(
    name="Successful Response",
    value=ownership_response_only,
    response_only=True,
)
