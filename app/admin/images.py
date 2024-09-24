from django.contrib import admin
from app.models import ImageBlog


@admin.register(ImageBlog)
class ImageBlogAdmin(admin.ModelAdmin):
    list_display= ('pk','created_at','updated_at')
    list_filter=('created_at','updated_at')
