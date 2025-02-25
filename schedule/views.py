from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser, FormParser
from search_endpoint.permissions import OnlyAuthenticated
from account.models import User
from tutor_register.models import Tutor
from .serializers import ScheduleSerializer
from .models import Schedule

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class ScheduleAPI(APIView):
    serializer_class = ScheduleSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (OnlyAuthenticated, )

    def post(self, request):
        user = User.objects.get(uid=request.user.uid)
        tutor = Tutor.objects.get(uid=user)
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['tutor_id'] = tutor
        if request.query_params:
            raise ParseError('invalid query params for post')
        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Schedule is Created',
            }

            return Response(response, status=status_code)
        
            

    def get(self, request):
        query_params = request.query_params
        is_tutor = query_params.get('tutor', False)
        if (not query_params) or (not is_tutor):
            raise ParseError('invalid query params for get')
        user = request.user
        try:
            if int(is_tutor)==1:
                tutor = Tutor.objects.get(uid=user)
                schedules = Schedule.objects.select_related('tutor_id','learner_id').filter(tutor_id = tutor)
            else:
                schedules = Schedule.objects.select_related('tutor_id','learner_id').filter(learner_id = user)
        except Tutor.DoesNotExist:
            raise NotFound('Tutor does not exist')
        serializer = ScheduleSerializer(schedules, many=True)
        status_code = status.HTTP_200_OK
        response = {
            'statusCode': status_code,
            'schedules': serializer.data
        }

        return Response(response, status=status_code)

    def delete(self, request):
        query_params = request.query_params
        schedule_id = query_params.get('sid', False)
        try:
            if schedule_id:
                schedule = Schedule.objects.get(pk=schedule_id)
            else:
                raise ParseError('invalid query params for delete')
        except Schedule.DoesNotExist:
            raise NotFound('Schedule does not exist')
        schedule.delete()
        status_code=status.HTTP_204_NO_CONTENT
        response = {
            'statusCode': status_code,
            'status': f"schedule with id {schedule_id} succesfully deleted",
        }
        return Response(response, status=status_code)
