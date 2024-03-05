from rest_framework import viewsets

from comments.models import Comment
from comments.serializers import CommentSerializer, CommentListSerializer, CommentDetailSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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
