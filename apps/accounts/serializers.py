from rest_framework import serializers

from .models import User


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "profile_image",
            "is_staff",
        )

    def get_profile_image(self, obj):
        request = self.context.get("request")

        if obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url)

        return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "shop",
            "is_active",
            "created_at",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "shop",
        )

    def create(self, validated_data,):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user

class ChangePasswordSerializer(serializers.Serializer,):
    old_password = serializers.CharField(required=True, write_only=True,)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6,)

class ResetPasswordSerializer(serializers.Serializer,):
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=6,
    )