from django.test import TestCase
import pytest
# Create your tests here.
from andika.accounts.models import User
from andika.content.models import Post

@pytest.mark.django_db
class test_post_slug_is_generated_from_title():
    author = User.objects.create_user(
        username="testuser", password="x", role=User.Role.AUTHOR
    )
    post = Post.objects.create(
        title="My First Post on Andika", body_markdown="Hello", author=author
    )
    assert post.slug == "my-first-post-on-andika"