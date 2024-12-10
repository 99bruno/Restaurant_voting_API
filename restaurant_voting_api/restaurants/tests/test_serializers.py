from core.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from restaurants.models import Menu, Restaurant
from restaurants.serializers import ItemSerializer, MenuSerializer, RestaurantSerializer


class RestaurantSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.valid_data = {
            "name": "Test Restaurant",
            "owner_id": self.user.id,
        }
        self.invalid_data = {
            "name": "Test Restaurant",
            "owner_id": self.user.id,
            "extra_field": "unexpected",  # Adding an unexpected field
        }

    def test_valid_restaurant_serializer(self):
        """Test valid data serialization for Restaurant"""
        serializer = RestaurantSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        restaurant = serializer.save()
        self.assertEqual(restaurant.name, self.valid_data["name"])
        self.assertEqual(restaurant.owner_id.id, self.valid_data["owner_id"])

    def test_invalid_restaurant_serializer(self):
        """Test invalid data serialization with unexpected field"""
        serializer = RestaurantSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class MenuSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant", owner_id=self.user
        )
        self.valid_menu_data = {
            "restaurant": self.restaurant.id,
            "date": "2024-12-10",
            "items": [
                {"name": "Item 1", "price": 9.99},
                {"name": "Item 2", "price": 12.99},
            ],
        }

    def test_valid_menu_serializer(self):
        """Test valid data serialization for Menu"""
        serializer = MenuSerializer(data=self.valid_menu_data)
        self.assertTrue(serializer.is_valid())
        menu = serializer.save()
        self.assertEqual(menu.restaurant.id, self.valid_menu_data["restaurant"])
        self.assertEqual(len(menu.items.all()), len(self.valid_menu_data["items"]))


class ItemSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant", owner_id=self.user
        )
        self.menu = Menu.objects.create(restaurant=self.restaurant, date="2024-12-10")
        self.valid_item_data = {
            "name": "Test Item",
            "price": 9.99,
        }

    def test_valid_item_serializer(self):
        """Test valid data serialization for Item"""
        serializer = ItemSerializer(data=self.valid_item_data)
        self.assertTrue(serializer.is_valid())
        item = serializer.save()
        self.assertEqual(item.name, self.valid_item_data["name"])
        self.assertEqual(item.price, self.valid_item_data["price"])
