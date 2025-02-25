from rest_framework import serializers
from tutor_register.models import Tutor
from .models import Schedule
from account.models import User


class ShortUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )

class TutorIdSerializer(serializers.ModelSerializer):
    uid = ShortUserDetailSerializer(read_only=True)

    class Meta:
        model = Tutor
        fields = (
            'uid',
            'id',
        )


class ScheduleSerializer(serializers.ModelSerializer):
    tutor_id = TutorIdSerializer(read_only=True)
    learner_id = ShortUserDetailSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = (
            'id',
            'tutor_id',
            'learner_id',
            'date_time',
            'is_booked',
            'is_finished'
        )

    def create(self, validated_data):
        schedule = Schedule.objects.create(**validated_data)
        return schedule
