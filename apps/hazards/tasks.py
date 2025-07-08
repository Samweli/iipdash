import time

from django.apps import apps
from django.utils.timezone import now

from celery import shared_task

__all__ = ["update_hazards_exposure_coverage_raster", "generate_hazards_exposure_coverage_tiles"]


@shared_task()
def update_hazards_exposure_coverage_raster(pk):
    """Update hazards exposure coverage raster data saved in the database based on it's GeoTIFF file."""
    start_time = time.perf_counter()

    ExposureCoverage = apps.get_registered_model("hazards", "ExposureCoverage")
    coverage = ExposureCoverage.objects.get(pk=pk)
    coverage.set_raster()
    ExposureCoverage.objects.filter(pk=pk).update(raster=coverage.raster, updated_at=now())

    end_time = time.perf_counter()

    return {
        "execution_time": end_time - start_time,
        "tiff": str(coverage.tiff),
    }


@shared_task()
def generate_hazards_exposure_coverage_tiles(pk):
    """Generate hazards exposure coverage tiles based on it's GeoTIFF file."""
    start_time = time.perf_counter()

    ExposureCoverage = apps.get_registered_model("hazards", "ExposureCoverage")
    coverage = ExposureCoverage.objects.get(pk=pk)
    coverage.generate_tiles()

    end_time = time.perf_counter()

    return {
        "execution_time": end_time - start_time,
        "tiff": str(coverage.tiff),
        "tiles_root": str(coverage.tiles_dir),
    }
