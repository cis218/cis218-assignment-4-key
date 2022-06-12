from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Custom User Creation Form"""

    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            "username",
            "email",
            "date_of_birth",
        )


class CustomUserChangeForm(UserChangeForm):
    """Custom User Change Form"""

    class Meta(UserChangeForm):
        model = CustomUser
        fields = (
            "username",
            "email",
            "date_of_birth",
        )
