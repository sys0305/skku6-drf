from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password", "phone_number", "email"]

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


from .models import Board


class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ["title", "content", "user"]
