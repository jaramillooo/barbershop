from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    UserProfile,
    Service,
    BarberSchedule,
    Appointment,
    Rating,
    Payment,
    CalendarEvent,
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django User model with password hashing."""
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "date_joined",
            "password",
        ]
        read_only_fields = ["id", "is_active", "date_joined"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source="user", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
            "user_detail",
            "role",
            "phone_number",
            "google_id",
            "created_at",
            "active",
        ]
        read_only_fields = ["id", "created_at"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "duration_minutes",
            "price",
            "description",
            "active",
        ]
        read_only_fields = ["id"]


class BarberScheduleSerializer(serializers.ModelSerializer):
    barber_detail = UserSerializer(source="barber", read_only=True)

    class Meta:
        model = BarberSchedule
        fields = [
            "id",
            "barber",
            "barber_detail",
            "day_of_week",
            "start_time",
            "end_time",
            "active",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        start = attrs.get("start_time")
        end = attrs.get("end_time")
        if start and end and end <= start:
            raise serializers.ValidationError("end_time must be after start_time.")
        day = attrs.get("day_of_week")
        if day and (day < 1 or day > 7):
            raise serializers.ValidationError("day_of_week must be between 1 and 7.")
        return attrs


class AppointmentSerializer(serializers.ModelSerializer):
    client_detail = UserSerializer(source="client", read_only=True)
    barber_detail = UserSerializer(source="barber", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "client",
            "client_detail",
            "barber",
            "barber_detail",
            "appointment_datetime",
            "duration_minutes",
            "status",
            "notes",
            "created_at",
            "active",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        client = attrs.get("client") or getattr(self.instance, "client", None)
        barber = attrs.get("barber") or getattr(self.instance, "barber", None)
        if client and barber and client == barber:
            raise serializers.ValidationError("client and barber must be different users.")

        duration = attrs.get("duration_minutes")
        if duration is not None and duration <= 0:
            raise serializers.ValidationError("duration_minutes must be positive.")

        # Optional: ensure the selected barber has BARBER role if profile exists
        try:
            if barber and hasattr(barber, "profile") and barber.profile.role != "barber":
                raise serializers.ValidationError("Selected user is not a barber.")
        except Exception:
            # If no profile, skip strict validation (can be enforced at data level later)
            pass

        return attrs


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            "id",
            "appointment",
            "user",
            "score",
            "comment",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "appointment",
            "amount",
            "currency",
            "status",
            "paid_at",
            "provider",
        ]
        read_only_fields = ["id"]


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = [
            "id",
            "appointment",
            "external_event_id",
            "provider",
            "synced_at",
        ]
        read_only_fields = ["id"]
