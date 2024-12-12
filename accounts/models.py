from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom User Model"""

    date_of_birth = models.DateField(null=True, blank=True)
