from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentListSerializer(CommentSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "username",
            "pub_date",
            "email",
            "homepage",
            "parent_comment",
            "text",
            "replies",
        )

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj)

        serializer = self.__class__(replies, many=True)

        return serializer.data
