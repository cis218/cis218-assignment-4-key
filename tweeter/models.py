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
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_twits",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:30]

    def get_absolute_url(self):
        return reverse("twit_detail", kwargs={"pk": self.pk})

    def get_like_url(self):
        """Get like url based on pk"""
        return reverse("twit_like", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("-created_at",)


class Comment(models.Model):
    """A single Comment on a Twit"""

    twit = models.ForeignKey(
        Twit,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("twit_list")

    class Meta:
        ordering = ("created_at",)
