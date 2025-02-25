from django.urls import path
from .views import make_transaction, get_learner_unpaid_booking,\
    get_tutor_booked_schedule, get_tutor_total_income,\
    get_update_from_midtrans, cancel_booking,get_learner_paid_booking, \
    get_tutor_paid_booked_schedule

urlpatterns = [
    path('book', make_transaction, name='book'),
    path('update-midtrans', get_update_from_midtrans, name='update-midtrans'),
    path('booked-list', get_tutor_booked_schedule, name='booked-list'),
    path('booking-list', get_learner_unpaid_booking, name='booking-list'),
    path('cancel', cancel_booking, name='cancel-booking'),
    path('tutor-income', get_tutor_total_income, name='tutor-income'),
    path('booking-paid', get_learner_paid_booking, name='booking-paid'),
    path('tutor-paid-list',get_tutor_paid_booked_schedule, name="tutor-paid-schedule")
]
