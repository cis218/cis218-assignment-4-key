from django.db import models
from django.conf import settings
from django.urls import reverse


class Twit(models.Model):
    """A single Twit that a user creates"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="twits",
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="twits_liked",
        blank=True,
    )

    def __str__(self):
        return self.body[:30]

    def get_absolute_url(self):
        return reverse("twit_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("-created_at",)
