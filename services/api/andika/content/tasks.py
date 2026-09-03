from io import BytesIO
from celery import shared_task
from django.core.files.base import ContentFile
from PIL import Image
from django.utils import timezone

from .models import Post

RESPONSIVE_WIDTHS = [400, 800, 1200, 1600]


@shared_task
def compress_uploaded_image(post_id: int) -> None:
    """Generate compressed, responsive-width JPEG/WebP variants of a
    post's featured image after upload.

    Runs after the triggering request has already returned, so a slow
    Pillow resize never adds latency to the author-facing save call.
    """
    from andika.content.models import Post

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return

    if not post.featured_image:
        return

    original = Image.open(post.featured_image.path)
    original = original.convert("RGB")

    for width in RESPONSIVE_WIDTHS:
        if original.width < width:
            continue

        ratio = width / original.width
        height = int(original.height * ratio)
        resized = original.resize((width, height), Image.LANCZOS)

        for fmt, ext, save_kwargs in (
            ("JPEG", "jpg", {"quality": 78, "optimize": True}),
            ("WEBP", "webp", {"quality": 75, "method": 6}),
        ):
            buffer = BytesIO()
            resized.save(buffer, format=fmt, **save_kwargs)
            filename = f"posts/responsive/{post.slug}-{width}.{ext}"
            content = ContentFile(buffer.getvalue())
            post.featured_image.storage.save(filename, content)


@shared_task
def publish_scheduled_posts() -> int:
    """Flip any due scheduled post to published.
Idempotent: re-running this task when nothing is due does nothing,
and a post already published is never touched twice, so running it
slightly more often than necessary is harmless.
"""
    due = Post.objects.filter(
        status=Post.Status.SCHEDULED,
        published_at__lte=timezone.now(),
    )
    count = due.count()
    for post in due:
        post.status = Post.Status.PUBLISHED
        post.save(update_fields=["status"])
    return count

