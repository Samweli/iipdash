from typing import List

from drf_spectacular.utils import OpenApiExample

from .category import category_list_response_only, category_retrieve_response_only
from .ownership import ownership_list_response_only, ownership_retrieve_response_only

category_list_examples: List[OpenApiExample] = [category_list_response_only]
category_retrieve_examples: List[OpenApiExample] = [category_retrieve_response_only]

ownership_list_examples: List[OpenApiExample] = [ownership_list_response_only]
ownership_retrieve_examples: List[OpenApiExample] = [ownership_retrieve_response_only]
