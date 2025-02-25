from django.urls import path
from .views import AuthUserRegistrationView, PeersJWTToken, PeersRefreshToken, UserManagement

urlpatterns = [
    path('token/', PeersJWTToken.as_view(), name='token_create'),
    path('token/refresh/', PeersRefreshToken.as_view(), name='token_refresh'),
    path('register/', AuthUserRegistrationView.as_view(), name='register'),
    path('user/profile/', UserManagement.as_view(), name='user_profile')
]