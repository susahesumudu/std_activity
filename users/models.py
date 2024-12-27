from django.db import models

# Create your models here.from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    # Link this Profile model to the User model
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Add a gender field to the profile
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),  # Optional for other gender choices
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    certificate_no = models.IntegerField(null=True, blank=True)
    is_Certificate_issued = models.BooleanField(null=True, blank=True)
    is_payment_completed = models.BooleanField(null=True, blank=True)
    certificate = models.ImageField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    final_marks = models.IntegerField(null=True, blank=True)
    module_marks= models.IntegerField(null=True, blank=True)
    task_marks = models.IntegerField(null=True, blank=True)
    completed_total_mod =  models.IntegerField(null=True, blank=True)
    completed_total_task =  models.IntegerField(null=True, blank=True)
    completed_total_activity =  models.IntegerField(null=True, blank=True)
    is_completed_total_tasks = models.BooleanField(null=True, blank=True)
    industry_experiance = models.IntegerField(null=True, blank=True)
    
    
    
    
    def __str__(self):
        return f'{self.user.username} Profile'
    


