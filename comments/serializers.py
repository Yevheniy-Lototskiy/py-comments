from rest_framework import serializers

from comments.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    # Shows all comments that have the parent_comment_id of this comment
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


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = (
            "username",
            "email",
            "pub_date",
            "homepage",
            "parent_comment",
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "username",
            "email",
            "homepage",
            "text",
            "parent_comment",
        )
