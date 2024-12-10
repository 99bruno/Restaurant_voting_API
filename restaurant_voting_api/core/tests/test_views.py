from rest_framework.test import APITestCase
from rest_framework import status
from core.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationViewTests(APITestCase):
    def setUp(self):
        self.valid_user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123"
        }
        self.invalid_user_data = {
            "username": "",
            "email": "invalidemail",
            "password": "short"
        }

    def test_user_registration_success(self):
        """Test successful user registration."""
        response = self.client.post('/authentication/register/', self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertEqual(response.data['username'], self.valid_user_data['username'])

    def test_user_registration_failure(self):
        """Test user registration with invalid data."""
        response = self.client.post('/authentication/register/', self.invalid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_sample_data_get(self):
        """Test retrieving sample data for registration."""
        response = self.client.get('/authentication/register/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SuperUserRegistrationViewTests(APITestCase):
    def setUp(self):
        # Create a regular user
        self.user = User.objects.create_user(username="regularuser", password="password")
        # Create a superuser
        self.superuser = User.objects.create_superuser(username="adminuser", password="password")
        self.valid_superuser_data = {
            "username": "superuser",
            "email": "superuser@example.com",
            "password": "supersecurepassword123"
        }

    def test_superuser_registration_success(self):
        """
        Test successful superuser registration.
        """
        admin_user = User.objects.create_user(username='admin', password='adminpassword', is_admin=True)
        self.client.force_authenticate(user=admin_user)

        response = self.client.post('/authentication/register/admin/', self.valid_superuser_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_registration_permission_denied(self):
        """Test superuser registration without sufficient permissions."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/authentication/register_admin/', self.valid_superuser_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_superuser_registration_unauthenticated(self):
        """Test superuser registration without authentication."""
        response = self.client.post('/authentication/register_admin/', self.valid_superuser_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
