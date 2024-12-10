from rest_framework import serializers
from restaurants.models import Menu

from .models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["user", "menu"]

    def validate(self, data) -> dict:
        """
        Validate the serializer data

        :param data:
        :return:
        """

        # Check if the menu exists
        if not Menu.is_menu_exists(data["menu"].id):
            raise serializers.ValidationError("The menu does not exist.")

        # Check if the user has already voted for this menu
        if Vote.is_user_voted(data["user"], data["menu"]):
            raise serializers.ValidationError("You have already voted for this menu.")

        # Check if the voting for this menu is allowed
        if not data["menu"].is_vote_allowed():
            raise serializers.ValidationError("Voting for this menu is closed.")

        return data


class VoteStatisticsSerializer(serializers.Serializer):
    menu = serializers.IntegerField()
    vote_count = serializers.IntegerField()
    restaurant_id = serializers.IntegerField()
