from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import (
    UserViewSet,
    UserProfileViewSet,
    ServiceViewSet,
    BarberScheduleViewSet,
    AppointmentViewSet,
    RatingViewSet,
    PaymentViewSet,
    CalendarEventViewSet,
)

# Router registrations
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"profiles", UserProfileViewSet, basename="profile")
router.register(r"services", ServiceViewSet, basename="service")
router.register(r"schedules", BarberScheduleViewSet, basename="schedule")
router.register(r"appointments", AppointmentViewSet, basename="appointment")
router.register(r"ratings", RatingViewSet, basename="rating")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"calendar-events", CalendarEventViewSet, basename="calendar-event")

urlpatterns = [
    path('', views.index, name='index'),
    path('', include(router.urls)),
]

# Swagger / OpenAPI documentation
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Barbershop API",
        default_version='v1',
        description="API documentation for Barbershop",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('openapi.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]