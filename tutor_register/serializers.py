from rest_framework import serializers
from .models import Tutor
from account.serializers import AuthUserRegistrationSerializer, UserSerializer


class TutorFormSerializer(serializers.ModelSerializer):

    uid = serializers.PrimaryKeyRelatedField(read_only=True)
    ktp = serializers.FileField(required=True)
    transkrip = serializers.FileField(required=True)
    ktm_person = serializers.FileField(required=True)

    class Meta:
        model = Tutor
        fields = (
            'uid',
            'subject',
            'university',
            'pddikti',
            'ktp',
            'transkrip',
            'ktm_person',
            'price_per_hour',
            'desc',
        )

    def create(self, validated_data):
        tutor = Tutor.objects.create(**validated_data)
        return tutor

class TutorVerifySerializer(serializers.ModelSerializer):

    uid = AuthUserRegistrationSerializer(read_only=True)
    ktp = serializers.FileField(required=True)
    ktm_person = serializers.FileField(required=True)
    transkrip = serializers.FileField(required=True)
    user_number = serializers.SerializerMethodField()

    class Meta:
        model = Tutor
        fields = (
            'user_number',
            'uid',
            'subject',
            'university',
            'pddikti',
            'ktm_person',
            'ktp',
            'transkrip',
            'is_verified',
            'is_accepted',
        )

    def get_user_number(self, obj):
        tutor_qs = Tutor.objects.order_by('created_date')
        tutor_list = list(tutor_qs)
        return tutor_list.index(obj) + 1

class TutorSerializer(serializers.ModelSerializer):
    ktp = serializers.FileField(required=True)
    ktm_person = serializers.FileField(required=True)
    transkrip = serializers.FileField(required=True)

    class Meta:
        model = Tutor
        fields = (
            'uid',
            'subject',
            'university',
            'pddikti',
            'ktm_person',
            'ktp',
            'transkrip',
            'is_verified',
            'is_accepted',
            'is_submitted'
        )

