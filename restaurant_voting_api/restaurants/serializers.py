from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Item, Menu, Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name", "owner_id"]
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": False},
            "owner_id": {"required": True},
        }

    def validate(self, data):
        """
        Validate the serializer data

        :param data:
        :return:
        """

        allowed_keys = {"name", "owner_id"}
        extra_keys = set(self.initial_data.keys()) - allowed_keys
        if extra_keys:
            raise ValidationError(f"Unexpected fields: {', '.join(extra_keys)}")
        return data


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["name", "price", "description"]


class MenuSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Menu
        fields = ["id", "date", "restaurant", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        menu = Menu.objects.create(**validated_data)
        for item_data in items_data:
            Item.objects.create(menu=menu, **item_data)
        return menu
