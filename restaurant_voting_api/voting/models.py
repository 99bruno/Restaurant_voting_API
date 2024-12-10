from collections import namedtuple
from datetime import date

from core.models import User
from django.db import models
from django.db.models import Count, Max
from restaurants.models import Menu


class Vote(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    menu: Menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    vote_date: date = models.DateField(auto_now_add=True)

    class Meta:
        """
        Metaclass for the Vote model. Defines the unique_together attribute to ensure that a user can only vote once
        for a menu.
        """

        unique_together = ("user", "menu")

    def __str__(self):
        return f"Vote by {self.user.username} for {self.menu.date}"

    @staticmethod
    def is_user_voted(user: User, menu: Menu) -> bool:
        """
        Check if the user has already voted for the menu.

        :param user:
        :param menu:
        :return:
        """

        return Vote.objects.filter(user=user, menu=menu).exists()

    @staticmethod
    def get_votes_for_day(date_menu: date = date.today()):
        """
        Get the votes for a specific date, including restaurant ID and the corresponding vote counts.
        By default, it returns the votes for today.

        :param date_menu: The date for which to get the votes
        :return: A list of namedtuples with menu IDs, restaurant IDs, vote counts, and menu dates
        """

        # The query retrieves the menu ID, restaurant ID, and vote count for each menu on the specified date.
        votes = (
            Vote.objects.filter(menu__date=date_menu)
            .values("menu", "menu__date", "menu__restaurant", "menu__restaurant__id")
            .annotate(vote_count=Count("id"))
            .order_by("menu")
        )

        VoteCount = namedtuple("VoteCount", ["menu", "restaurant_id", "vote_count"])
        return [
            VoteCount(vote["menu"], vote["menu__restaurant__id"], vote["vote_count"])
            for vote in votes
        ]

    @staticmethod
    def get_today_menu() -> models.QuerySet:
        """
        Get the menus with the maximum vote count for today, including restaurant ID and the corresponding vote counts.
        If multiple menus have the same vote count, they are all returned.

        :return: A list of dictionaries with menu IDs, restaurant IDs, vote counts, and menu dates
        """

        # Annotate each menu with its vote count for today
        votes = (
            Vote.objects.filter(menu__date=date.today())
            .values("menu", "menu__restaurant")
            .annotate(vote_count=Count("id"))
        )

        # Get the maximum vote count for today
        max_vote_count = votes.aggregate(max_votes=Max("vote_count"))["max_votes"]

        # Filter menus that have the maximum vote count
        top_votes = votes.filter(vote_count=max_vote_count)

        # Get the actual menus based on the top votes
        menus_with_max_votes = Menu.objects.filter(
            id__in=[vote["menu"] for vote in top_votes]
        )

        return menus_with_max_votes
