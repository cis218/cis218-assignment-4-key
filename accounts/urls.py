from django.urls import path

from .views import SignUpView, ProfileView, PublicProfileView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("public_profile/<int:pk>", PublicProfileView.as_view(), name="public_profile"),
]
