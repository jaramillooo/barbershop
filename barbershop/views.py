from django.shortcuts import render

# Django REST framework imports
from rest_framework import viewsets
from rest_framework import filters

# Models and serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile,
    Service,
    BarberSchedule,
    Appointment,
    Rating,
    Payment,
    CalendarEvent,
)
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    ServiceSerializer,
    BarberScheduleSerializer,
    AppointmentSerializer,
    RatingSerializer,
    PaymentSerializer,
    CalendarEventSerializer,
)

from django_filters.rest_framework import DjangoFilterBackend


# Existing template view
def index(request):
    return render(request, 'barbershop/index.html')


# API ViewSets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {"is_active": ["exact"], "email": ["exact"]}
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering_fields = ["id", "date_joined", "username"]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related("user").all().order_by("-created_at")
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {"user": ["exact"], "role": ["exact"], "active": ["exact"]}
    search_fields = ["user__username", "phone_number"]
    ordering_fields = ["created_at", "id"]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by("name")
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {"active": ["exact"], "price": ["gte", "lte"]}
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price", "id"]


class BarberScheduleViewSet(viewsets.ModelViewSet):
    queryset = (
        BarberSchedule.objects.select_related("barber")
        .all()
        .order_by("barber_id", "day_of_week", "start_time")
    )
    serializer_class = BarberScheduleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {"barber": ["exact"], "day_of_week": ["exact"], "active": ["exact"]}
    search_fields = ["barber__username"]
    ordering_fields = ["day_of_week", "start_time", "end_time", "id"]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = (
        Appointment.objects.select_related("client", "barber")
        .prefetch_related("ratings", "payments", "calendar_events")
        .all()
        .order_by("-appointment_datetime")
    )
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "client": ["exact"],
        "barber": ["exact"],
        "status": ["exact"],
        "active": ["exact"],
        "appointment_datetime": ["date", "gte", "lte"],
    }
    search_fields = ["notes", "client__username", "barber__username"]
    ordering_fields = ["appointment_datetime", "duration_minutes", "id"]


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.select_related("appointment", "user").all().order_by("-created_at")
    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {"appointment": ["exact"], "user": ["exact"], "score": ["gte", "lte", "exact"]}
    search_fields = ["comment", "user__username"]
    ordering_fields = ["created_at", "score", "id"]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("appointment").all().order_by("-id")
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "appointment": ["exact"],
        "status": ["exact"],
        "provider": ["exact"],
        "amount": ["gte", "lte"],
    }
    search_fields = ["provider"]
    ordering_fields = ["id", "amount", "paid_at"]


class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.select_related("appointment").all().order_by("-id")
    serializer_class = CalendarEventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {"appointment": ["exact"], "provider": ["exact"]}
    search_fields = ["external_event_id", "provider"]
    ordering_fields = ["id", "synced_at"]