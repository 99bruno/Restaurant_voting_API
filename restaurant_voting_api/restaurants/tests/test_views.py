from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant, Menu
from rest_framework.exceptions import NotFound


class RestaurantViewTests(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            password='password'
        )
        self.normal_user = get_user_model().objects.create_user(
            username='user',
            password='password'
        )

    def test_create_restaurant_as_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)
        data = {'name': 'Test Restaurant', 'owner_id': self.normal_user.id}
        response = self.client.post('/restaurants/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_restaurants(self):
        self.client.force_authenticate(user=self.admin_user)
        Restaurant.objects.create(name='Test Restaurant', owner_id=self.admin_user)
        response = self.client.get('/restaurants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_restaurant_with_invalid_data(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': '', 'owner_id': self.admin_user.id}
        response = self.client.post('/restaurants/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MenuViewTests(APITestCase):
    def setUp(self):
        # Створюємо користувача-адміністратора, користувача та ресторан
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            password='password'
        )
        self.normal_user = get_user_model().objects.create_user(
            username='user',
            password='password'
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            owner_id=self.admin_user
        )

    def test_create_menu_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'restaurant': self.restaurant.id, 'date': '2024-12-10', 'items': []}
        response = self.client.post(f'/restaurants/{self.restaurant.id}/menu/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_menu_as_owner(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'restaurant': self.restaurant.id, 'date': '2024-12-10', 'items': []}
        response = self.client.post(f'/restaurants/{self.restaurant.id}/menu/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_menu_as_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)
        data = {'restaurant': self.restaurant.id, 'date': '2024-12-10', 'items': []}
        response = self.client.post(f'/restaurants/{self.restaurant.id}/menu/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_menu_for_restaurant(self):
        self.client.force_authenticate(user=self.admin_user)
        menu = Menu.objects.create(restaurant=self.restaurant, date='2024-12-10')
        response = self.client.get(f'/restaurants/{self.restaurant.id}/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_menu_for_nonexistent_restaurant(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'restaurant': 9999, 'date': '2024-12-10', 'items': []}
        response = self.client.post(f'/restaurants/9999/menu/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
