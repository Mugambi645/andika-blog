from rest_framework import permissions

from andika.content.models import Post


class PostVisibilityPermission(permissions.BasePermission):
    """Gate Post access by status, visibility, and requester identity.

    Write access (create/update/delete) is restricted to authors.
    Read access depends on the post's status and visibility:
    - status != published: only the post's own author may read it.
    - visibility == public: anyone may read it.
    - visibility == members: any authenticated member or author may read it.
    - visibility == paid: only an authenticated member with an active subscription, or the post's author, may read it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role == user.Role.AUTHOR
        )

    def has_object_permission(self, request, view, obj: Post):
        if request.method not in permissions.SAFE_METHODS:
            return bool(
                request.user.is_authenticated
                and request.user.role == request.user.Role.AUTHOR
            )

        user = request.user
        is_author_of_post = user.is_authenticated and obj.author_id == user.id

        if is_author_of_post:
            return True

        if obj.status != Post.Status.PUBLISHED:
            return False

        if obj.visibility == Post.Visibility.PUBLIC:
            return True

        if not user.is_authenticated:
            return False

        if obj.visibility == Post.Visibility.MEMBERS:
            return True

        if obj.visibility == Post.Visibility.PAID:
            return _has_active_subscription(user)

        return False


def _has_active_subscription(user) -> bool:
    from andika.memberships.models import Subscription

    return Subscription.objects.filter(
        member=user, status=Subscription.Status.ACTIVE
    ).exists()