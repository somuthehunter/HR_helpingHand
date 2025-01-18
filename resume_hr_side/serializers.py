from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=6, required=True)

    class Meta:
        model = User
        fields = ["email", "name", "role", "password"]

    def create(self, validated_data):
        """Create a new user and hash their password."""
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)
