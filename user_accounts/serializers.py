from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


# class CustomRegistrationSerializer(RegisterSerializer):
#     _has_phone_field = False  # Your own flag to track if phone is used
#     # phone_number = serializers.Char

#     def get_cleaned_data(self):
#         """Return validated registration data without forcing phone_number."""
#         data = super().get_cleaned_data()

#         return data


# -------------------------
# Registration Serializer
# -------------------------
class CustomRegistrationSerializer(RegisterSerializer):

    username = None  # No username
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    def get_cleaned_data(self):
        """Return validated registration data for user and profile."""
        data = super().get_cleaned_data()
        data.update(
            {
                "first_name": self.validated_data.get("first_name", ""),  # type: ignore
                "last_name": self.validated_data.get("last_name", ""),  # type: ignore
                "phone": self.validated_data.get("phone", ""),  # type: ignore
            }
        )
        return data

    def save(self, request):
        """Create user and their profile with extra fields."""
        user = super().save(request)
        cleaned_data = self.get_cleaned_data()

        user.first_name = cleaned_data["first_name"]
        user.last_name = cleaned_data["last_name"]
        user.save()

        return user


# -------------------------
# Login Serializer
# -------------------------
class CustomLoginSerializer(LoginSerializer):
    username = None  # No username
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(self.context["request"], email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        attrs["user"] = user
        return attrs
