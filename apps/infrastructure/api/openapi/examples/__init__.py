from typing import List

from drf_spectacular.utils import OpenApiExample

from .celltower import celltower_list_response_only, celltower_retrieve_response_only
from .fiberoptic import fiberoptic_list_response_only, fiberoptic_retrieve_response_only

celltower_list_examples: List[OpenApiExample] = [celltower_list_response_only]
celltower_retrieve_examples: List[OpenApiExample] = [celltower_retrieve_response_only]

fiberoptic_list_examples: List[OpenApiExample] = [fiberoptic_list_response_only]
fiberoptic_retrieve_examples: List[OpenApiExample] = [fiberoptic_retrieve_response_only]
