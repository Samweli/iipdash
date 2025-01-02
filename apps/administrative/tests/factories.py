import typing

from django.contrib.gis import geos

import factory
import factory.fuzzy
from django_countries import countries

from ..models import Area


class AreaFactory(factory.django.DjangoModelFactory):
    type_code = factory.Iterator(["ADM0", "ADM1"], cycle=True)
    country = factory.Iterator([code for code, name in countries], cycle=True)
    name = factory.Faker("city")
    code = factory.Faker("postcode")
    description = factory.Faker("text", max_nb_chars=200)

    @factory.lazy_attribute
    def full_name(self) -> str:
        return f"{self.name} ({self.type_code})"

    population = factory.fuzzy.FuzzyInteger(1_000, 1_000_000)

    @factory.lazy_attribute
    def population_male(self) -> int:
        return int(self.population * 0.5)

    @factory.lazy_attribute
    def population_female(self) -> int:
        return int(self.population - self.population_male)

    population_year = factory.fuzzy.FuzzyInteger(2000, 2023)

    @factory.lazy_attribute
    def geometry(self) -> geos.MultiPolygon:
        return geos.MultiPolygon(geos.Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))))

    area = factory.fuzzy.FuzzyFloat(100.0, 100_000.0)
    extras = factory.Faker("pydict", value_types=[str, int, bool])

    class Meta:
        model: typing.Type[Area] = Area
