from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Page, Post, Tag
from .permissions import PostVisibilityPermission, _has_active_subscription
from .serializers import (
    PageSerializer,
    PostSerializer,
    PostWriteSerializer,
    TagSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [PostVisibilityPermission]
    filterset_fields = ["status", "visibility", "language", "tags__slug"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return PostWriteSerializer
        return PostSerializer

    def get_queryset(self):
        qs = Post.objects.select_related("author").prefetch_related("tags")
        user = self.request.user

        if user.is_authenticated and user.role == user.Role.AUTHOR:
            return qs  # authors browse everything, incl. their drafts

        qs = qs.filter(status=Post.Status.PUBLISHED)

        if not user.is_authenticated:
            return qs.filter(visibility=Post.Visibility.PUBLIC)

        if _has_active_subscription(user):
            return qs  # members with active paid sub see everything

        return qs.exclude(visibility=Post.Visibility.PAID)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer