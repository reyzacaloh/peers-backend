from django.urls import path
from.views import SearchTutorAPI
urlpatterns = [
    path('', SearchTutorAPI.as_view(), name='search'),
]
