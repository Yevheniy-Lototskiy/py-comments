from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from comments.models import Comment
from comments.serializers import (
    CommentSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
)


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.filter(parent_comment__isnull=True)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer

        if self.action == "update":
            return CommentDetailSerializer

        return CommentSerializer
