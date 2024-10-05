# billing_system/authentication/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    phone_no = models.CharField(max_length=15, blank=True, null=True)  # Add this field
    # Other custom fields...

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change this to avoid conflicts
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Change this to avoid conflicts
        blank=True,
    )
