from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from schedule.models import Schedule
from account.permissions import OnlyAdmin, OnlyLearner

from .models import Tutor
from .serializers import (
    TutorFormSerializer, TutorSerializer, TutorVerifySerializer,
)

import math


@method_decorator(csrf_exempt, name='dispatch')
class TutorFormUploadAPI(APIView):
    serializer_class = TutorFormSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (OnlyLearner, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.get(uid=request.user.uid)  # Get User object based on UUID
        data["uid"] = user

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Form is successfully submitted!',
            }

            return Response(response, status=status_code)


@method_decorator(csrf_exempt, name='dispatch')
class TutorVerifyAPI(APIView):
    serializer_class = TutorVerifySerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (OnlyAdmin, )

    def get(self, request):
        applicants = Tutor.objects.filter(is_verified=False).order_by('created_date')

        serializer = self.serializer_class(applicants, many=True)
        status_code = status.HTTP_200_OK
        response = {
            'success': True,
            'statusCode': status_code,
            'applicants': serializer.data
        }
        return Response(response, status_code)

    def patch(self, request):
        applicant = Tutor.objects.get(pddikti=request.data['pddikti'])
        serializer = self.serializer_class(applicant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            if request.data['is_accepted'] == "true":
                User.objects.filter(uid=applicant.uid.uid).update(role=User.TUTOR)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class TutorDetailsView(APIView):
    serializer_class = TutorSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        tutor = Tutor.objects.filter(uid__uid=request.user.uid).first()
        serializer = self.serializer_class(tutor)
        response = {
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'Tutor data fetched',
            'tutor': serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request):
        Tutor.objects.filter(uid__uid=request.user.uid).delete()
        User.objects.filter(uid=request.user.uid).update(role=User.LEARNER)
        response = {
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'tutor uid={uid} has been deleted'.format(uid=request.user.uid)
        }
        return Response(response, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class TutorRatingAPI(APIView):

    permission_classes = (OnlyLearner,)

    def post(self, request):
        try:
            tutor = Tutor.objects.get(id=request.data["tutor_id"])
            schedule = Schedule.objects.get(id=request.data["schedule_id"])
            print(schedule)
            schedule.is_finished = True
            rating = tutor.rating
            rating_count = tutor.review_count + 1
            rating = (rating * tutor.review_count + float(request.data["rating"])) / rating_count
            tutor.rating = math.ceil(rating*100)/100
            tutor.review_count = rating_count
            tutor.save()
            schedule.save()
            response = {
                'message': 'Tutor rating updated',
                'schedule': schedule.id,
                'rating': tutor.rating,
                'rating_count': tutor.review_count,
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            response = {
                'message': 'Error: ' + str(e),
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class TutorPriceUpdateAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        try:
            tutor = Tutor.objects.filter(uid__uid=request.user.uid).first()
            if request.data["new_price"].isnumeric():
                tutor.price_per_hour = int(request.data["new_price"])
                tutor.save()

            response = {
                'message': 'Tutor rates succesfully updated',
                'new_price': tutor.price_per_hour,
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            response = {
                'message': 'Error: ' + str(e),
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
