from django.test import TestCase
from core.models import User
from restaurants.models import Restaurant, Menu, Item
from datetime import date
from rest_framework.exceptions import ValidationError


class RestaurantModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", owner_id=self.user)

    def test_create_restaurant(self):
        """Test creating a restaurant"""
        self.assertEqual(self.restaurant.name, "Test Restaurant")
        self.assertEqual(self.restaurant.owner_id, self.user)

    def test_get_all_restaurants(self):
        """Test getting all restaurants"""
        restaurant = Restaurant.objects.create(name="Second Restaurant", owner_id=self.user)
        restaurants = Restaurant.get_all_restaurants()
        self.assertEqual(len(restaurants), 2)

    def test_get_restaurant_by_owner(self):
        """Test getting restaurants by owner id"""
        restaurant = Restaurant.objects.create(name="Second Restaurant", owner_id=self.user)
        owner_restaurants = Restaurant.get_restaurant_by_owner_id(self.user.id)
        self.assertEqual(len(owner_restaurants), 2)


class MenuModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", owner_id=self.user)
        self.menu = Menu.objects.create(restaurant=self.restaurant, date=date.today())

    def test_create_menu(self):
        """Test creating a menu"""
        self.assertEqual(self.menu.restaurant, self.restaurant)
        self.assertEqual(self.menu.date, date.today())

    def test_is_vote_allowed_today(self):
        """Test if vote is allowed for today"""
        self.assertTrue(self.menu.is_vote_allowed())

    def test_is_vote_allowed_future(self):
        """Test if vote is allowed for a future date"""
        future_menu = Menu.objects.create(restaurant=self.restaurant, date=date(2024, 12, 31))
        self.assertTrue(future_menu.is_vote_allowed())

    def test_is_vote_not_allowed_past(self):
        """Test if vote is not allowed for a past date"""
        past_menu = Menu.objects.create(restaurant=self.restaurant, date=date(2023, 12, 31))
        self.assertFalse(past_menu.is_vote_allowed())

    def test_get_menu_by_restaurant(self):
        """Test getting menu by restaurant id"""
        menus = Menu.get_menu_by_restaurant_id(self.restaurant.id)
        self.assertEqual(len(menus), 1)

    def test_get_menu_by_date(self):
        """Test getting menu by date"""
        menus = Menu.get_menu_by_date(date.today())
        self.assertEqual(len(menus), 1)


class ItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", owner_id=self.user)
        self.menu = Menu.objects.create(restaurant=self.restaurant, date=date.today())
        self.item = Item.objects.create(name="Test Item", menu=self.menu, price=10.99)

    def test_create_item(self):
        """Test creating an item"""
        self.assertEqual(self.item.name, "Test Item")
        self.assertEqual(self.item.menu, self.menu)
        self.assertEqual(self.item.price, 10.99)

    def test_item_price_validation(self):
        """Test item price validation"""
        item = Item(name="Invalid Item", menu=self.menu, price=-1)
        with self.assertRaises(ValidationError):
            item.clean()  # This should raise a ValidationError because price is negative

    def test_get_items_by_menu(self):
        """Test getting items by menu"""
        items = self.menu.items.all()
        self.assertEqual(len(items), 1)

    def test_item_str(self):
        """Test string representation of an item"""
        self.assertEqual(str(self.item), "Test Item")


