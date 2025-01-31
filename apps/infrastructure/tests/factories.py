import datetime
import typing

from django.contrib.gis import geos

import factory
import factory.fuzzy
from django_countries import countries
from faker import Faker

from administrative.models import Area
from administrative.tests.factories import AreaFactory

from ..models import CellTower, FiberOptic

fake = Faker()


class FiberOpticFactory(factory.django.DjangoModelFactory):
    name: str = factory.Faker("company")
    description: str = factory.Faker("text", max_nb_chars=200)

    @factory.lazy_attribute
    def geometry(self) -> geos.MultiLineString:
        return geos.MultiLineString(
            [
                geos.LineString([(0.0, 0.0), (1.0, 1.0)]),
                geos.LineString([(2.0, 2.0), (3.0, 3.0)]),
            ]
        )

    extras: typing.Dict[str, typing.Any] = factory.Faker("pydict", value_types=[str, int, bool])

    class Meta:
        model: typing.Type[FiberOptic] = FiberOptic


class CellTowerFactory(factory.django.DjangoModelFactory):
    network_type: str = factory.Iterator(["GSM", "UMTS", "LTE", "CDMA"], cycle=True)
    mcc: int = factory.Faker("random_int", min=200, max=999)

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

    location_is_approximate: bool = factory.Faker("boolean")
    range: float = factory.Faker("pyfloat", left_digits=3, right_digits=2, positive=True)
    administrative_area: Area = factory.SubFactory(AreaFactory, depth=1)
    src_created_at: datetime.datetime = factory.Faker("date_time_this_month", tzinfo=datetime.timezone.utc)
    src_updated_at: datetime.datetime = factory.Faker("date_time_this_month", tzinfo=datetime.timezone.utc)
    extras: typing.Dict[str, typing.Any] = factory.Faker("pydict", value_types=[str, int, bool])

    class Meta:
        model: typing.Type[CellTower] = CellTower
