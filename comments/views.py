from rest_captcha.serializers import RestCaptchaSerializer
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import Comment
from comments.serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    CommentCreateSerializer,
)


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


class CommentListView(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        # Filtering by parent_comment_id can be removed,
        # it is applied for cascading display in json format
        comments = Comment.objects.all().filter(parent_comment_id__isnull=True)

        # Filtering objects by fields
        sort_by = request.query_params.get("sort_by")
        if sort_by:
            comments = comments.order_by(sort_by)

        # Filtering objects by values
        username = request.query_params.get("username")
        if username:
            comments = comments.filter(username=username)

        email = request.query_params.get("email")
        if email:
            comments = comments.filter(email=email)

        pub_date = request.query_params.get("pub_date")
        if pub_date:
            comments = comments.filter(pub_date=pub_date)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(comments, request)
        serializer = CommentListSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        captcha = request.data.get("captcha")

        if not RestCaptchaSerializer(data=captcha).is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Invalid captcha value'"},
            )

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

        comment = self.get_object(pk=pk)
        serializer = CommentDetailSerializer(comment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int):
        comment = self.get_object(pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
