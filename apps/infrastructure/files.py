def mobile_coverage_tiff_path(instance, filename):
    """Returns path for storing mobile coverage tiff files, i.e.
    "infrastructure/mobile-coverage/{instance.uuid}/tiff/{filename}"
    """
    return f"infrastructure/mobile-coverage/{instance.uuid}/tiff/{filename}"
