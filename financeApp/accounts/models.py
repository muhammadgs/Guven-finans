from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # İstersen ekstra alanlar:
    # role = models.CharField(max_length=20, choices=[('company','Company'),('employee','Employee'),('admin','Admin')], default='company')
    pass