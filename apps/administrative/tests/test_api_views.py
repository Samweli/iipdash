import uuid
from typing import Any, Dict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings
from rest_framework.test import APIClient

from .factories import AreaFactory

_search_param = api_settings.SEARCH_PARAM
_ordering_param = api_settings.ORDERING_PARAM
_bbox_param = settings.BBOX_PARAM
_tile_param = settings.TILE_PARAM
_point_param = settings.POINT_PARAM
_dist_param = settings.DIST_PARAM

User = get_user_model()

_test_username = "testuser"
_test_password = "12mhud93pkqo_"


class AreaAPITestCase(TestCase):
    """Test suite for the AreaViewSet."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = APIClient()

        user = User.objects.create_user(username=_test_username, password=_test_password)
        self.client.force_login(user)

        self.area = AreaFactory.create(depth=1)

    def test_list_areas(self) -> None:
        """Test that the `list` endpoint returns the correct feature collection of `Area`."""
        url = reverse("api:area-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreAreas(response.data)

    def test_list_areas_searching(self) -> None:
        """Test that the `list` endpoint with search filters returns the correct feature collection of `Area`."""
        url = reverse("api:area-list")
        response = self.client.get(url, {_search_param: self.area.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreAreas(response.data)

    def test_list_areas_ordering(self) -> None:
        """Test that the `list` endpoint with ordering filters returns the correct feature collection of `Area`."""  # noqa
        url = reverse("api:area-list")
        response = self.client.get(url, {_ordering_param: "name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreAreas(response.data)

    def test_retrieve_area(self) -> None:
        """Test that the `retrieve` endpoint returns the correct `Area` feature."""
        url = reverse("api:area-detail", kwargs={"uuid": self.area.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsArea(response.data)

    def test_list_areas_pagination(self) -> None:
        """Test that the `list` endpoint with pagination filters returns the correct feature collection of `Area`."""  # noqa
        url = reverse("api:area-list")
        response = self.client.get(url, {"page": 1, "page_size": 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreAreas(response.data)

    def test_list_areas_filtering(self) -> None:
        """Test that the `list` endpoint with field filters returns the correct feature collection of `Area`."""
        test_cases = [
            {"level": self.area.depth},
            {"country": self.area.country.code},
        ]
        for test_case in test_cases:
            with self.subTest(**test_case):
                url = reverse("api:area-list")
                response = self.client.get(url, test_case)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertAreAreas(response.data)

    def test_list_areas_spatial_filtering(self) -> None:
        """Test that the `list` endpoint with spatial filters returns the correct feature collection of `Area`."""  # noqa
        test_cases = [
            {_bbox_param: "-180,-90,180,90"},
            {_tile_param: "0/0/0"},
            {
                _point_param: f"{self.area.geometry[-1][-1][0][0]},{self.area.geometry[-1][-1][0][1]}",
                _dist_param: 1000,
            },
        ]
        for test_case in test_cases:
            with self.subTest(**test_case):
                url = reverse("api:area-list")
                response = self.client.get(url, test_case)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertAreAreas(response.data)

    def test_retrieve_area_not_found(self) -> None:
        """Test that the `retrieve` endpoint returns 404 error, if `Area` does not exist."""
        url = reverse("api:area-detail", kwargs={"uuid": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def assertAreAreas(self, data: Dict[str, Any]) -> None:
        """Assert `data` is a correct feature collection of `Area`."""
        self.assertEqual(len(data["features"]), 1)
        self.assertIsArea(data["features"][0])

    def assertIsArea(self, data: Dict[str, Any]) -> None:
        """Assert `data` is a correct `Area` feature."""
        self.assertIsNotNone(data["id"])
        self.assertIsNotNone(data["properties"]["type_code"])
        self.assertIsNotNone(data["properties"]["country"])
        self.assertIsNotNone(data["properties"]["name"])
        self.assertIsNotNone(data["properties"]["code"])
        self.assertIsNotNone(data["properties"]["description"])
        self.assertIsNotNone(data["properties"]["full_name"])
        self.assertIsNotNone(data["properties"]["population"])
        self.assertIsNotNone(data["properties"]["population_male"])
        self.assertIsNotNone(data["properties"]["population_female"])
        self.assertIsNotNone(data["properties"]["population_year"])
        self.assertIsNotNone(data["geometry"])
        self.assertIsNotNone(data["properties"]["area"])
        self.assertIsNotNone(data["properties"]["created_at"])
        self.assertIsNotNone(data["properties"]["updated_at"])
        self.assertIsNotNone(data["properties"]["extras"])
        self.assertEqual(data["id"], str(self.area.uuid))
