"""
OpenAPI Examples for :class:`education.api.views.CategoryViewSet`.

This module defines reusable OpenAPI examples for documenting the responses of
education categories API endpoints using `drf-spectacular`.

Attributes:
    category_response_only (Dict[str, Any]):
        A detailed representation of a single education category in JSON
        format.

    category_list_response_only (OpenApiExample):
        An OpenAPI example for the list endpoint response in JSON paginated object list format.

    category_retrieve_response_only (OpenApiExample):
        An OpenAPI example for the retrieve endpoint response in JSON single
        object format.

See Also:
    `drf_spectacular.utils.OpenApiExample`
"""

from typing import Any, Dict

from drf_spectacular.utils import OpenApiExample

#: A detailed JSON representation of a single education category.
category_response_only: Dict[str, Any] = {
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "name": "university",
    "code": "university",
    "description": "An institution offering higher education.",
    "created_at": "2025-01-01T12:00:00Z",
    "updated_at": "2025-01-02T12:00:00Z",
    "extras": {"type": "academic"},
}

#: OpenAPI example for the list endpoint response (paginated object list).
category_list_response_only: OpenApiExample = OpenApiExample(
    name="Successful Response",
    value={
        "count": 123,
        "next": "/api/education/catergories/?page=3",
        "previous": "/api/education/catergories/?page=1",
        "results": [category_response_only],
    },
    response_only=True,
)

#: OpenAPI example for the retrieve endpoint response (single object).
category_retrieve_response_only: OpenApiExample = OpenApiExample(
    name="Successful Response",
    value=category_response_only,
    response_only=True,
)
