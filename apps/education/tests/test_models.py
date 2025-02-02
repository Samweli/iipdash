from django.template.defaultfilters import slugify
from django.test import TestCase

from faker import Faker

from ..models import Category, Institution, Ownership
from .factories import CategoryFactory, InstitutionFactory, OwnershipFactory

fake = Faker()


class CategoryModelTestCase(TestCase):
    """Test suite for the Category model."""

    def test_category_creation(self) -> None:
        """Test that a Category instance can be created and has valid attributes."""
        category: Category = CategoryFactory.create()

        self.assertIsInstance(category, Category)
        self.assertEqual(Category.objects.count(), 1)

        self.assertIsNotNone(category.id)
        self.assertIsNotNone(category.uuid)
        self.assertIsNotNone(category.name)
        self.assertIsNotNone(category.code)
        self.assertIsNotNone(category.description)
        self.assertIsNotNone(category.created_at)
        self.assertIsNotNone(category.updated_at)
        self.assertIsNotNone(category.extras)
        self.assertEqual(str(category), category.name)

    def test_generate_code_on_save(self) -> None:
        """Test that code is auto-generated when not provided."""
        category: Category = CategoryFactory.create(code=None)
        self.assertIsNotNone(category.code)
        self.assertEqual(category.code, slugify(category.name[:50]))

    def test_no_generate_code_on_save(self) -> None:
        """Test that code is not auto-generated when provided."""
        code: str = fake.postcode()
        category: Category = CategoryFactory.create(code=code)
        self.assertIsNotNone(category.code)
        self.assertEqual(category.code, code)


class OwnershipModelTestCase(TestCase):
    """Test suite for the Ownership model."""

    def test_ownership_creation(self) -> None:
        """Test that an Ownership instance can be created and has valid attributes."""
        ownership: Ownership = OwnershipFactory.create()

        self.assertIsInstance(ownership, Ownership)
        self.assertEqual(Ownership.objects.count(), 1)

        self.assertIsNotNone(ownership.id)
        self.assertIsNotNone(ownership.uuid)
        self.assertIsNotNone(ownership.name)
        self.assertIsNotNone(ownership.code)
        self.assertIsNotNone(ownership.description)
        self.assertIsNotNone(ownership.created_at)
        self.assertIsNotNone(ownership.updated_at)
        self.assertIsNotNone(ownership.extras)
        self.assertEqual(str(ownership), ownership.name)

    def test_generate_code_on_save(self) -> None:
        """Test that code is auto-generated when not provided."""
        ownership: Ownership = OwnershipFactory.create(code=None)
        self.assertIsNotNone(ownership.code)
        self.assertEqual(ownership.code, slugify(ownership.name[:50]))

    def test_no_generate_code_on_save(self) -> None:
        """Test that code is not auto-generated when provided."""
        code: str = fake.postcode()
        ownership: Ownership = OwnershipFactory.create(code=code)
        self.assertIsNotNone(ownership.code)
        self.assertEqual(ownership.code, code)


class InstitutionModelTestCase(TestCase):
    """Test suite for the Institution model."""

    def test_institution_creation(self) -> None:
        """Test that an Institution instance can be created and has valid attributes."""
        institution: Institution = InstitutionFactory.create()

        self.assertIsInstance(institution, Institution)
        self.assertEqual(Institution.objects.count(), 1)

        self.assertIsNotNone(institution.id)
        self.assertIsNotNone(institution.uuid)
        self.assertIsNotNone(institution.category)
        self.assertIsNotNone(institution.name)
        self.assertIsNotNone(institution.ownership)
        self.assertIsNotNone(institution.description)
        self.assertIsNotNone(institution.code)
        self.assertIsNotNone(institution.postal_code)
        self.assertIsNotNone(institution.address)
        self.assertIsNotNone(institution.phone)
        self.assertIsNotNone(institution.fax)
        self.assertIsNotNone(institution.email)
        self.assertIsNotNone(institution.website)
        self.assertIsNotNone(institution.geometry)
        self.assertIsNotNone(institution.administrative_area)
        self.assertIsNotNone(institution.has_electricity)
        self.assertIsNotNone(institution.has_fiber_optic)
        self.assertIsNotNone(institution.osm_id)
        self.assertIsNotNone(institution.osm_type)
        self.assertIsNotNone(institution.created_at)
        self.assertIsNotNone(institution.updated_at)
        self.assertIsNotNone(institution.extras)
        self.assertIsNotNone(institution.related_areas)
        self.assertEqual(str(institution), institution.name)

    def test_institution_with_null_foreign_keys(self) -> None:
        """Test institution with null category, ownership, and administrative area."""
        institution: Institution = InstitutionFactory.create(
            category=None,
            ownership=None,
            administrative_area=None,
        )
        self.assertIsNone(institution.category)
        self.assertIsNone(institution.ownership)
        self.assertIsNone(institution.administrative_area)

    def test_invalid_geometry_raises_error(self) -> None:
        """Test that invalid geometry raises a `ValueError`."""
        with self.assertRaises(ValueError):
            InstitutionFactory.create(geometry="Invalid Geometry")
