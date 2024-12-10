from django.urls import path

from .views import MenuView, RestaurantView, TodayMenuView

urlpatterns = [
    path("", RestaurantView.as_view(), name="token_refresh"),
    path("<int:restaurant_id>/menu/", MenuView.as_view(), name="restaurant"),
    path("menu/", TodayMenuView.as_view(), name="menu"),
]
