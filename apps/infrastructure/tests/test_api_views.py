import uuid
from typing import Any, Dict

from django.conf import settings
from django.test import TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings
from rest_framework.test import APIClient

from .factories import CellTowerFactory, FiberOpticFactory

_search_param = api_settings.SEARCH_PARAM
_ordering_param = api_settings.ORDERING_PARAM
_bbox_param = settings.BBOX_PARAM
_tile_param = settings.TILE_PARAM
_point_param = settings.POINT_PARAM
_dist_param = settings.DIST_PARAM


class CellTowerAPITestCase(TestCase):
    """Test suite for the CellTowerViewSet."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = APIClient()
        self.cell_tower = CellTowerFactory.create()

    def test_list_cell_towers(self) -> None:
        """Test that the `list` endpoint returns the correct feature collection of `CellTower`."""
        url = reverse("api:cell-tower-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreCellTowers(response.data)

    def test_list_cell_towers_searching(self) -> None:
        """Test that the `list` endpoint with search filters returns the correct feature collection of `CellTower`."""
        url = reverse("api:cell-tower-list")
        response = self.client.get(url, {_search_param: self.cell_tower.network_type})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreCellTowers(response.data)

    def test_list_cell_towers_ordering(self) -> None:
        """Test that the `list` endpoint with ordering filters returns the correct feature collection of `CellTower`."""  # noqa
        url = reverse("api:cell-tower-list")
        response = self.client.get(url, {_ordering_param: "network_type"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreCellTowers(response.data)

    def test_list_cell_towers_pagination(self) -> None:
        """Test that the `list` endpoint with pagination filters returns the correct feature collection of `CellTower`."""  # noqa
        url = reverse("api:cell-tower-list")
        response = self.client.get(url, {"page": 1, "page_size": 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreCellTowers(response.data)

    def test_list_cell_towers_filtering(self) -> None:
        """Test that the `list` endpoint with field filters returns the correct feature collection of `CellTower`."""
        test_cases = [
            {"network_type": self.cell_tower.network_type},
            {"mcc": self.cell_tower.mcc},
            {"range_gte": self.cell_tower.range},
            {"range_lte": self.cell_tower.range},
            {"range_gte": self.cell_tower.range, "range_lte": self.cell_tower.range},
        ]
        for test_case in test_cases:
            with self.subTest(**test_case):
                url = reverse("api:cell-tower-list")
                response = self.client.get(url, test_case)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertAreCellTowers(response.data)

    def test_list_cell_towers_spatial_filtering(self) -> None:
        """Test that the `list` endpoint with spatial filters returns the correct feature collection of `CellTower`."""
        test_cases = [
            {_bbox_param: "-180,-90,180,90"},
            {_tile_param: "0/0/0"},
            {_point_param: f"{self.cell_tower.geometry.x},{self.cell_tower.geometry.y}", _dist_param: 1000},
        ]
        for test_case in test_cases:
            with self.subTest(**test_case):
                url = reverse("api:cell-tower-list")
                response = self.client.get(url, test_case)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertAreCellTowers(response.data)

    def test_retrieve_cell_tower(self) -> None:
        """Test that the `retrieve` endpoint returns the correct `CellTower` feature."""
        url = reverse("api:cell-tower-detail", kwargs={"uuid": self.cell_tower.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsCellTower(response.data)

    def test_retrieve_cell_tower_not_found(self) -> None:
        """Test that the `retrieve` endpoint returns 404 error, if `CellTower` does not exist."""
        url = reverse("api:cell-tower-detail", kwargs={"uuid": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def assertAreCellTowers(self, data: Dict[str, Any]) -> None:
        """Assert `data` is a correct feature collection of `CellTower`."""
        self.assertEqual(len(data["features"]), 1)
        self.assertIsCellTower(data["features"][0])

    def assertIsCellTower(self, data: Dict[str, Any]) -> None:
        """Assert `data` is a correct `CellTower` feature."""
        self.assertIsNotNone(data["id"])
        self.assertIsNotNone(data["properties"]["network_type"])
        self.assertIsNotNone(data["properties"]["mcc"])
        self.assertIsNotNone(data["geometry"])
        self.assertIsNotNone(data["properties"]["location_is_approximate"])
        self.assertIsNotNone(data["properties"]["range"])
        self.assertIsNotNone(data["properties"]["administrative_area"])
        self.assertIsNotNone(data["properties"]["src_created_at"])
        self.assertIsNotNone(data["properties"]["src_updated_at"])
        self.assertIsNotNone(data["properties"]["created_at"])
        self.assertIsNotNone(data["properties"]["updated_at"])
        self.assertIsNotNone(data["properties"]["extras"])
        self.assertEqual(data["id"], str(self.cell_tower.uuid))


class FiberOpticAPITestCase(TestCase):
    """Test suite for the FiberOpticViewSet."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = APIClient()
        self.fiber_optic = FiberOpticFactory.create()

    def test_list_fiber_optics(self) -> None:
        """Test that the `list` endpoint returns the correct feature collection of `FiberOptic`."""
        url = reverse("api:fiber-optic-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreFiberOptics(response.data)

    def test_list_fiber_optics_searching(self) -> None:
        """Test that the `list` endpoint with search filters returns the correct feature collection of `FiberOptic`."""
        url = reverse("api:fiber-optic-list")
        response = self.client.get(url, {_search_param: self.fiber_optic.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreFiberOptics(response.data)

    def test_list_fiber_optics_ordering(self) -> None:
        """Test that the `list` endpoint with ordering filters returns the correct feature collection of `FiberOptic`."""  # noqa
        url = reverse("api:fiber-optic-list")
        response = self.client.get(url, {_ordering_param: "name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreFiberOptics(response.data)

    def test_list_fiber_optics_pagination(self) -> None:
        """Test that the `list` endpoint with pagination filters returns the correct feature collection of `FiberOptic`."""  # noqa
        url = reverse("api:fiber-optic-list")
        response = self.client.get(url, {"page": 1, "page_size": 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAreFiberOptics(response.data)

    def test_list_fiber_optics_filtering(self) -> None:
        """Test that the `list` endpoint with field filters returns the correct feature collection of `FiberOptic`."""
        test_cases = [
            {"name": self.fiber_optic.name},
        ]
        for test_case in test_cases:
            with self.subTest(**test_case):
                url = reverse("api:fiber-optic-list")
                response = self.client.get(url, test_case)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertAreFiberOptics(response.data)

    def test_list_fiber_optics_spatial_filtering(self) -> None:
        """Test that the `list` endpoint with spatial filters returns the correct feature collection of `FiberOptic`."""  # noqa
        test_cases = [
            {_bbox_param: "-180,-90,180,90"},
            {_tile_param: "0/0/0"},
            {
                _point_param: f"{self.fiber_optic.geometry[-1][-1][0]},{self.fiber_optic.geometry[-1][-1][1]}",
                _dist_param: 1000,
            },
        ]
        for test_case in test_cases:
            with self.subTest(**test_case):
                url = reverse("api:fiber-optic-list")
                response = self.client.get(url, test_case)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertAreFiberOptics(response.data)

    def test_retrieve_fiber_optic(self) -> None:
        """Test that the `retrieve` endpoint returns the correct `FiberOptic` feature."""
        url = reverse("api:fiber-optic-detail", kwargs={"uuid": self.fiber_optic.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsFiberOptic(response.data)

    def test_retrieve_cell_tower_not_found(self) -> None:
        """Test that the `retrieve` endpoint returns 404 error, if `FiberOptic` does not exist."""
        url = reverse("api:fiber-optic-detail", kwargs={"uuid": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def assertAreFiberOptics(self, data: Dict[str, Any]) -> None:
        """Assert `data` is a correct feature collection of `FiberOptic`."""
        self.assertEqual(len(data["features"]), 1)
        self.assertIsFiberOptic(data["features"][0])

    def assertIsFiberOptic(self, data: Dict[str, Any]) -> None:
        """Assert `data` is a correct `FiberOptic` feature."""
        self.assertIsNotNone(data["id"])
        self.assertIsNotNone(data["properties"]["name"])
        self.assertIsNotNone(data["properties"]["description"])
        self.assertIsNotNone(data["geometry"])
        self.assertIsNotNone(data["properties"]["administrative_area"])
        self.assertIsNotNone(data["properties"]["status"])
        self.assertIsNotNone(data["properties"]["operator_name"])
        self.assertIsNotNone(data["properties"]["created_at"])
        self.assertIsNotNone(data["properties"]["updated_at"])
        self.assertIsNotNone(data["properties"]["extras"])
        self.assertEqual(data["id"], str(self.fiber_optic.uuid))
