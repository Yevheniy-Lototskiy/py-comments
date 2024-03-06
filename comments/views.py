from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import Comment
from comments.serializers import (
    CommentListSerializer,
    CommentDetailSerializer, CommentCreateSerializer,
)


# class CustomPagination(PageNumberPagination):
#     page_size = 25
#     page_size_query_param = 'page_size'
#     max_page_size = 100


# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     pagination_class = CustomPagination
#     filter_backends = [DjangoFilterBackend]
#     filter_set_fields = ["username", "email", "pub_date"]
#
#     def get_queryset(self):
#         queryset = self.queryset
#
#         if self.action == "list":
#             queryset = queryset.filter(parent_comment__isnull=True)
#
#             # Filter by fields
#             sort_by = self.request.query_params.get("sort_by")
#             if sort_by:
#                 queryset = queryset.order_by(sort_by)
#
#         # Filter by values
#         username = self.request.query_params.get('username', None)
#         email = self.request.query_params.get('email', None)
#         pub_date = self.request.query_params.get('pub_date', None)
#
#         if username:
#             queryset = queryset.filter(username=username)
#         if email:
#             queryset = queryset.filter(email=email)
#         if pub_date:
#             queryset = queryset.filter(pub_date=pub_date)
#
#         return queryset
#
#     def get_serializer_class(self):
#         if self.action == "list":
#             return CommentListSerializer
#
#         if self.action == "update":
#             return CommentDetailSerializer
#
#         return CommentSerializer


class CommentListView(APIView):
    def get(self, request):
        # Filtering by parent_comment_id can be removed,
        # it is applied for cascading display in json format
        comments = Comment.objects.all().filter(parent_comment_id__isnull=True)
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def get_object(self, pk: int):
        return get_object_or_404(Comment, pk=pk)

    def get(self, request, pk: int):
        serializer = CommentDetailSerializer(self.get_object(pk=pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk: int):
        comment = Comment.objects.get(pk=pk)

        serializer = CommentDetailSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

