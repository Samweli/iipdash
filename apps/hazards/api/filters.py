from typing import List, Type

from django.utils.translation import gettext_lazy as _

from django_filters import rest_framework as filters

from core.api.filters import EmptyValueFilter

from ..models import ExposureCoverage, HazardExposure

__all__ = ["ExposureCoverageFilter", "HazardExposureFilter"]


class ExposureCoverageFilter(filters.FilterSet):
    """FilterSet for the :class:`hazards.models.ExposureCoverage` model.

    This filter allows filtering `ExposureCoverage` objects based on specific
    fields.

    Examples:
        Filter by country code (exact match):
            `/api/hazards/exposure-coverage/?country=MW`

        Filter by multiple country codes (in comparison):
            `/api/hazards/exposure-coverage/?country_in=MW,ZM`

        Filter by administrative area UUID (exact match):
            `/api/hazards/exposure-coverage/?administrative_area=04bcbe53-
            98da-4ff5-96a8-d626c6da45cc`

        Filter by multiple administrative area UUIDs (in comparison):
            `/api/hazards/exposure-coverage/?administrative_area_in=04bcbe53-
            98da-4ff5-96a8-d626c6da45cc,032ffe37-67d6-40d4-a65d-144f12bbd493`

        Filtering by administrative area level (exact match):
            `/api/hazards/exposure-coverage/?administrative_area_level=1`

        Filtering by empty tiff value:
            `/api/hazards/exposure-coverage/?tiff_empty=true`

    Attributes:
        country (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `administrative_area__country` field
            of the `ExposureCoverage` model using `exact, case-insensitive` comparison.

        country_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `administrative_area__country` field
            of the `ExposureCoverage` model using `in` comparison.

        administrative_area (:class:`django_filters.rest_framework.filters.UUIDFilter`):
            A filter for matching the `administrative_area__uuid` field of
            the `ExposureCoverage` model using `uuid equal` comparison.

        administrative_area_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `administrative_area__uuid` field of
            the `ExposureCoverage` model using `in` comparison.

        administrative_area_level (:class:`django_filters.rest_framework.filters.NumberFilter`):
            A filter for matching the `administrative_area__depth` field
            of the `ExposureCoverage` model using `equal` comparison.

        tiff_empty (:class:`core.api.filters.EmptyValueFilter`):
            A filter for matching the `tiff` field
            of the `ExposureCoverage` model using `empty values` comparison.
    """

    #: Filter by country code (exact match, case-insensitive)
    country: filters.CharFilter = filters.CharFilter(
        field_name="administrative_area__country",
        lookup_expr="iexact",
        help_text=_("Filter by country code."),
    )

    #: Filter by multiple country codes
    country_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="administrative_area__country",
        help_text=_("Filter by multiple country codes."),
    )

    #: Filter by administrative area UUID (exact match)
    administrative_area: filters.UUIDFilter = filters.UUIDFilter(
        field_name="administrative_area__uuid",
        help_text=_("Filter by administrative area UUID."),
    )

    #: Filter by multiple administrative area UUIDs
    administrative_area_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="administrative_area__uuid",
        help_text=_("Filter by multiple administrative area UUIDs."),
    )

    #: Filter by administrative area level (exact match)
    administrative_area_level: filters.NumberFilter = filters.NumberFilter(
        field_name="administrative_area__depth",
        help_text=_("Filter by administrative area level."),
    )

    #: Filter by empty tiff value
    tiff_empty: EmptyValueFilter = EmptyValueFilter(
        field_name=_("tiff"),
        help_text=_("Filter by empty tiff value."),
    )

    class Meta:
        """
        Metadata for the :class:`ExposureCoverageFilter`.

        Attributes:
            model (Type[ExposureCoverage]):
                A Django model associated with this filter.
                In this case, it's the :class:`ExposureCoverage` model.

            fields (List[str]):
                A list of field names (i.e query parameters) available for filtering.
        """

        model: Type[ExposureCoverage] = ExposureCoverage
        fields: List[str] = [
            "country",
            "country_in",
            "administrative_area",
            "administrative_area_in",
            "administrative_area_level",
            "tiff_empty",
        ]


class HazardExposureFilter(filters.FilterSet):
    """FilterSet for the :class:`hazards.models.HazardExposure` model.

    This filter allows filtering `HazardExposure` objects based on specific
    fields.

    Examples:
        Filter by country code (exact match):
            `/api/hazards/hazard-exposures/?country=MW`

        Filter by multiple country codes (in comparison):
            `/api/hazards/hazard-exposures/?country_in=MW,ZM`

        Filter by administrative area UUID (exact match):
            `/api/hazards/hazard-exposures/?administrative_area=04bcbe53-
            98da-4ff5-96a8-d626c6da45cc`

        Filter by multiple administrative area UUIDs (in comparison):
            `/api/hazards/hazard-exposures/?administrative_area_in=04bcbe53-
            98da-4ff5-96a8-d626c6da45cc,032ffe37-67d6-40d4-a65d-144f12bbd493`

        Filtering by administrative area level (exact match):
            `/api/hazards/hazard-exposures/?administrative_area_level=1`

    Attributes:
        country (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `coverage__administrative_area__country` field
            of the `HazardExposure` model using `exact, case-insensitive` comparison.

        country_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `coverage__administrative_area__country` field
            of the `HazardExposure` model using `in` comparison.

        administrative_area (:class:`django_filters.rest_framework.filters.UUIDFilter`):
            A filter for matching the `coverage__administrative_area__uuid` field of
            the `HazardExposure` model using `uuid equal` comparison.

        administrative_area_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `coverage__administrative_area__uuid` field of
            the `HazardExposure` model using `in` comparison.

        administrative_area_level (:class:`django_filters.rest_framework.filters.NumberFilter`):
            A filter for matching the `coverage__administrative_area__depth` field
            of the `HazardExposure` model using `equal` comparison.
    """

    #: Filter by country code (exact match, case-insensitive)
    country: filters.CharFilter = filters.CharFilter(
        field_name="coverage__administrative_area__country",
        lookup_expr="iexact",
        help_text=_("Filter by country code."),
    )

    #: Filter by multiple country codes
    country_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="coverage__administrative_area__country",
        help_text=_("Filter by multiple country codes."),
    )

    #: Filter by administrative area UUID (exact match)
    administrative_area: filters.UUIDFilter = filters.UUIDFilter(
        field_name="coverage__administrative_area__uuid",
        help_text=_("Filter by administrative area UUID."),
    )

    #: Filter by multiple administrative area UUIDs
    administrative_area_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="coverage__administrative_area__uuid",
        help_text=_("Filter by multiple administrative area UUIDs."),
    )

    #: Filter by administrative area level (exact match)
    administrative_area_level: filters.NumberFilter = filters.NumberFilter(
        field_name="coverage__administrative_area__depth",
        help_text=_("Filter by administrative area level."),
    )

    hazard_code_in = filters.BaseCSVFilter(field_name="hazards_codes", lookup_expr="overlap")
    urbanization_degree_code_in = filters.BaseInFilter(field_name="urbanization_degree__code")

    class Meta:
        """
        Metadata for the :class:`HazardExposureFilter`.

        Attributes:
            model (Type[HazardExposure]):
                A Django model associated with this filter.
                In this case, it's the :class:`HazardExposure` model.

            fields (List[str]):
                A list of field names (i.e query parameters) available for filtering.
        """

        model: Type[HazardExposure] = HazardExposure
        fields: List[str] = [
            "country",
            "country_in",
            "administrative_area",
            "administrative_area_in",
            "administrative_area_level",
            "hazard_code_in",
            "urbanization_degree_code_in",
        ]
