"""
Custom User model for Authentication.

This module defines a custom `User` model by extending Django's built-in
:class:`django.contrib.auth.models.AbstractUser`.

References:
    - :class:`django.contrib.auth.models.AbstractUser`
    - :class:`django.db.models.Model`

See Also:
    https://docs.djangoproject.com/en/stable/ref/contrib/auth/

"""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model extending Django's :class:`django.contrib.auth.models.AbstractUser`.

    Attributes:
        id (:class:`django.db.models.BigAutoField`):
            A database primary key for the user. Inherited from
            :class:`django.db.models.Model`.

        uuid (:class:`django.db.models.UUIDField`):
            A universally unique identifier (UUID) for the user, generated using
            :func:`uuid.uuid4`. This field is non-editable, unique, and set by default.

        username (:class:`django.db.models.CharField`):
            A unique username of the user. Inherited from
            :class:`django.contrib.auth.models.AbstractUser`.

        email (:class:`django.db.models.EmailField`):
            A unique email address of the user. Inherited from
            :class:`django.contrib.auth.models.AbstractUser`.

        password (:class:`django.db.models.CharField`):
            A hashed password of the user. Inherited from
            :class:`django.contrib.auth.models.AbstractUser`.

        first_name (:class:`django.db.models.CharField`):
            A first name of the user. Inherited from
            :class:`django.contrib.auth.models.AbstractUser`.

        last_name (:class:`django.db.models.CharField`):
            A last name of the user. Inherited from
            :class:`django.contrib.auth.models.AbstractUser`.

        is_superuser (:class:`django.db.models.BooleanField`):
            Indicates whether the user has superuser privileges. Inherited from
            :class:`django.contrib.auth.models.AbstractUser`.

        is_staff (:class:`django.db.models.BooleanField`):
            Indicates whether the user can log in to the admin interface. Inherited
            from :class:`django.contrib.auth.models.AbstractUser`.

        is_active (:class:`django.db.models.BooleanField`):
            Indicates whether the user account is active. Inherited from
            :class:`django.contrib.auth.models.AbstractUser`.

        last_login (:class:`django.db.models.DateTimeField`):
            The last time the user logged in. Inherited from
            :class:`django.contrib.auth.models.AbstractUser`.

        date_joined (:class:`django.db.models.DateTimeField`):
            The date and time when the user account was created. Inherited from
            :class:`django.contrib.auth.models.AbstractUser`.

        groups (:class:`django.db.models.ManyToManyField`):
            The groups the user belongs to. A Many-to-many relationship to
            :class:`django.contrib.auth.models.Group`. Inherited from
            :class:`django.contrib.auth.models.AbstractUser`.

        user_permissions (:class:`django.db.models.ManyToManyField`):
            The permissions the user has. A Many-to-many relationship to
            :class:`django.contrib.auth.models.Permission`. Inherited from
            :class:`django.contrib.auth.models.AbstractUser`.

        logentry_set:
            A reverse relationship to :class:`django.contrib.admin.models.LogEntry`
            representing logs associated with the user.
    """

    #: A universally unique identifier (UUID) for the user.
    uuid = models.UUIDField(
        _("UUID"),
        editable=False,
        unique=True,
        default=uuid.uuid4,
    )

    @cached_property
    def display_name(self):
        """
        A user-friendly display name for the user.

        The display name is determined based on the following priorities:
          1. `first_name`: If set, the first name is used.
          2. `email`: If `first_name` is not set, the email is used.
          3. `username`: If neither `first_name` nor `email` is set, the username is used.

        Returns:
            str:
                A user-friendly display name.
        """
        if self.first_name:
            return self.first_name
        elif self.email:
            return self.email
        else:
            return self.username
