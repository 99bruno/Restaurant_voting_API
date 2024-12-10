from core.models import User
from core.serializers import UserSerializer
from django.test import TestCase


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
        }

    def test_valid_user_creation(self):
        """Test that a user is successfully created with valid data."""
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, self.valid_data["username"])
        self.assertEqual(user.email, self.valid_data["email"])
        self.assertTrue(user.check_password(self.valid_data["password"]))

    def test_missing_required_fields(self):
        """Test that missing required fields raise validation errors."""
        invalid_data = {"username": "testuser"}  # No email or password
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertIn("password", serializer.errors)

    def test_duplicate_email(self):
        """Test that a duplicate email raises a validation error."""
        User.objects.create_user(**self.valid_data)
        serializer = UserSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertEqual(
            str(serializer.errors["email"][0]), "A user with this email already exists."
        )

    def test_unexpected_fields(self):
        """Test that unexpected fields raise validation errors."""
        invalid_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "extra_field": "unexpected_value",
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertIn(
            "Unexpected fields: extra_field",
            str(serializer.errors["non_field_errors"][0]),
        )
