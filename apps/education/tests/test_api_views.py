import uuid

from django.test import TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings
from rest_framework.test import APIClient

from .factories import CategoryFactory, OwnershipFactory

_search_param = api_settings.SEARCH_PARAM
_ordering_param = api_settings.ORDERING_PARAM


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
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNotNone(response.data["results"][0]["uuid"])
        self.assertIsNotNone(response.data["results"][0]["name"])
        self.assertIsNotNone(response.data["results"][0]["code"])
        self.assertIsNotNone(response.data["results"][0]["description"])
        self.assertIsNotNone(response.data["results"][0]["created_at"])
        self.assertIsNotNone(response.data["results"][0]["updated_at"])
        self.assertIsNotNone(response.data["results"][0]["extras"])
        self.assertEqual(response.data["results"][0]["uuid"], str(self.category.uuid))

    def test_list_categories_searching(self) -> None:
        """Test that the `list` endpoint with search filters returns the correct paginated list of `Category`."""

        url = reverse("api:category-list")
        response = self.client.get(url, {_search_param: self.category.name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNotNone(response.data["results"][0]["uuid"])
        self.assertIsNotNone(response.data["results"][0]["name"])
        self.assertIsNotNone(response.data["results"][0]["code"])
        self.assertIsNotNone(response.data["results"][0]["description"])
        self.assertIsNotNone(response.data["results"][0]["created_at"])
        self.assertIsNotNone(response.data["results"][0]["updated_at"])
        self.assertIsNotNone(response.data["results"][0]["extras"])
        self.assertEqual(response.data["results"][0]["uuid"], str(self.category.uuid))

    def test_list_categories_ordering(self) -> None:
        """Test that the `list` endpoint with ordering filters returns the correct paginated list of `Category`."""
        url = reverse("api:category-list")
        response = self.client.get(url, {_ordering_param: "name"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNotNone(response.data["results"][0]["uuid"])
        self.assertIsNotNone(response.data["results"][0]["name"])
        self.assertIsNotNone(response.data["results"][0]["code"])
        self.assertIsNotNone(response.data["results"][0]["description"])
        self.assertIsNotNone(response.data["results"][0]["created_at"])
        self.assertIsNotNone(response.data["results"][0]["updated_at"])
        self.assertIsNotNone(response.data["results"][0]["extras"])
        self.assertEqual(response.data["results"][0]["uuid"], str(self.category.uuid))

    def test_list_categories_pagination(self) -> None:
        """Test that the `list` endpoint with pagination filters returns the correct paginated list of `Category`."""
        url = reverse("api:category-list")
        response = self.client.get(url, {"page": 1, "page_size": 10})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNotNone(response.data["results"][0]["uuid"])
        self.assertIsNotNone(response.data["results"][0]["name"])
        self.assertIsNotNone(response.data["results"][0]["code"])
        self.assertIsNotNone(response.data["results"][0]["description"])
        self.assertIsNotNone(response.data["results"][0]["created_at"])
        self.assertIsNotNone(response.data["results"][0]["updated_at"])
        self.assertIsNotNone(response.data["results"][0]["extras"])
        self.assertEqual(response.data["results"][0]["uuid"], str(self.category.uuid))

    def test_list_categories_filtering(self) -> None:
        """Test that the `list` endpoint with field filters returns the correct paginated list of `Category`."""

        url = reverse("api:category-list")
        response = self.client.get(url, {"name": self.category.name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNotNone(response.data["results"][0]["uuid"])
        self.assertIsNotNone(response.data["results"][0]["name"])
        self.assertIsNotNone(response.data["results"][0]["code"])
        self.assertIsNotNone(response.data["results"][0]["description"])
        self.assertIsNotNone(response.data["results"][0]["created_at"])
        self.assertIsNotNone(response.data["results"][0]["updated_at"])
        self.assertIsNotNone(response.data["results"][0]["extras"])
        self.assertEqual(response.data["results"][0]["uuid"], str(self.category.uuid))

    def test_retrieve_category(self) -> None:
        """Test that the `retrieve` endpoint returns the correct `Category`."""
        url = reverse("api:category-detail", kwargs={"uuid": self.category.uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["uuid"])
        self.assertIsNotNone(response.data["name"])
        self.assertIsNotNone(response.data["code"])
        self.assertIsNotNone(response.data["description"])
        self.assertIsNotNone(response.data["created_at"])
        self.assertIsNotNone(response.data["updated_at"])
        self.assertIsNotNone(response.data["extras"])
        self.assertEqual(response.data["uuid"], str(self.category.uuid))

    def test_retrieve_category_not_found(self) -> None:
        """Test that the `retrieve` endpoint returns 404 error, if `Category` does not exist."""
        url = reverse("api:category-detail", kwargs={"uuid": uuid.uuid4()})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNotNone(response.data["results"][0]["uuid"])
        self.assertIsNotNone(response.data["results"][0]["name"])
        self.assertIsNotNone(response.data["results"][0]["code"])
        self.assertIsNotNone(response.data["results"][0]["description"])
        self.assertIsNotNone(response.data["results"][0]["created_at"])
        self.assertIsNotNone(response.data["results"][0]["updated_at"])
        self.assertIsNotNone(response.data["results"][0]["extras"])
        self.assertEqual(response.data["results"][0]["uuid"], str(self.ownership.uuid))

    def test_list_ownerships_searching(self) -> None:
        """Test that the `list` endpoint with search filters returns the correct paginated list of `Ownership`."""

        url = reverse("api:ownership-list")
        response = self.client.get(url, {_search_param: self.ownership.name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNotNone(response.data["results"][0]["uuid"])
        self.assertIsNotNone(response.data["results"][0]["name"])
        self.assertIsNotNone(response.data["results"][0]["code"])
        self.assertIsNotNone(response.data["results"][0]["description"])
        self.assertIsNotNone(response.data["results"][0]["created_at"])
        self.assertIsNotNone(response.data["results"][0]["updated_at"])
        self.assertIsNotNone(response.data["results"][0]["extras"])
        self.assertEqual(response.data["results"][0]["uuid"], str(self.ownership.uuid))

    def test_list_ownerships_ordering(self) -> None:
        """Test that the `list` endpoint with ordering filters returns the correct paginated list of `Ownership`."""
        url = reverse("api:ownership-list")
        response = self.client.get(url, {_ordering_param: "name"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNotNone(response.data["results"][0]["uuid"])
        self.assertIsNotNone(response.data["results"][0]["name"])
        self.assertIsNotNone(response.data["results"][0]["code"])
        self.assertIsNotNone(response.data["results"][0]["description"])
        self.assertIsNotNone(response.data["results"][0]["created_at"])
        self.assertIsNotNone(response.data["results"][0]["updated_at"])
        self.assertIsNotNone(response.data["results"][0]["extras"])
        self.assertEqual(response.data["results"][0]["uuid"], str(self.ownership.uuid))

    def test_list_ownerships_pagination(self) -> None:
        """Test that the `list` endpoint with pagination filters returns the correct paginated list of `Ownership`."""
        url = reverse("api:ownership-list")
        response = self.client.get(url, {"page": 1, "page_size": 10})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNotNone(response.data["results"][0]["uuid"])
        self.assertIsNotNone(response.data["results"][0]["name"])
        self.assertIsNotNone(response.data["results"][0]["code"])
        self.assertIsNotNone(response.data["results"][0]["description"])
        self.assertIsNotNone(response.data["results"][0]["created_at"])
        self.assertIsNotNone(response.data["results"][0]["updated_at"])
        self.assertIsNotNone(response.data["results"][0]["extras"])
        self.assertEqual(response.data["results"][0]["uuid"], str(self.ownership.uuid))

    def test_list_ownerships_filtering(self) -> None:
        """Test that the `list` endpoint with field filters returns the correct paginated list of `Ownership`."""

        url = reverse("api:ownership-list")
        response = self.client.get(url, {"name": self.ownership.name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNotNone(response.data["results"][0]["uuid"])
        self.assertIsNotNone(response.data["results"][0]["name"])
        self.assertIsNotNone(response.data["results"][0]["code"])
        self.assertIsNotNone(response.data["results"][0]["description"])
        self.assertIsNotNone(response.data["results"][0]["created_at"])
        self.assertIsNotNone(response.data["results"][0]["updated_at"])
        self.assertIsNotNone(response.data["results"][0]["extras"])
        self.assertEqual(response.data["results"][0]["uuid"], str(self.ownership.uuid))

    def test_retrieve_ownership(self) -> None:
        """Test that the `retrieve` endpoint returns the correct `Ownership`."""
        url = reverse("api:ownership-detail", kwargs={"uuid": self.ownership.uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["uuid"])
        self.assertIsNotNone(response.data["name"])
        self.assertIsNotNone(response.data["code"])
        self.assertIsNotNone(response.data["description"])
        self.assertIsNotNone(response.data["created_at"])
        self.assertIsNotNone(response.data["updated_at"])
        self.assertIsNotNone(response.data["extras"])
        self.assertEqual(response.data["uuid"], str(self.ownership.uuid))

    def test_retrieve_ownership_not_found(self) -> None:
        """Test that the `retrieve` endpoint returns 404 error, if `Ownership` does not exist."""
        url = reverse("api:category-detail", kwargs={"uuid": uuid.uuid4()})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
