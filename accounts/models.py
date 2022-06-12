from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    """Custom User Model"""

    date_of_birth = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})
