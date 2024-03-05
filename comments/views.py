from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
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
    filter_backends = [DjangoFilterBackend]
    filter_set_fields = ["username", "email", "pub_date"]

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.filter(parent_comment__isnull=True)

            # Filter by fields
            sort_by = self.request.query_params.get("sort_by")
            if sort_by:
                queryset = queryset.order_by(sort_by)

        # Filter by values
        username = self.request.query_params.get('username', None)
        email = self.request.query_params.get('email', None)
        pub_date = self.request.query_params.get('pub_date', None)

        if username:
            queryset = queryset.filter(username=username)
        if email:
            queryset = queryset.filter(email=email)
        if pub_date:
            queryset = queryset.filter(pub_date=pub_date)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer

        if self.action == "update":
            return CommentDetailSerializer

        return CommentSerializer
