from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    uid = models.CharField(primary_key=True, editable=False, max_length=36)