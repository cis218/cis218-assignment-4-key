from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView

from .models import CustomUser

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    """Sign Up View"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ProfileView(LoginRequiredMixin, UpdateView):
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
