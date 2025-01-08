import uuid

from django.test import TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings
from rest_framework.test import APIClient

from .factories import CellTowerFactory

_search_param = api_settings.SEARCH_PARAM
_ordering_param = api_settings.ORDERING_PARAM


class CellTowerAPITestCase(TestCase):
    """Test suite for the CellTowerViewSet."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = APIClient()
        self.cell_tower = CellTowerFactory.create()

    def test_list_cell_towers(self) -> None:
        """Test that the `list` endpoint returns the correct feature collection of `CellTower`."""
        url = reverse("api:celltower-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["features"]), 1)
        self.assertIsNotNone(response.data["features"][0]["id"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["network_type"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["mcc"])
        self.assertIsNotNone(response.data["features"][0]["geometry"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["location_is_approximate"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["range"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["administrative_area"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["src_created_at"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["src_updated_at"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["created_at"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["updated_at"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["extras"])
        self.assertEqual(response.data["features"][0]["id"], str(self.cell_tower.uuid))

    def test_list_cell_towers_searching(self) -> None:
        """Test that the `list` endpoint with search filters returns the correct feature collection of `CellTower`."""

        url = reverse("api:celltower-list")
        response = self.client.get(url, {_search_param: self.cell_tower.network_type})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["features"]), 1)
        self.assertIsNotNone(response.data["features"][0]["id"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["network_type"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["mcc"])
        self.assertIsNotNone(response.data["features"][0]["geometry"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["location_is_approximate"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["range"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["administrative_area"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["src_created_at"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["src_updated_at"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["created_at"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["updated_at"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["extras"])
        self.assertEqual(response.data["features"][0]["id"], str(self.cell_tower.uuid))

    def test_list_cell_towers_ordering(self) -> None:
        """Test that the `list` endpoint with ordering filters returns the correct feature collection of `CellTower`."""  # noqa
        url = reverse("api:celltower-list")
        response = self.client.get(url, {_ordering_param: "network_type"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["features"]), 1)
        self.assertIsNotNone(response.data["features"][0]["id"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["network_type"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["mcc"])
        self.assertIsNotNone(response.data["features"][0]["geometry"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["location_is_approximate"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["range"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["administrative_area"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["src_created_at"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["src_updated_at"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["created_at"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["updated_at"])
        self.assertIsNotNone(response.data["features"][0]["properties"]["extras"])
        self.assertEqual(response.data["features"][0]["id"], str(self.cell_tower.uuid))

    def test_retrieve_cell_tower(self) -> None:
        """Test that the `retrieve` endpoint returns the correct `CellTower` feature."""
        url = reverse("api:celltower-detail", kwargs={"uuid": self.cell_tower.uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["id"])
        self.assertIsNotNone(response.data["properties"]["network_type"])
        self.assertIsNotNone(response.data["properties"]["mcc"])
        self.assertIsNotNone(response.data["geometry"])
        self.assertIsNotNone(response.data["properties"]["location_is_approximate"])
        self.assertIsNotNone(response.data["properties"]["range"])
        self.assertIsNotNone(response.data["properties"]["administrative_area"])
        self.assertIsNotNone(response.data["properties"]["src_created_at"])
        self.assertIsNotNone(response.data["properties"]["src_updated_at"])
        self.assertIsNotNone(response.data["properties"]["created_at"])
        self.assertIsNotNone(response.data["properties"]["updated_at"])
        self.assertIsNotNone(response.data["properties"]["extras"])
        self.assertEqual(response.data["id"], str(self.cell_tower.uuid))

    def test_retrieve_cell_tower_not_found(self) -> None:
        """Test that the `retrieve` endpoint returns 404 error, if `CellTower` does not exist."""
        url = reverse("api:celltower-detail", kwargs={"uuid": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
