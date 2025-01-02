from django.contrib.gis import geos
from django.test import TestCase

from ..models import Area
from .factories import AreaFactory


class AreaModelTestCase(TestCase):
    """Test suite for the Area model."""

    def test_area_creation(self) -> None:
        """Test that an Area instance can be created and has valid attributes."""
        area: Area = AreaFactory.create(depth=1)

        self.assertIsInstance(area, Area)
        self.assertEqual(Area.objects.count(), 1)

        self.assertIsNotNone(area.id)
        self.assertIsNotNone(area.uuid)
        self.assertIsNotNone(area.type_code)
        self.assertIsNotNone(area.country)
        self.assertIsNotNone(area.name)
        self.assertIsNotNone(area.code)
        self.assertIsNotNone(area.description)
        self.assertIsNotNone(area.full_name)
        self.assertIsNotNone(area.population)
        self.assertIsNotNone(area.population_male)
        self.assertIsNotNone(area.population_female)
        self.assertIsNotNone(area.population_year)
        self.assertIsNotNone(area.geometry)
        self.assertIsNotNone(area.area)
        self.assertIsNotNone(area.created_at)
        self.assertIsNotNone(area.updated_at)
        self.assertIsNotNone(area.extras)
        self.assertEqual(str(area), area.name)

    def test_geometry_auto_conversion(self):
        """Test save method converts a Polygon to MultiPolygon."""
        area: Area = AreaFactory.create(depth=1)

        with self.assertRaises(TypeError):
            area.geometry = geos.Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0)))
            area.save()

        self.assertIsInstance(area.geometry, geos.MultiPolygon)
        self.assertEqual(len(area.geometry), 1)

    def test_invalid_geometry(self):
        """Test that invalid geometry raises a validation error."""
        with self.assertRaises(ValueError):
            AreaFactory.create(depth=1, geometry="Invalid Geometry")
