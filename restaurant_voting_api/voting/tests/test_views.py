from datetime import date

from core.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from restaurants.models import Menu, Restaurant
from voting.models import Vote


class VoteViewTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password")

        # Create a restaurant and menu for testing
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant", owner_id=self.user
        )
        self.menu = Menu.objects.create(restaurant=self.restaurant, date=date.today())

        # Set up URLs
        self.vote_url = reverse("vote-list")
        self.vote_statistics_url = reverse("vote-list")
        self.vote_detail_url = reverse("vote-detail")

    def test_create_vote(self):
        """
        Test creating a new vote for the menu.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "menu": self.menu.id,
        }

        # Send POST request to create a vote
        response = self.client.post(self.vote_url, data, format="json")

        # Assert the response is successful (status code 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert the vote was created in the database
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(Vote.objects.first().user, self.user)
        self.assertEqual(Vote.objects.first().menu, self.menu)

    def test_create_vote_unauthenticated(self):
        """
        Test that creating a vote without authentication fails.
        """
        data = {
            "menu": self.menu.id,
        }

        # Send POST request without authentication
        response = self.client.post(self.vote_url, data, format="json")

        # Assert the response is unauthorized (status code 401)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_vote_statistics(self):
        """
        Test fetching vote statistics for the day.
        """
        # Create some votes for the menu
        Vote.objects.create(user=self.user, menu=self.menu)

        self.client.force_authenticate(user=self.user)

        # Send GET request to fetch vote statistics for the day
        response = self.client.get(self.vote_statistics_url)

        # Assert the response is successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response data contains the vote statistics
        self.assertGreater(len(response.data), 0)

    def test_get_today_menu(self):
        """
        Test fetching the menu with the most votes for today.
        """
        # Create some votes for the menu
        Vote.objects.create(user=self.user, menu=self.menu)

        self.client.force_authenticate(user=self.user)

        # Send GET request to fetch the menu with the most votes for today
        response = self.client.get(
            reverse("vote-detail")
        )  # Adjust with the correct URL name

        # Assert the response is successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response data contains the correct menu
        self.assertEqual(len(response.data), 1)  # Only one menu with max votes
        self.assertEqual(response.data[0]["id"], self.menu.id)
