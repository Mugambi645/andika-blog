from django.contrib import admin

# Register your models here.
from .models import Page, Post, Tag
admin.site.register(Tag)
admin.site.register(Page)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "visibility", "author", "published_at")
    list_filter = ("status", "visibility", "language")
    search_fields = ("title", "body_markdown")