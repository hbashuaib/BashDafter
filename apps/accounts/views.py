from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import (
    FormParser,
    MultiPartParser,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserProfileSerializer


class HealthCheckView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        return Response({"status": "success", "app": "BashDafter", "version": "1.0.0"})


class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        return {
            "request": self.request,
        }


class UploadProfileImageView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def post(
        self,
        request,
    ):
        user = request.user
        image = request.FILES.get("profile_image")

        if image:
            user.profile_image = image
            user.save()

        return Response(
            UserProfileSerializer(
                user,
                context={
                    "request": request,
                },
            ).data
        )
