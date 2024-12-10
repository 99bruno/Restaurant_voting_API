from datetime import date as date_datetime
from datetime import datetime

from core.models import User
from django.db import models
from rest_framework.exceptions import ValidationError


class Restaurant(models.Model):
    """
    Represents a restaurant in the restaurant voting system.

    Attributes:
        id (int): The primary key for the restaurant.
        name (str): The name of the restaurant.
        owner_id (User): The user who has access to update the restaurant details.
    """

    id: models.AutoField(primary_key=True)
    name: str = models.CharField(max_length=200, unique=True)
    owner_id: User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_all_restaurants() -> models.QuerySet:
        """
        Get all the restaurants.

        :return: QuerySet
        """

        return Restaurant.objects.all()

    @staticmethod
    def get_restaurant_by_owner_id(owner_id: int) -> models.QuerySet:
        """
        Get the restaurant by the owner id.

        :param owner_id:
        :return: QuerySet
        """

        return Restaurant.objects.filter(owner_id=owner_id)


class Menu(models.Model):
    """
    Represents a menu in the restaurant voting system.

    Attributes:
        id (int): The primary key for the menu.
        restaurant (Restaurant): The restaurant to which the menu belongs.
        date (date): The date of the menu.
    """

    id: models.AutoField(primary_key=True)
    date: date_datetime = models.DateField(default=date_datetime.today)
    restaurant: Restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="menus"
    )

    def __str__(self) -> str:
        return str(self.date) + " - " + self.restaurant.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "restaurant"], name="unique_menu_per_day_per_restaurant"
            )
        ]

    @staticmethod
    def get_menu_by_restaurant_id(restaurant_id: int) -> models.QuerySet:
        """
        Get the menu for a restaurant by the restaurant id.

        :param restaurant_id:
        :return: QuerySet
        """

        return Menu.objects.filter(restaurant=restaurant_id)

    @staticmethod
    def get_menu_by_date(
        date_menu: date_datetime = date_datetime.today(),
    ) -> models.QuerySet:
        """
        Get the menu for a restaurant by the date. By default, it returns the menu for today.

        :param date_menu:
        :return: QuerySet
        """

        return Menu.objects.filter(date=date_menu)

    def is_vote_allowed(self) -> bool:
        """
        Check if vote is allowed for the menu. Vote is allowed if the menu date is today or in the future.

        :return: bool
        """

        return self.date >= datetime.today().date()

    @staticmethod
    def is_menu_exists(menu_id: int) -> bool:
        """
        Check if the menu exists.

        :param menu_id:
        :return: bool
        """

        return Menu.objects.filter(id=menu_id).exists()


class Item(models.Model):
    """
    Represents an item from menu in the restaurant voting system.

    Attributes:
        id (int): The primary key for the item.
        name (str): The name of the item.
        description (str): A detailed description of the item.
        price (float): The price of the item.
    """

    id: models.AutoField(primary_key=True)
    name: str = models.CharField(max_length=200)
    menu: int = models.ForeignKey(
        Menu, on_delete=models.CASCADE, blank=True, null=True, related_name="items"
    )
    description: str = models.TextField(blank=True)
    price: float = models.FloatField()

    def clean(self):
        """
        Validates the price to ensure it's not negative.
        """
        if self.price < 0:
            raise ValidationError("Price cannot be negative.")

    def __str__(self) -> str:
        return self.name
