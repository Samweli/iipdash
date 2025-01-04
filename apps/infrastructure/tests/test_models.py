from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import CellTower, OpticalFibre
from .factories import CellTowerFactory, OpticalFibreFactory


class OpticalFibreModelTestCase(TestCase):
    """Test suite for the OpticalFibre model."""

    def test_optical_fibre_creation(self) -> None:
        """Test that a OpticalFibre instance can be created and has valid attributes."""
        optical_fibre: OpticalFibre = OpticalFibreFactory.create()

        self.assertIsInstance(optical_fibre, OpticalFibre)
        self.assertEqual(OpticalFibre.objects.count(), 1)

        self.assertIsNotNone(optical_fibre.id)
        self.assertIsNotNone(optical_fibre.uuid)
        self.assertIsNotNone(optical_fibre.country)
        self.assertIsNotNone(optical_fibre.name)
        self.assertIsNotNone(optical_fibre.description)
        self.assertIsNotNone(optical_fibre.geometry)
        self.assertIsNotNone(optical_fibre.created_at)
        self.assertIsNotNone(optical_fibre.updated_at)
        self.assertIsNotNone(optical_fibre.extras)
        self.assertEqual(str(optical_fibre), optical_fibre.name)

    def test_invalid_geometry_raises_error(self) -> None:
        """Test that invalid geometry raises a validation error."""
        with self.assertRaises(ValueError):
            OpticalFibreFactory.create(geometry="Invalid Geometry")


class CellTowerModelTestCase(TestCase):
    """Test suite for the CellTower model."""

    def test_cell_tower_creation(self) -> None:
        """Test that a CellTower instance can be created and has valid attributes."""
        cell_tower: CellTower = CellTowerFactory.create()

        self.assertIsInstance(cell_tower, CellTower)
        self.assertEqual(CellTower.objects.count(), 1)

        self.assertIsNotNone(cell_tower.id)
        self.assertIsNotNone(cell_tower.uuid)
        self.assertIsNotNone(cell_tower.network_type)
        self.assertIsNotNone(cell_tower.mcc)
        self.assertIsNotNone(cell_tower.geometry)
        self.assertIsNotNone(cell_tower.location_is_approximate)
        self.assertIsNotNone(cell_tower.range)
        self.assertIsNotNone(cell_tower.administrative_area)
        self.assertIsNotNone(cell_tower.src_created)
        self.assertIsNotNone(cell_tower.src_updated_at)
        self.assertIsNotNone(cell_tower.created_at)
        self.assertIsNotNone(cell_tower.updated_at)
        self.assertIsNotNone(cell_tower.extras)
        self.assertIsNotNone(cell_tower.display_name)
        self.assertEqual(cell_tower.__str__(), cell_tower.display_name)

    def test_cell_tower_creation_with_null_foreign_keys(self) -> None:
        """Test cell_tower creation with null administrative area."""
        cell_tower: CellTower = CellTowerFactory.create(administrative_area=None)
        self.assertIsNone(cell_tower.administrative_area)

    def test_invalid_geometry_raises_error(self) -> None:
        """Test that invalid geometry raises a `ValueError`."""
        with self.assertRaises(ValueError):
            CellTowerFactory.create(geometry="Invalid Geometry")

    def test_negative_range_raises_error(self):
        """Test that a negative range value raises a `ValidationError`."""
        with self.assertRaises(ValidationError):
            cell_tower: CellTower = CellTowerFactory.create(range=-100)
            cell_tower.full_clean()
