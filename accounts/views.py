from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView

from .models import CustomUser

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    """Sign Up View"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Profile View"""

    model = CustomUser
    success_url = reverse_lazy("twit_list")
    template_name = "registration/profile.html"
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "date_of_birth",
    )

    def test_func(self):
        """User passes test function authorization"""
        obj = self.get_object()
        return obj == self.request.user


class PublicProfileView(LoginRequiredMixin, DetailView):
    """Public Profile View"""

    model = CustomUser
    template_name = "public_profile.html"
