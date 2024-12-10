from .models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},  # Email обов'язковий
            'username': {'required': True},  # Ім'я користувача обов'язкове
        }

    @staticmethod
    def validate_email(value):
        """
        Validate email field

        :param value:
        :return:
        """
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        """
        Validate the serializer data

        :param data:
        :return:
        """
        allowed_keys = {'username', 'email', 'password'}
        extra_keys = set(self.initial_data.keys()) - allowed_keys
        if extra_keys:
            raise ValidationError(f"Unexpected fields: {', '.join(extra_keys)}")
        return data

    def create(self, validated_data):
        """
        Create a new user

        :param validated_data:
        :return:
        """
        return User.objects.create_user(**validated_data)
