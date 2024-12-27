from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    email_verified = models.BooleanField(default=False)

    # Add custom related_name arguments
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Custom related_name for groups
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Custom related_name for permissions
        blank=True,
    )
