from django.urls import path, include
from rest_framework.routers import DefaultRouter

from comments.views import CommentListView, CommentDetailView

urlpatterns = [
    path("comments/", CommentListView.as_view()),
    path("comments/<int:pk>/", CommentDetailView.as_view()),
]

