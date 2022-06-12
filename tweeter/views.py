from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView

from .models import Twit


class TwitListView(ListView):
    """Twit List View"""

    model = Twit
    template_name = "twit_list.html"


class TwitUpdateView(UpdateView):
    """Twit Update View"""

    model = Twit
    template_name = "twit_edit.html"
    success_url = reverse_lazy("twit_list")
    fields = (
        "body",
        "image_url",
    )


class TwitDeleteView(DeleteView):
    """Twit Delete View"""

    model = Twit
    template_name = "twit_delete.html"
    success_url = reverse_lazy("twit_list")


class TwitCreateView(CreateView):
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
