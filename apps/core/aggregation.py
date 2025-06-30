from django.contrib.gis.db.models import PolygonField
from django.db.models import Aggregate, FloatField, Func


class Median(Aggregate):
    function = "PERCENTILE_CONT"
    name = "median"
    output_field = FloatField()
    template = "%(function)s(0.5) WITHIN GROUP (ORDER BY %(expressions)s)"


class StBuffer(Func):
    function = "ST_Buffer"
    output_field = PolygonField()
