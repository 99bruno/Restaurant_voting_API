from core.models import User
from django.test import TestCase


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123", is_admin=False
        )
        self.admin_user = User.objects.create_user(
            username="adminuser", password="password123", is_admin=True
        )

    def test_user_creation(self):
        """Test that a user is created successfully."""
        self.assertEqual(self.user.username, "testuser")
        self.assertFalse(self.user.is_admin)

    def test_admin_user_creation(self):
        """Test that an admin user is created successfully."""
        self.assertEqual(self.admin_user.username, "adminuser")
        self.assertTrue(self.admin_user.is_admin)

    def test_str_method(self):
        """Test the __str__ method of the User model."""
        self.assertEqual(str(self.user), "testuser")
        self.assertEqual(str(self.admin_user), "adminuser")
