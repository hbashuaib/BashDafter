from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view,):
        return request.user.is_authenticated and request.user.role == "OWNER"


class IsOwnerOrAdmin(BasePermission,):
    def has_permission(self, request, view,):
        return request.user.is_authenticated and request.user.role in [
            "OWNER",
            "ADMIN",
        ]


class IsManagerOrAbove(BasePermission,):
    def has_permission(self, request, view,):
        return request.user.is_authenticated and request.user.role in [
            "OWNER",
            "ADMIN",
            "MANAGER",
        ]

class IsCashierOrAbove(BasePermission,):
    def has_permission(self, request, view,):
        return (
            request.user.is_authenticated
            and request.user.role in [
                "OWNER",
                "ADMIN",
                "MANAGER",
                "CASHIER",
            ]
        )
