import requests
import json
from .models import Transaction
from tutor_register.models import Tutor
from account.models import User
from schedule.models import Schedule
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import uuid
from rest_framework import status
from django.db.models import Q, Sum
from account.serializers import UserSerializer

HEADER_APPLICATION_JSON = "application/json"


def create_snap_token(order_id, gross_amount, user, tutor):
    url = settings.MIDTRANS_URL

    payload = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": gross_amount
        },
        "credit_card": {"secure": True},
        "customer_details": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        },
        "item_details": {
            "tutor_name": tutor.uid.first_name + " " + tutor.uid.last_name,
            "tutor_id": tutor.pk,
            "tutor_email": tutor.uid.email,
            "name": tutor.subject,
            "price": gross_amount,
            "quantity": 1
        },
        "custom_expiry": {
            "expiry_duration": 5,
            "unit": "minute"
        }
    }
    headers = {
        "accept": HEADER_APPLICATION_JSON,
        "content-type": HEADER_APPLICATION_JSON,
        "authorization": "Basic " + settings.MIDTRANS_AUTH.decode('UTF-8')
    }

    response = requests.post(url, json=payload, headers=headers)
    return json.loads(response.text)["token"]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def make_transaction(request):
    data = json.loads(request.body)
    users = User.objects.filter(pk = data['tutor_id'])
    tutor = Tutor.objects.get(uid = users.first())
    learner = User.objects.get(email=request.user.email)
    schedule = Schedule.objects.get(pk=data['schedule_id'])

    if schedule.is_booked:
        return JsonResponse({"message": "Failed. Not Available"}, status=status.HTTP_417_EXPECTATION_FAILED)

    price = tutor.price_per_hour
    transaction_id = uuid.uuid4()
    snap_token = create_snap_token(str(transaction_id), price, learner, tutor)
    schedule.is_booked = True
    schedule.learner_id = learner

    transaction = Transaction(transaction_id=transaction_id, learner=learner, tutor=tutor, schedule=schedule,
                            price=price, status="PENDING", snap_token=snap_token)
    transaction.save()
    schedule.save()
    return JsonResponse({"message": "Booking has been created", "token": snap_token}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def get_update_from_midtrans(request):
    data = json.loads(request.body)
    transaction_status = data["transaction_status"]
    if transaction_status == "cancel":
        return JsonResponse({'message': 'Not Handled'}, status=status.HTTP_200_OK)

    transaction = Transaction.objects.get(transaction_id=data['order_id'])
    schedule = Schedule.objects.get(pk=transaction.schedule.pk)
    if transaction_status == "settlement" or transaction_status == "capture":
        transaction.status = "COMPLETED"
        schedule.is_booked = True
        schedule.learner_id = transaction.learner
        transaction.save()
        schedule.save()
        return JsonResponse({'message': 'Booking success'}, status=status.HTTP_201_CREATED)
    elif transaction_status == "deny":
        transaction.status = "FAILED"
        schedule.is_booked = False
        transaction.save()
        schedule.save()
        return JsonResponse({'message': 'Booking failed'}, status=status.HTTP_200_OK)
    elif transaction_status == 'expired':
        transaction.status = "EXPIRED"
        schedule.is_booked = False
        transaction.save()
        schedule.save()
        return JsonResponse({'message': 'Transaction expired'}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'Status Not Known'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_tutor_booked_schedule(request):
    user = Tutor.objects.get(uid__email=request.user.email)
    transactions = Transaction.objects.filter(tutor=user)
    transaction_list = []
    for transaction in transactions:
        transaction_list.append({
            "transaction_id": transaction.transaction_id,
            "date": transaction.date,
            "schedule": Schedule.objects.get(pk=transaction.schedule.pk).date_time,
            "price": transaction.price,
            "status": transaction.status,
            "snap_token": transaction.snap_token,
            "learner_name": User.objects.get(email=transaction.learner.email).first_name,
        })
    return JsonResponse({'transactions': transaction_list}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_learner_unpaid_booking(request):
    transactions = Transaction.objects.filter(Q(learner=request.user) & Q(status="PENDING"))
    transaction_list = []
    for transaction in transactions:
        tutor = transaction.tutor.uid
        transaction_list.append({
            "transaction_id": transaction.transaction_id,
            "date": transaction.date,
            "schedule": Schedule.objects.get(pk=transaction.schedule.pk).date_time,
            "price": transaction.price,
            "status": transaction.status,
            "snap_token": transaction.snap_token,
            "tutor_name": tutor.first_name + " " + tutor.last_name,
            "subject": transaction.tutor.subject,
            "tutor_id": transaction.tutor.pk,
            "schedule_id": transaction.schedule.pk
        })
    return JsonResponse({'booking_list': transaction_list}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def cancel_booking(request):
    data = json.loads(request.body)
    url = settings.MIDTRANS_CANCEL_URL.format(order_id=data['order_id'])

    headers = {"accept": HEADER_APPLICATION_JSON,  "authorization": "Basic " + settings.MIDTRANS_AUTH.decode('UTF-8')}

    response = requests.post(url, headers=headers)
    if (response.status_code == 200):
        transaction = Transaction.objects.get(transaction_id=data['order_id'])
        schedule = Schedule.objects.get(pk=transaction.schedule.pk)
        schedule.is_booked = False
        schedule.save()
        transaction.delete()
        return JsonResponse({'message': "booking has been cancelled"}, status=status.HTTP_200_OK)
    return JsonResponse({'message': "booking can't be cancelled"}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_tutor_total_income(request):
    try:
        tutor = Tutor.objects.get(uid__email=request.user.email)
        transactions = Transaction.objects.filter(tutor__pk=tutor.pk)
        total_income = transactions.aggregate(Sum('price'))['price__sum'] or 0
        response = {
            "tutor_id": tutor.pk,
            "total_income": total_income
        }
        return JsonResponse(response, status=status.HTTP_200_OK)
    except Tutor.DoesNotExist:
        return JsonResponse({"message": "Tutor not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_learner_paid_booking(request):
    transactions = Transaction.objects.filter(Q(learner=request.user) & Q(status="COMPLETED"))
    transaction_list = []
    serializer_class = UserSerializer
    for transaction in transactions:
        tutor = transaction.tutor.uid
        user = User.objects.filter(uid=tutor.uid)[0]
        user_data = serializer_class(user)
        transaction_list.append({
            "transaction_id": transaction.transaction_id,
            "date": transaction.date,
            "schedule": Schedule.objects.get(pk=transaction.schedule.pk).date_time,
            "price": transaction.price,
            "status": transaction.status,
            "snap_token": transaction.snap_token,
            "tutor_email": user_data.data['email'],
            "tutor_name": tutor.first_name + " " + tutor.last_name,
            "subject": transaction.tutor.subject,
            "uid": tutor.uid,
            "profile_pic":user_data.data['profile_picture'],
            "schedule_id": transaction.schedule.pk
        })
    return JsonResponse({'booking_list': transaction_list}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_tutor_paid_booked_schedule(request):
    user = Tutor.objects.get(uid__email=request.user.email)
    transactions = Transaction.objects.filter(Q(tutor=user) & Q(status="COMPLETED"))
    print(user)
    print(transactions)
    transaction_list = []
    for transaction in transactions:
        transaction_list.append({
            "transaction_id": transaction.transaction_id,
            "date": transaction.date,
            "schedule": Schedule.objects.get(pk=transaction.schedule.pk).date_time,
            "price": transaction.price,
            "status": transaction.status,
            "snap_token": transaction.snap_token,
            "uid": User.objects.get(email=transaction.learner.email).uid,
        })
    return JsonResponse({'booking_list': transaction_list}, status=status.HTTP_200_OK)