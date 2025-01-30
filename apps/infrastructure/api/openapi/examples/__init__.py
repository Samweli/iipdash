from typing import List

from drf_spectacular.utils import OpenApiExample

from .cell_tower import cell_tower_list_response_only, cell_tower_retrieve_response_only
from .fiber_optic import fiber_optic_list_response_only, fiber_optic_retrieve_response_only

cell_tower_list_examples: List[OpenApiExample] = [cell_tower_list_response_only]
cell_tower_retrieve_examples: List[OpenApiExample] = [cell_tower_retrieve_response_only]

fiber_optic_list_examples: List[OpenApiExample] = [fiber_optic_list_response_only]
fiber_optic_retrieve_examples: List[OpenApiExample] = [fiber_optic_retrieve_response_only]
