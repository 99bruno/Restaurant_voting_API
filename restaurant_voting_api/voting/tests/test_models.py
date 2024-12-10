from datetime import date

from core.models import User
from django.test import TestCase
from django.utils import timezone
from restaurants.models import Menu, Restaurant
from voting.models import Vote


class VoteModelTest(TestCase):

    def setUp(self):
        # Create a test user and a restaurant owner user
        self.restaurant_owner = User.objects.create_user(
            username="owner", password="password", is_admin=True
        )

        # Create a restaurant and assign the owner
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant", owner_id=self.restaurant_owner
        )

        # Create regular test user
        self.user = User.objects.create_user(username="testuser", password="password")

        # Create test menus for the restaurant
        self.menu = Menu.objects.create(restaurant=self.restaurant, date=date.today())

        # Create votes for testing
        Vote.objects.create(user=self.user, menu=self.menu)

    def test_no_votes_for_nonexistent_date(self):
        # Test that no votes are returned for a nonexistent date
        votes = Vote.get_votes_for_day(date.today() + timezone.timedelta(days=1))
        self.assertEqual(len(votes), 0)
