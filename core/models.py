from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICE = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICE)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    workplace = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    language_preference = models.CharField(max_length=10, default='uz')
    bot_token = models.CharField(max_length=255, blank=True, null=True)
    manually_created = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"
