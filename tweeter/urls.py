from django.urls import path

from .views import (
    TwitDetailCommentCreateView,
    TwitCreateView,
    TwitDeleteView,
    TwitListView,
    TwitUpdateView,
)


urlpatterns = [
    path(
        "<int:pk>/comment/new",
        TwitDetailCommentCreateView.as_view(),
        name="comment_new",
    ),
    path("<int:pk>/edit/", TwitUpdateView.as_view(), name="twit_edit"),
    path("<int:pk>/delete/", TwitDeleteView.as_view(), name="twit_delete"),
    path("new/", TwitCreateView.as_view(), name="twit_new"),
    path("", TwitListView.as_view(), name="twit_list"),
]
