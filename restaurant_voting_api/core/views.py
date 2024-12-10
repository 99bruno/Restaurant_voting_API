from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class BaseView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def validate_serializer(serializer):
        """
        Method to validate a serializer and return the response

        :param serializer:
        :return:
        """
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def response_200(serializer):
        """
        Method to return a 200 response

        :param serializer:
        :return:
        """

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def validate_user_creation(serializer, *, is_admin=False):
        """
        Method to validate a serializer and return the response

        :param serializer:
        :param is_admin:
        :return:
        """

        if serializer.is_valid():
            user = serializer.save(is_admin=is_admin, is_superuser=is_admin)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'username': user.username,
                'email': user.email,
                'access_token': access_token,
                'refresh_token': str(refresh),
            }, status=status.HTTP_201_CREATED)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(BaseView):
    permission_classes = []

    def post(self, request):
        """
        Method to register a new user and return a jwt token

        :param request:
        :return:
        """

        return self.validate_user_creation(UserSerializer(data=request.data))


class SuperUserRegistrationView(BaseView):
    def post(self, request):
        """
        Method to register a new superuser and return a jwt token

        :param request:
        :return:
        """
        user = request.user
        if not hasattr(user, 'is_admin') or not user.is_admin:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        return self.validate_user_creation(UserSerializer(data=request.data), is_admin=True)
