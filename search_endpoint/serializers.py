from rest_framework import serializers
from tutor_register.models import Tutor
from account.models import User


class UserOfTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'date_of_birth',
            'profile_picture',
        )


class GetTutorSerializer(serializers.ModelSerializer):
    uid = UserOfTutorSerializer()

    class Meta:
        model = Tutor
        fields = (
            'subject',
            'university',
            'is_verified',
            'is_accepted',
            'uid',
            'desc',
            'price_per_hour',
            'rating',
            'review_count'
        )
