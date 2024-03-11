from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_captcha.serializers import RestCaptchaSerializer
from rest_framework.exceptions import ValidationError
from .models import Comment
from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    CommentCreateSerializer
)
from rest_framework.pagination import PageNumberPagination
import json


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'comments'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'list':
            await self.list_comments(text_data_json)
        elif action == 'create':
            await self.create_comment(text_data_json)
        elif action == 'detail':
            await self.get_comment_detail(text_data_json)
        else:
            await self.send(text_data=json.dumps({"non_field_errors": ["Invalid action"]}))

    async def list_comments(self, data):
        page = data.get('page', 1)
        paginator = self.get_paginator()
        comments = await self.get_comments(page, paginator)
        await self.send(text_data=json.dumps(comments))

    async def get_comment_detail(self, data):
        comment_id = data.get('comment_id')
        if comment_id:
            comment = await self.get_comment_by_id(comment_id)
            if comment:
                serializer = CommentDetailSerializer(comment)
                await self.send(text_data=json.dumps(serializer.data))
            else:
                await self.send(text_data=json.dumps({"non_field_errors": ["Comment not found"]}))
        else:
            await self.send(text_data=json.dumps({"non_field_errors": ["Comment ID not provided"]}))

    async def create_comment(self, data):
        captcha_data = data.get("captcha")
        if not RestCaptchaSerializer(data=captcha_data).is_valid():
            await self.send(text_data=json.dumps({"non_field_errors": ["Invalid captcha"]}))
            return
        try:
            comment_data = data.get('data', {})
            comment = await self.create_comment_instance(comment_data)
            serializer = CommentListSerializer(comment)
            await self.send(text_data=json.dumps(serializer.data))
        except ValidationError as e:
            await self.send(text_data=json.dumps(e.detail))

    def get_paginator(self):
        paginator = PageNumberPagination()
        paginator.page_size = 25
        return paginator

    @database_sync_to_async
    def get_comments(self, page, paginator):
        queryset = Comment.objects.all()
        result_page = paginator.paginate_queryset(queryset, page, self.scope)
        serialized_comments = CommentListSerializer(result_page, many=True).data
        return serialized_comments

    @database_sync_to_async
    def get_comment_by_id(self, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
            return comment
        except Comment.DoesNotExist:
            return None

    @database_sync_to_async
    def create_comment_instance(self, data):
        serializer = CommentCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()
