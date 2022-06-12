from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView

from .models import Twit


class TwitListView(LoginRequiredMixin, ListView):
    """Twit List View"""

    model = Twit
    template_name = "twit_list.html"


class TwitUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Twit Update View"""

    model = Twit
    template_name = "twit_edit.html"
    success_url = reverse_lazy("twit_list")
    fields = (
        "body",
        "image_url",
    )

    def test_func(self):
        """User passes test function authorization"""
        obj = self.get_object()
        return obj.user == self.request.user


class TwitDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Twit Delete View"""

    model = Twit
    template_name = "twit_delete.html"
    success_url = reverse_lazy("twit_list")

    def test_func(self):
        """User passes test function authorization"""
        obj = self.get_object()
        return obj.user == self.request.user


class TwitCreateView(LoginRequiredMixin, CreateView):
    """Twit Create View"""

    model = Twit
    template_name = "twit_new.html"
    success_url = reverse_lazy("twit_list")
    fields = (
        "body",
        "image_url",
    )

    def form_valid(self, form):
        """Form Valid"""
        form.instance.user = self.request.user
        return super().form_valid(form)
