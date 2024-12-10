from django.urls import path

from .views import VoteDetailView, VoteView

urlpatterns = [
    path("", VoteView.as_view(), name="vote-list"),
    path("today/", VoteDetailView.as_view(), name="vote-detail"),
]
