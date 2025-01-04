from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import CellTower, FiberOptic
from .factories import CellTowerFactory, FiberOpticFactory


class FiberOpticModelTestCase(TestCase):
    """Test suite for the FiberOptic model."""

    def test_fiber_optic_creation(self) -> None:
        """Test that a FiberOptic instance can be created and has valid attributes."""
        fiber_optic: FiberOptic = FiberOpticFactory.create()

        self.assertIsInstance(fiber_optic, FiberOptic)
        self.assertEqual(FiberOptic.objects.count(), 1)

        self.assertIsNotNone(fiber_optic.id)
        self.assertIsNotNone(fiber_optic.uuid)
        self.assertIsNotNone(fiber_optic.country)
        self.assertIsNotNone(fiber_optic.name)
        self.assertIsNotNone(fiber_optic.description)
        self.assertIsNotNone(fiber_optic.geometry)
        self.assertIsNotNone(fiber_optic.created_at)
        self.assertIsNotNone(fiber_optic.updated_at)
        self.assertIsNotNone(fiber_optic.extras)
        self.assertEqual(str(fiber_optic), fiber_optic.name)

    def test_invalid_geometry_raises_error(self) -> None:
        """Test that invalid geometry raises a validation error."""
        with self.assertRaises(ValueError):
            FiberOpticFactory.create(geometry="Invalid Geometry")


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
