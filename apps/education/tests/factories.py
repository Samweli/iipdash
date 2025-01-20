import typing

from django.contrib.gis import geos

import factory
import factory.fuzzy
from django_countries import countries
from faker import Faker

from administrative.models import Area
from administrative.tests.factories import AreaFactory

from ..models import Category, Institution, Ownership

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    name: str = factory.Iterator(
        [
            "university",
            "college",
            "kindergarten",
            "school",
            "other",
        ],
        cycle=True,
    )
    description: str = factory.Faker("text", max_nb_chars=200)
    extras: typing.Dict[str, typing.Any] = factory.Faker("pydict", value_types=[str, int, bool])

    class Meta:
        model: typing.Type[Category] = Category
        django_get_or_create: typing.Tuple[str, ...] = ("name",)


class OwnershipFactory(factory.django.DjangoModelFactory):
    name: str = factory.Iterator(
        [
            "public",
            "private",
            "government",
            "religious",
            "private_non_profit",
            "community",
            "ngo",
            "other",
        ],
        cycle=True,
    )
    description: str = factory.Faker("text", max_nb_chars=200)
    extras: typing.Dict[str, typing.Any] = factory.Faker("pydict", value_types=[str, int, bool])

    class Meta:
        model: typing.Type[Ownership] = Ownership
        django_get_or_create: typing.Tuple[str, ...] = ("name",)


class InstitutionFactory(factory.django.DjangoModelFactory):
    category: Category = factory.SubFactory(CategoryFactory)
    name: str = factory.Faker("company")
    ownership: Ownership = factory.SubFactory(OwnershipFactory)
    description: str = factory.Faker("text", max_nb_chars=200)
    code: str = factory.Faker("postcode")
    postal_code: str = factory.Faker("postcode")
    address: str = factory.Faker("address")
    phone: str = factory.Faker("phone_number")
    fax: str = factory.Faker("phone_number")
    email: str = factory.Faker("email")
    website: str = factory.Faker("url")

    @factory.lazy_attribute
    def geometry(self) -> geos.Point:
        country_code: typing.Optional[str] = fake.random_element([code for code, name in countries])
        if self.administrative_area and self.administrative_area.country:
            if self.administrative_area.country.code:
                country_code = self.administrative_area.country.code

        latlong: typing.Tuple[str, ...] = fake.local_latlng(country_code=country_code)
        if not latlong:
            latlong = fake.local_latlng()

        return geos.Point(float(latlong[1]), float(latlong[0]))

    administrative_area: Area = factory.SubFactory(AreaFactory, depth=1)
    has_electricity: bool = factory.Faker("boolean")
    has_fiber_optic: bool = factory.Faker("boolean")
    fon_distance: float = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    osm_id: int = factory.Faker("random_number", digits=10)
    osm_type: str = factory.Iterator(["nodes"], cycle=True)
    extras: typing.Dict[str, typing.Any] = factory.Faker("pydict", value_types=[str, int, bool])

    class Meta:
        model: typing.Type[Institution] = Institution
        django_get_or_create: typing.Tuple[str, ...] = ("code",)
