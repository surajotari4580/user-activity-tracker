from email.policy import default
from sre_constants import SUCCESS
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

CREATE, READ, UPDATE, DELETE = "Create", "Read", "Update", "Delete"
LOGIN, LOGOUT, LOGIN_FAILED = "Login", "Logout", "Login_FAILLED"

ACTION_TYPES = [
    (CREATE, "CREATE"),
    (READ, "READ"),
    (UPDATE, "UPDATE"),
    (DELETE, "DELETE"),
    (LOGIN, "LOGIN"),
    (LOGOUT, "LOGOUT"),
    (LOGIN_FAILED, "Login_FAIL"),
    ]

SUCCESS, FAILED = "Success", "Failed"
ACTION_STATUS =  [(SUCCESS, SUCCESS), (FAILED, FAILED)]


class Activity_tracker_logs(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    action_type = models.CharField(choices=ACTION_TYPES, max_length=20)
    action_time = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(choices=ACTION_STATUS, max_length=10, default=SUCCESS)
    data = models.JSONField(default=dict)
    
    content_type = models.ForeignKey(ContentType, models.SET_NULL, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()
    
    def __str__(self) -> str:
        return f"{self.action_type} by {self.member} on {self.action_time}"