from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to include user role"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = user.role
        token['is_verified'] = user.is_verified if hasattr(user, 'is_verified') else False
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add user info to response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
            'is_verified': self.user.is_verified if hasattr(self.user, 'is_verified') else False,
        }
        return data


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'first_name', 'last_name', 'is_verified')
        read_only_fields = ('id', 'is_verified')

