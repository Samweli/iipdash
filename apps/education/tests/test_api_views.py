import uuid
from typing import Any, Dict

from django.conf import settings
from django.test import TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings
from rest_framework.test import APIClient

from .factories import CategoryFactory, InstitutionFactory, OwnershipFactory

_search_param = api_settings.SEARCH_PARAM
_ordering_param = api_settings.ORDERING_PARAM
_bbox_param = settings.BBOX_PARAM
_tile_param = settings.TILE_PARAM
_point_param = settings.POINT_PARAM
_dist_param = settings.DIST_PARAM


class CategoryAPITestCase(TestCase):
    """Test suite for the CategoryViewSet."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = APIClient()
        self.category = CategoryFactory.create()

    def test_list_categories(self) -> None:
        """Test that the `list` endpoint returns the correct paginated list of `Category`."""
        url = reverse("api:category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreCategories(response.data)

    def test_list_categories_searching(self) -> None:
        """Test that the `list` endpoint with search filters returns the correct paginated list of `Category`."""

        url = reverse("api:category-list")
        response = self.client.get(url, {_search_param: self.category.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreCategories(response.data)

    def test_list_categories_ordering(self) -> None:
        """Test that the `list` endpoint with ordering filters returns the correct paginated list of `Category`."""
        url = reverse("api:category-list")
        response = self.client.get(url, {_ordering_param: "name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreCategories(response.data)

    def test_list_categories_pagination(self) -> None:
        """Test that the `list` endpoint with pagination filters returns the correct paginated list of `Category`."""
        url = reverse("api:category-list")
        response = self.client.get(url, {"page": 1, "page_size": 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreCategories(response.data)

    def test_list_categories_filtering(self) -> None:
        """Test that the `list` endpoint with field filters returns the correct paginated list of `Category`."""
        url = reverse("api:category-list")
        response = self.client.get(url, {"name": self.category.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreCategories(response.data)

    def test_retrieve_category(self) -> None:
        """Test that the `retrieve` endpoint returns the correct `Category`."""
        url = reverse("api:category-detail", kwargs={"uuid": self.category.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsCategory(response.data)

    def test_retrieve_category_not_found(self) -> None:
        """Test that the `retrieve` endpoint returns 404 error, if `Category` does not exist."""
        url = reverse("api:category-detail", kwargs={"uuid": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def assertAreCategories(self, data: Dict[str, Any]) -> None:
        """Assert `data` is a correct list of `Category`."""
        self.assertIn("count", data)
        self.assertIn("next", data)
        self.assertIn("previous", data)
        self.assertIn("results", data)
        self.assertEqual(len(data["results"]), 1)
        self.assertIsCategory(data["results"][0])

    def assertIsCategory(self, data: Dict[str, Any]) -> None:
        """Assert `data` is a correct `Category`."""
        self.assertIsNotNone(data["uuid"])
        self.assertIsNotNone(data["name"])
        self.assertIsNotNone(data["code"])
        self.assertIsNotNone(data["description"])
        self.assertIsNotNone(data["created_at"])
        self.assertIsNotNone(data["updated_at"])
        self.assertIsNotNone(data["extras"])
        self.assertEqual(data["uuid"], str(self.category.uuid))


class OwnershipAPITestCase(TestCase):
    """Test suite for the OwnershipViewSet."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = APIClient()
        self.ownership = OwnershipFactory.create()

    def test_list_ownerships(self) -> None:
        """Test that the `list` endpoint returns the correct paginated list of `Ownership`."""
        url = reverse("api:ownership-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreOwnerships(response.data)

    def test_list_ownerships_searching(self) -> None:
        """Test that the `list` endpoint with search filters returns the correct paginated list of `Ownership`."""
        url = reverse("api:ownership-list")
        response = self.client.get(url, {_search_param: self.ownership.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreOwnerships(response.data)

    def test_list_ownerships_ordering(self) -> None:
        """Test that the `list` endpoint with ordering filters returns the correct paginated list of `Ownership`."""
        url = reverse("api:ownership-list")
        response = self.client.get(url, {_ordering_param: "name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreOwnerships(response.data)

    def test_list_ownerships_pagination(self) -> None:
        """Test that the `list` endpoint with pagination filters returns the correct paginated list of `Ownership`."""
        url = reverse("api:ownership-list")
        response = self.client.get(url, {"page": 1, "page_size": 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreOwnerships(response.data)

    def test_list_ownerships_filtering(self) -> None:
        """Test that the `list` endpoint with field filters returns the correct paginated list of `Ownership`."""
        url = reverse("api:ownership-list")
        response = self.client.get(url, {"name": self.ownership.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreOwnerships(response.data)

    def test_retrieve_ownership(self) -> None:
        """Test that the `retrieve` endpoint returns the correct `Ownership`."""
        url = reverse("api:ownership-detail", kwargs={"uuid": self.ownership.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsOwnership(response.data)

    def test_retrieve_ownership_not_found(self) -> None:
        """Test that the `retrieve` endpoint returns 404 error, if `Ownership` does not exist."""
        url = reverse("api:category-detail", kwargs={"uuid": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def assertAreOwnerships(self, data: Dict[str, Any]) -> None:
        """Assert `data` is a correct list of `Ownership`."""
        self.assertIn("count", data)
        self.assertIn("next", data)
        self.assertIn("previous", data)
        self.assertIn("results", data)
        self.assertEqual(len(data["results"]), 1)
        self.assertIsOwnership(data["results"][0])

    def assertIsOwnership(self, data: Dict[str, Any]) -> None:
        """Assert `data` is a correct `Ownership`."""
        self.assertIsNotNone(data["uuid"])
        self.assertIsNotNone(data["name"])
        self.assertIsNotNone(data["code"])
        self.assertIsNotNone(data["description"])
        self.assertIsNotNone(data["created_at"])
        self.assertIsNotNone(data["updated_at"])
        self.assertIsNotNone(data["extras"])
        self.assertEqual(data["uuid"], str(self.ownership.uuid))


class InstitutionAPITestCase(TestCase):
    """Test suite for the InstitutionViewSet."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = APIClient()
        self.institution = InstitutionFactory.create()

    def test_list_institutions(self) -> None:
        """Test that the `list` endpoint returns the correct feature collection of `Institution`."""
        url = reverse("api:institution-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreInstitutions(response.data)

    def test_list_institutions_searching(self) -> None:
        """Test that the `list` endpoint with search filters returns the correct feature collection of `Institution`."""  # noqa
        url = reverse("api:institution-list")
        response = self.client.get(url, {_search_param: self.institution.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreInstitutions(response.data)

    def test_list_institutions_ordering(self) -> None:
        """Test that the `list` endpoint with ordering filters returns the correct feature collection of `Institution`."""  # noqa
        url = reverse("api:institution-list")
        response = self.client.get(url, {_ordering_param: "name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreInstitutions(response.data)

    def test_list_institutions_pagination(self) -> None:
        """Test that the `list` endpoint with pagination filters returns the correct feature collection of `Institution`."""  # noqa
        url = reverse("api:institution-list")
        response = self.client.get(url, {"page": 1, "page_size": 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreInstitutions(response.data)

    def test_list_institutions_filtering(self) -> None:
        """Test that the `list` endpoint with field filters returns the correct feature collection of `Institution`."""
        test_cases = [
            {"country_in": self.institution.administrative_area.country.code},
            {"category_in": self.institution.category.uuid},
            {"name": self.institution.name},
            {"ownership_in": self.institution.ownership.uuid},
            {"code": self.institution.code},
            {"administrative_area_in": self.institution.administrative_area.uuid},
            {"has_electricity": self.institution.has_electricity},
            {"has_fiber_optic": self.institution.has_fiber_optic},
            {"fon_distance_gte": self.institution.fon_distance},
            {"fon_distance_lte": self.institution.fon_distance},
            {"fon_distance_gte": self.institution.fon_distance, "fon_distance_lte": self.institution.fon_distance},
        ]
        for test_case in test_cases:
            with self.subTest(**test_case):
                url = reverse("api:institution-list")
                response = self.client.get(url, test_case)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertAreInstitutions(response.data)

    def test_list_institutions_spatial_filtering(self) -> None:
        """Test that the `list` endpoint with spatial filters returns the correct feature collection of `Institution`."""  # noqa
        test_cases = [
            {_bbox_param: "-180,-90,180,90"},
            {_tile_param: "0/0/0"},
            {
                _point_param: f"{self.institution.geometry.x},{self.institution.geometry.y}",
                _dist_param: 1000,
            },
        ]
        for test_case in test_cases:
            with self.subTest(**test_case):
                url = reverse("api:institution-list")
                response = self.client.get(url, test_case)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertAreInstitutions(response.data)

    def test_retrieve_institution(self) -> None:
        """Test that the `retrieve` endpoint returns the correct `Institution` feature."""
        url = reverse("api:institution-detail", kwargs={"uuid": self.institution.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstitution(response.data)

    def test_retrieve_institution_not_found(self) -> None:
        """Test that the `retrieve` endpoint returns 404 error, if `Institution` does not exist."""
        url = reverse("api:institution-detail", kwargs={"uuid": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def assertAreInstitutions(self, data: Dict[str, Any]) -> None:
        """Assert `data` is a correct feature collection of `Institution`."""
        self.assertEqual(len(data["features"]), 1)
        self.assertIsInstitution(data["features"][0])

    def assertIsInstitution(self, data: Dict[str, Any]) -> None:
        """Assert `data` is a correct `Institution` feature."""
        self.assertIsNotNone(data["id"])
        self.assertIsNotNone(data["properties"]["category"])
        self.assertIsNotNone(data["properties"]["name"])
        self.assertIsNotNone(data["properties"]["ownership"])
        self.assertIsNotNone(data["properties"]["description"])
        self.assertIsNotNone(data["properties"]["code"])
        self.assertIsNotNone(data["properties"]["postal_code"])
        self.assertIsNotNone(data["properties"]["address"])
        self.assertIsNotNone(data["properties"]["phone"])
        self.assertIsNotNone(data["properties"]["fax"])
        self.assertIsNotNone(data["properties"]["email"])
        self.assertIsNotNone(data["properties"]["website"])
        self.assertIsNotNone(data["properties"]["administrative_area"])
        self.assertIsNotNone(data["geometry"])
        self.assertIsNotNone(data["properties"]["has_electricity"])
        self.assertIsNotNone(data["properties"]["has_fiber_optic"])
        self.assertIsNotNone(data["properties"]["fon_distance"])
        self.assertIsNotNone(data["properties"]["osm_id"])
        self.assertIsNotNone(data["properties"]["osm_type"])
        self.assertIsNotNone(data["properties"]["created_at"])
        self.assertIsNotNone(data["properties"]["updated_at"])
        self.assertIsNotNone(data["properties"]["extras"])
        self.assertEqual(data["id"], str(self.institution.uuid))
