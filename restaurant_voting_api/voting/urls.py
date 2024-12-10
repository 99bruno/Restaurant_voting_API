from django.urls import path
from .views import VoteView, VoteDetailView

urlpatterns = [
    path('', VoteView.as_view(), name='vote-list'),
    path('today/', VoteDetailView.as_view(), name='vote-detail'),
]
