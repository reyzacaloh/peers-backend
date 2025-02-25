from django.urls import path
from .views import TutorFormUploadAPI,TutorVerifyAPI, TutorDetailsView, TutorRatingAPI, TutorPriceUpdateAPI

urlpatterns = [
    path('upload/', TutorFormUploadAPI.as_view(), name='upload'),
    path('verify/', TutorVerifyAPI.as_view(), name='verify'),
    path('tutor/data', TutorDetailsView.as_view(), name='tutor_details' ),
    path('rate/', TutorRatingAPI.as_view(), name='rate_tutor' ),
    path('price/', TutorPriceUpdateAPI.as_view(), name='price_update'),
]
