import time

from django.apps import apps

from celery import shared_task

__all__ = ["generate_layer_tiff_tiles"]


@shared_task()
def generate_layer_tiff_tiles(pk):
    """Generate tiles of Layer's GeoTIFF file."""
    start_time = time.perf_counter()

    Layer = apps.get_registered_model("catalog", "Layer")
    layer = Layer.objects.get(pk=pk)
    layer.generate_tiles()

    end_time = time.perf_counter()

    return {
        "execution_time": end_time - start_time,
        "tiff": str(layer.tiff),
        "tiles_root": str(layer.tiles_dir),
    }
