import re
import requests
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext_lazy as _

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from user.models import User
from utils.send_email import send_email


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "latitude", "longitude", "role"]

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError(_("email cannot be empty"))
        return value

    def validate_coordinates_with_precision(self, value):
        lat_long_pattern = r"^-?\d{1,3}\.\d{1,6}$"
        if not re.match(lat_long_pattern, str(value)):
            return False
        return True

    def validate_latitude(self, value):
        if not self.validate_coordinates_with_precision(value):
            raise serializers.ValidationError(
                _("Invalid latitude format. Max 6 decimal places allowed.")
            )

        if not (-90 <= value <= 90):
            raise serializers.ValidationError(
                _("Invalid latitude. It must be between -90 and 90.")
            )

        return value

    def validate_longitude(self, value):
        if not self.validate_coordinates_with_precision(value):
            raise serializers.ValidationError(
                _("Invalid latitude format. Max 6 decimal places allowed.")
            )
        if not (-180 <= value <= 180):
            raise serializers.ValidationError(
                _("Invalid longitude. It must be between -180 and 180.")
            )
        return value

    def validate(self, data):
        request = self.context.get("request")
        try:
            data["latitude"]
            data["longitude"]
        except:
            location_data = self.get_geolocation(request)
            data["latitude"] = location_data["latitude"]
            data["longitude"] = location_data["longitude"]
        return data

    def create(self, validated_data):
        group = Group.objects.get(name=validated_data["role"])
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            latitude=validated_data["latitude"],
            longitude=validated_data["longitude"],
        )
        user.groups.add(group)

        return user

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        ip = "8.8.8.8"
        return ip

    def get_geolocation(self, request):
        try:
            ip = self.get_client_ip(request)
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            if data["status"] == "success":
                return {
                    "latitude": data.get("lat"),
                    "longitude": data.get("lon"),
                    "city": data.get("city"),
                    "country": data.get("country"),
                }
            else:
                raise serializers.ValidationError(_("something want wrong"))
        except Exception as e:
            raise serializers.ValidationError(_("something want wrong"))


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                _("This email address is not associated with any account.")
            )
        return value

    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user=user)
        request = self.context.get("request")
        domain = get_current_site(request).domain
        reset_link = f"http://{domain}/api/user/password_reset_confirm/{uid}/{token}/"
        data = {
            "subject": "Password Reset",
            "message": f"Click the link to reset your password: {reset_link}",
            "from_email": "noreply@library.com",
            "to_email": email,
        }
        send_email(data)


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        uid = self.context.get("uid")
        token = self.context.get("token")
        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError("Invalid user.")

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Invalid or expired token.")
        return data

    def save(self):
        uid = self.context.get("uid")
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)
        user.set_password(self.validated_data["new_password"])
        user.save()
