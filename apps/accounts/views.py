from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import (
    FormParser,
    MultiPartParser,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.auditlog.utils import create_audit_log

from .serializers import (
    ChangePasswordSerializer,
    UserProfileSerializer,
)


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
        
@extend_schema(request=ChangePasswordSerializer,responses={200: dict, 400: dict,},)
class ChangePasswordView(APIView,):
    permission_classes = (IsAuthenticated,)

    def post(self, request,):
        serializer = ChangePasswordSerializer(data=request.data,)
        serializer.is_valid(raise_exception=True,)
        
        if (
            serializer.validated_data["old_password"]
            == serializer.validated_data["new_password"]
        ):
            return Response(
                {
                    "detail":
                    "New password must be different from current password."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user = request.user

        if not user.check_password(
            serializer.validated_data["old_password"]
        ):
            return Response(
                {
                    "detail":
                    "Old password is incorrect."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(
            serializer.validated_data["new_password"]
        )

        user.save()

        create_audit_log(
            user=user,
            action="PASSWORD_CHANGE",
            model_name="User",
            object_id=user.id,
            description=(
                f"Changed password for "
                f"{user.username}"
            ),
        )

        return Response(
            {
                "message":
                "Password changed successfully."
            }
        )
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer,):
    @classmethod
    def get_token(cls, user,):
        token = super().get_token(user)

        return token

    def validate(self, attrs,):
        data = super().validate(attrs)

        create_audit_log(
            user=self.user,
            action="LOGIN",
            model_name="User",
            object_id=self.user.id,
            description=(
                f"{self.user.username} logged in"
            ),
        )

        return data

class CustomTokenObtainPairView(TokenObtainPairView,):
    serializer_class = CustomTokenObtainPairSerializer