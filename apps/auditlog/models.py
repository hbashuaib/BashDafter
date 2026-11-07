from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    ACTION_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("RESTORE", "Restore"),
        ("LOGIN", "Login"),
        ("PASSWORD_CHANGE", "Password Change"),
        ("PASSWORD_RESET", "Password Reset"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES,)
    model_name = models.CharField(max_length=100,)
    object_id = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return (
            f"{self.user} - "
            f"{self.action} - "
            f"{self.model_name}"
        )