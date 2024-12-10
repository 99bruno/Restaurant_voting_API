from core.views import BaseView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from restaurants.serializers import MenuSerializer

from .models import Vote
from .serializers import VoteSerializer, VoteStatisticsSerializer


class VoteView(BaseView):
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        """
        Method to create a new vote

        :param request:
        :return:
        """
        data = request.data
        data["user"] = request.user.id
        return self.validate_serializer(VoteSerializer(data=data))

    def get(self, request: Request):
        """
        Method to get the statistics of the votes for the day

        :param request:
        :return:
        """

        return self.response_200(
            VoteStatisticsSerializer(Vote.get_votes_for_day(), many=True)
        )


class VoteDetailView(BaseView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Method to get today menu
        :param request:
        :return:
        """

        return self.response_200(MenuSerializer(Vote.get_today_menu(), many=True))
