from rest_framework import serializers

from .models import User

class AuthUserRegistrationSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = (
            'email',
            'uid',
            'password',
            'first_name',
            'last_name',
            'date_of_birth',
            'profile_picture',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'email', 'first_name', 'last_name', 'role', 'date_joined', 'is_active', 'is_deleted', 'created_date', 'modified_date', 'created_by', 'modified_by', 'date_of_birth', 'profile_picture']
        read_only_fields = ['uid', 'date_joined', 'is_active', 'is_deleted', 'created_date', 'modified_date', 'created_by', 'modified_by']
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user