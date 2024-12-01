import typing

import factory

from ..models import User


class UserFactory(factory.django.DjangoModelFactory):
    username: str = factory.Faker("user_name")
    email: str = factory.Faker("email")
    first_name: str = factory.Faker("first_name")
    last_name: str = factory.Faker("last_name")
    password: str = factory.django.Password("#Passw0rD@t3sT")

    class Meta:
        model: typing.Type[User] = User
        django_get_or_create: typing.Tuple[str, ...] = ("username", )
