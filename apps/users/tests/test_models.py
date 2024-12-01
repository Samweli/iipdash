from django.test import TestCase

from ..models import User
from .factories import UserFactory


class UserModelTestCase(TestCase):

    def test_user_creation(self) -> None:
        """Test that a User instance can be created and and has valid attributes."""
        user: User = UserFactory.create()

        self.assertIsInstance(user, User)
        self.assertEqual(User.objects.count(), 1)

        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.uuid)
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.email)
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.first_name)
        self.assertIsNotNone(user.last_name)
        self.assertIsNotNone(user.is_superuser)
        self.assertIsNotNone(user.is_staff)
        self.assertIsNotNone(user.is_active)
        self.assertIsNotNone(user.date_joined)
        self.assertIsNone(user.last_login)
        self.assertEqual(user.display_name, user.first_name)

    def test_user_display_name(self):
        """Test the display name of the User instance."""
        user: User = UserFactory.build()
        self.assertIsNotNone(user.first_name)
        self.assertEqual(user.display_name, user.first_name)

        user: User = UserFactory.build(first_name=None)
        self.assertIsNone(user.first_name)
        self.assertIsNotNone(user.email)
        self.assertEqual(user.display_name, user.email)

        user: User = UserFactory.build(first_name=None, email=None)
        self.assertIsNone(user.first_name)
        self.assertIsNone(user.email)
        self.assertIsNotNone(user.username)
        self.assertEqual(user.display_name, user.username)
