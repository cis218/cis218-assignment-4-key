from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView

from tweeter.forms import CommentForm

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


class CommentCreateGetView(DetailView):
    """Comment Create View"""

    model = Twit
    template_name = "comment_new.html"
    context_object_name = "twit"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentCreatePostView(SingleObjectMixin, FormView):
    """Comment Create Post View"""

    model = Twit
    form_class = CommentForm
    template_name = "comment_new.html"
    context_object_name = "twit"

    def post(self, request, *args, **kwargs):
        """Post request"""
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """Form Valid"""
        comment = form.save(commit=False)
        comment.twit = self.object
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Get success Url"""
        return reverse("twit_list")


class TwitDetailCommentCreateView(LoginRequiredMixin, View):
    """Twit Detail / Comment Create View"""

    def get(self, request, *args, **kwargs):
        """Get request"""
        view = CommentCreateGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post request"""
        view = CommentCreatePostView.as_view()
        return view(request, *args, **kwargs)


class TwitLikeView(LoginRequiredMixin, View):
    """Article Like View"""

    def get(self, request, *args, **kwargs):
        """GET Request"""

        # Get out the data from the GET request
        twit_id = request.GET.get("twit_id", None)
        twit_action = request.GET.get("twit_action", None)

        if not twit_id or not twit_action:
            return JsonResponse(
                {
                    "success": False,
                }
            )

        twit = Twit.objects.get(id=twit_id)
        if twit_action == "like":
            # Do like stuff
            twit.likes.add(request.user)
        else:
            # Do unlike stuff
            twit.likes.remove(request.user)

        return JsonResponse(
            {
                "success": True,
            }
        )
