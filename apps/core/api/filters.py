from typing import Any, Dict, List

from django.conf import settings
from django.core.validators import EMPTY_VALUES

from django_filters import rest_framework as filters
from rest_framework.views import View
from rest_framework_gis import filters as gis_filters


class InBBoxFilter(gis_filters.InBBoxFilter):
    """Filter backend for objects within a bounding box.

    This filter allows querying objects by specifying a bounding box (bbox)
    in the query parameter. The bounding box should be provided as a
    comma-separated string in the format `min_lon,min_lat,max_lon,max_lat`.

    Attributes:
        bbox_param (str):
            The URL query parameter containing the bounding box.
            Default to `in_bbox`.
    """

    #: The URL query parameter which contains the bbox.
    bbox_param: str = settings.BBOX_PARAM

    def get_schema_operation_parameters(self, view: View) -> List[Dict[str, Any]]:
        """Generate schema parameters for API documentation.

        Args:
            view (:class:`rest_framework.views.View`):
                The view using this filter.

        Returns:
            List[Dict[str, Any]]:
                A list of schema operation parameters for the `bbox` filter.
        """
        return [
            {
                "name": self.bbox_param,
                "required": False,
                "in": "query",
                "description": (
                    f"Filter by a bounding box, defined as a comma-separated string: "
                    f"`{self.bbox_param}=min_lon,min_lat,max_lon,max_lat`. "
                    f"e.g, `?{self.bbox_param}=-180,-90,180,90`."
                ),
                "schema": {
                    "type": "string",
                },
            },
        ]


class TMSTileFilter(gis_filters.TMSTileFilter):
    """Filter backend for objects within a TMS (Tile Map Service) tile.

    This filter allows querying objects by specifying a tile in the query parameter.
    The tile should be provided in the format `Z/X/Y`, where:
      - `Z` is the zoom level.
      - `X` is the tile column.
      - `Y` is the tile row.

    Attributes:
        tile_param (str):
            The URL query parameter containing the tile address.
            Default to `in_tile`.
    """

    #: The URL query parameter which contains the tile address.
    tile_param: str = settings.TILE_PARAM

    def get_schema_operation_parameters(self, view: View) -> List[Dict[str, Any]]:
        """Generate schema parameters for API documentation.

        Args:
            view (:class:`rest_framework.views.View`):
                The view using this filter.

        Returns:
            List[Dict[str, Any]]:
                A list of schema operation parameters for the TMS tile filter.
        """
        return [
            {
                "name": self.tile_param,
                "required": False,
                "in": "query",
                "description": (
                    f"Filter by a bounding box defined by a TMS (Tile Map Service) tile address, "
                    f"specified as `Z/X/Y`. e.g, `?{self.tile_param}=0/0/0`."
                ),
                "schema": {
                    "type": "string",
                },
            },
        ]


class DistanceToPointFilter(gis_filters.DistanceToPointFilter):
    """Filter backend for querying objects by distance to a specific point.

    This filter allows querying objects within a specified distance (in meters)
    from a given geographic point.

    Attributes:
        dist_param (str):
            The URL query parameter that specifies the distance in meters.
            Defaults to `radius`.

        point_param (str):
            The URL query parameter that specifies the geographic point as `x,y`. Defaults to `point`.
    """

    #: The URL query parameter which contains the distance in meters.
    dist_param: str = settings.DIST_PARAM

    #: The URL query parameter which contains the geographic point.
    point_param: str = settings.POINT_PARAM

    def get_schema_operation_parameters(self, view: View) -> List[Dict[str, Any]]:
        """Generate schema parameters for API documentation.

        Args:
            view (:class:`rest_framework.views.View`):
                The view using this filter.

        Returns:
            List[Dict[str, Any]]:
                A list of schema operation parameters for the distance filter.
        """
        return [
            {
                "name": self.dist_param,
                "required": False,
                "in": "query",
                "description": (
                    f"Filter by distance (in meters) from a specified point. "
                    f"Specify the distance as `{self.dist_param}=value`, e.g., `?{self.dist_param}=1000`."
                ),
                "schema": {"type": "number", "format": "float"},
            },
            {
                "name": self.point_param,
                "required": False,
                "in": "query",
                "description": (
                    f"Filter by distance from a specific geographic point. "
                    f"Specify the point as `{self.point_param}=x,y`, e.g., `?{self.point_param}=0,10`."
                ),
                "schema": {"type": "string"},
            },
        ]


class EmptyValueFilter(filters.BooleanFilter):

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        exclude = self.exclude ^ (value is False)
        method = qs.exclude if exclude else qs.filter

        return method(**{f"{self.field_name}__in": EMPTY_VALUES})
