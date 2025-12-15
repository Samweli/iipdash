"""
User admin configuration.

This module defines the admin interface for the custom :class:`users.models.User`
model by extending Django's built-in :class:`django.contrib.auth.admin.UserAdmin`.

References:
    - :class:`django.contrib.admin.ModelAdmin`
    - :class:`django.contrib.auth.admin.UserAdmin`
    - :class:`users.models.User`
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as CoreUserAdmin

from .forms import AdminUserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(CoreUserAdmin):
    """
    Admin interface configuration for the :class:`users.models.User` model.

    This class extends :class:`django.contrib.auth.admin.UserAdmin` to provide
    additional customization for the user management interface in the Django admin panel.
    """

    #: A list of fields in the admin's list view that link to the detailed
    #: user editing page.
    list_display_links: list[str] = ["username", "email"]

    #: A list of fields that are displayed as read-only in the admin interface.
    readonly_fields: list[str] = ["uuid"]

    #: A tuple that defines the layout of the user editing form. It extends
    #: the default `fieldsets` from
    #: :class:`django.contrib.auth.admin.UserAdmin` to include an additional
    #: section for the `uuid` field.
    fieldsets: tuple = CoreUserAdmin.fieldsets + (("Additional info", {"fields": ["uuid"]}),)

    add_form = AdminUserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
