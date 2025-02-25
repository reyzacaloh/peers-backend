from django.urls import path
from .views import ScheduleAPI
urlpatterns = [
    path('', ScheduleAPI.as_view(), name='schedule'),
]