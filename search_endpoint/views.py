from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from account.models import User
from tutor_register.models import Tutor
from .permissions import OnlyAuthenticated
from .serializers import GetTutorSerializer
from schedule.models import Schedule
from schedule.serializers import ScheduleSerializer


@method_decorator(csrf_exempt, name='dispatch')
class SearchTutorAPI(APIView):
    serializer_class = GetTutorSerializer
    permission_classes = (OnlyAuthenticated, )

    def get(self, request):
        status_code = status.HTTP_200_OK
        query_params = request.query_params
        sub = query_params.get('sub', False)
        tutor_id = query_params.get('id', False)
        if sub:
            tutors = Tutor.objects.prefetch_related('uid').filter(subject = sub, is_accepted=True)
            serializer = GetTutorSerializer(tutors, many=True)
        elif tutor_id:
            users = User.objects.filter(pk = tutor_id)
            if len(users) == 0:
                raise NotFound('Tutor tidak ditemukan')
            tutor = Tutor.objects.get(uid = users.first())
            serializer = GetTutorSerializer([tutor], many=True)
            schedules = Schedule.objects.select_related('tutor_id','learner_id').filter(tutor_id = tutor)
        else:
            tutors = Tutor.objects.prefetch_related('uid').filter(is_accepted=True)
            serializer = GetTutorSerializer(tutors, many=True)
        response = {
            'statusCode': status_code,
            'tutors': serializer.data,
        }
        if tutor_id:
            schedules_serializer = ScheduleSerializer(schedules, many=True)
            response['schedules'] = schedules_serializer.data

        return Response(response, status=status_code)
