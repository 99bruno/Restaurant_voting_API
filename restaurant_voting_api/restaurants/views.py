from core.views import BaseView
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Menu, Restaurant
from .serializers import MenuSerializer, RestaurantSerializer


class RestaurantView(BaseView):

    def get(self, request: Request) -> Response:
        """
        Method to get the list of all restaurants

        :param request:
        :return:
        """

        return self.response_200(
            RestaurantSerializer(Restaurant.get_all_restaurants(), many=True)
        )

    def post(self, request) -> Response:
        """
        Method to create a new restaurant only for admin users

        :param request:
        :return:
        """
        if not request.user.is_admin:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return self.validate_serializer(RestaurantSerializer(data=request.data))


class MenuView(BaseView):

    def post(self, request: Request, restaurant_id: int) -> Response:
        """
        Method to create a new menu only for admin users or restaurant owners

        :param restaurant_id:
        :param request:
        :return:
        """
        user = request.user

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise NotFound(detail="Restaurant not found.")

        if not (user.is_admin or user.id == restaurant.owner_id.id):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data.copy()
        data["restaurant"] = restaurant_id

        return self.validate_serializer(MenuSerializer(data=data))

    def get(self, request: Request, restaurant_id: int) -> Response:
        """
        Method to get the menu of a restaurant

        :param restaurant_id:
        :param request:
        :return:
        """
        menus = Menu.get_menu_by_restaurant_id(restaurant_id)
        if not menus:
            return Response(
                {"detail": "No menus found for this restaurant."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return self.response_200(MenuSerializer(menus, many=True))


class TodayMenuView(BaseView):

    def get(self, request: Request) -> Response:
        """
        Method to get the menu of all restaurants for today

        :param request:
        :return:
        """

        return self.response_200(MenuSerializer(Menu.get_menu_by_date(), many=True))
