import uuid

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .factories import CategoryFactory


class CategoryAPITestCase(TestCase):
    """Test suite for the CategoryViewSet."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = APIClient()
        self.category = CategoryFactory.create()

    def test_list_categories(self) -> None:
        """Test that the `list` endpoint returns the correct list of `Category`."""
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]["uuid"])
        self.assertIsNotNone(response.data[0]["name"])
        self.assertIsNotNone(response.data[0]["code"])
        self.assertIsNotNone(response.data[0]["description"])
        self.assertIsNotNone(response.data[0]["created_at"])
        self.assertIsNotNone(response.data[0]["updated_at"])
        self.assertIsNotNone(response.data[0]["extras"])
        self.assertEqual(response.data[0]["uuid"], str(self.category.uuid))

    def test_list_categories_searching(self) -> None:
        """Test that the `list` endpoint with search filters returns the correct list of `Category`."""
        response = self.client.get("/api/categories/", {"search": self.category.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]["uuid"])
        self.assertIsNotNone(response.data[0]["name"])
        self.assertIsNotNone(response.data[0]["code"])
        self.assertIsNotNone(response.data[0]["description"])
        self.assertIsNotNone(response.data[0]["created_at"])
        self.assertIsNotNone(response.data[0]["updated_at"])
        self.assertIsNotNone(response.data[0]["extras"])
        self.assertEqual(response.data[0]["uuid"], str(self.category.uuid))

    def test_list_categories_ordering(self) -> None:
        """Test that the `list` endpoint with ordering filters returns the correct list of `Category`."""
        response = self.client.get("/api/categories/", {"ordering": "name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]["uuid"])
        self.assertIsNotNone(response.data[0]["name"])
        self.assertIsNotNone(response.data[0]["code"])
        self.assertIsNotNone(response.data[0]["description"])
        self.assertIsNotNone(response.data[0]["created_at"])
        self.assertIsNotNone(response.data[0]["updated_at"])
        self.assertIsNotNone(response.data[0]["extras"])
        self.assertEqual(response.data[0]["uuid"], str(self.category.uuid))

    def test_retrieve_category(self) -> None:
        """Test that the `retrieve` endpoint returns the correct `Category`."""
        response = self.client.get(f"/api/categories/{self.category.uuid}/")
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
        response = self.client.get(f"/api/categories/{uuid.uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
