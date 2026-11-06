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
