def hazard_exposure_tiff_path(instance, filename):
    """Returns path for storing hazard exposure tiff files, i.e.
    "hazards/hazard-exposure/{instance.uuid}/tiff/{filename}"
    """
    return f"hazards/hazard-exposure/{instance.uuid}/tiff/{filename}"
