from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        AUTHOR = "author", "Author"
        MEMBER = "member", "Member"

    role = models.CharField(
        max_length=16, choices=Role.choices, default=Role.MEMBER
    )

    # Author-facing profile fields. Blank for members.
    display_name = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True
    )

    def __str__(self) -> str:
        return self.display_name or self.username


    