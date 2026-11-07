from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.permissions import (
    IsOwner,
    IsOwnerOrAdmin,
)
from apps.auditlog.utils import create_audit_log

from .models import User
from .serializers import (
    ResetPasswordSerializer,
    UserCreateSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet,):
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(
            shop=self.request.user.shop,
            is_active=True,
        )
        
    def get_permissions(self):
        if self.action in [
            "list",
            "retrieve",
        ]:
            permission_classes = [IsOwnerOrAdmin,]

        elif self.action == "create":
            permission_classes = [IsOwner,]

        elif self.action in [
            "update",
            "partial_update",
            "destroy",
            "restore",
            "inactive",
            "reset_password",
        ]:
            permission_classes = [IsOwnerOrAdmin,]

        else:
            permission_classes = [IsOwnerOrAdmin,]

        return [
            permission()
            for permission in permission_classes
        ]
        
    def get_serializer_class(self,):
        if self.action == "create":
            return UserCreateSerializer

        return UserSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()

        if not user.shop:
            user.shop = self.request.user.shop
            user.save()

        create_audit_log(
            user=self.request.user,
            action="CREATE",
            model_name="User",
            object_id=user.id,
            description=f"Created user {user.username}",
        )
        
    def perform_update(self, serializer,):
        user = serializer.save()

        create_audit_log(
            user=self.request.user,
            action="UPDATE",
            model_name="User",
            object_id=user.id,
            description=(
                f"Updated user "
                f"{user.username}"
            ),
        )
        
    def perform_destroy(self, instance,):
        instance.is_active = False
        instance.save()

        create_audit_log(
            user=self.request.user,
            action="DELETE",
            model_name="User",
            object_id=instance.id,
            description=(
                f"Deactivated user "
                f"{instance.username}"
            ),
        )
        
    @action(detail=False, methods=["get"],)
    def inactive(self, request,    ):
        users = User.objects.filter(
            shop=request.user.shop,
            is_active=False,
        )

        serializer = UserSerializer(users, many=True,)

        return Response(
            serializer.data
        )
    
    @action(detail=True, methods=["post"],)
    def restore(self, request, pk=None,):
        user = get_object_or_404(
            User,
            pk=pk,
            shop=request.user.shop,
            is_active=False,
        )

        user.is_active = True
        user.save()

        create_audit_log(
            user=request.user,
            action="RESTORE",
            model_name="User",
            object_id=user.id,
            description=(
                f"Restored user "
                f"{user.username}"
            ),
        )

        return Response(
            {
                "message":
                    "User restored successfully"
            }
        )
        
    @extend_schema(request=ResetPasswordSerializer,)
    @action(detail=True, methods=["post"],)
    def reset_password(self, request, pk=None,):
        user = get_object_or_404(
            User,
            pk=pk,
            shop=request.user.shop,
        )

        serializer = ResetPasswordSerializer(data=request.data,)
        serializer.is_valid(raise_exception=True,)

        user.set_password(
            serializer.validated_data[
                "new_password"
            ]
        )

        user.save()

        create_audit_log(
            user=request.user,
            action="PASSWORD_RESET",
            model_name="User",
            object_id=user.id,
            description=(
                f"Reset password for "
                f"{user.username}"
            ),
        )

        return Response(
            {
                "message":
                    "Password reset successfully."
            }
        )