from rest_framework import serializers
from .models import Page, Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author_display_name = serializers.CharField(
        source="author.display_name", read_only=True
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "body_html",
            "status",
            "visibility",
            "published_at",
            "author",
            "author_display_name",
            "tags",
            "featured_image",
            "language",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "body_html", "author"]


class PostWriteSerializer(serializers.ModelSerializer):
    """Used for create/update, where body_markdown is the input field."""

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "body_markdown",
            "status",
            "visibility",
            "published_at",
            "tags",
            "featured_image",
            "language",
        ]


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["id", "title", "slug", "body_html", "updated_at"]
        read_only_fields = ["slug", "body_html"]