from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .permissions import OnlyAnon
from tutor_register.models import Tutor
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from search_endpoint.serializers import GetTutorSerializer
from .serializers import (
    AuthUserRegistrationSerializer,
    UserSerializer
)

@method_decorator(csrf_exempt, name='dispatch')
class AuthUserRegistrationView(APIView):
    serializer_class = AuthUserRegistrationSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (OnlyAnon, )

    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        print(valid)
        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data,
            }

            return Response(response, status=status_code)

class PeersJWTTokenSerializer(TokenObtainPairSerializer):
    serializer_class = UserSerializer

    def validate(self, attrs):
        data = super().validate(attrs)
        tutor = Tutor.objects.prefetch_related('uid').filter(uid = self.user)
        if tutor:
            data['is_tutor'] = True
        return data

@method_decorator(csrf_exempt, name='dispatch')
class PeersJWTToken(TokenObtainPairView):
    serializer_class = PeersJWTTokenSerializer

@method_decorator(csrf_exempt, name='dispatch')
class PeersRefreshToken(TokenRefreshView):
    pass

@method_decorator(csrf_exempt, name='dispatch')
class UserManagement(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        response = {
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'User data fetched',
            'user': serializer.data,
        }
        print(response['user'])
       
        tutor = Tutor.objects.prefetch_related('uid').filter(uid = user)
        if tutor:
            tutor_serializer = GetTutorSerializer(tutor, many=True)
            response['tutor'] = tutor_serializer.data[0]
            print(tutor_serializer.data[0])
            
        return Response(response, status=status.HTTP_200_OK)
