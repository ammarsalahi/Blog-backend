from django.contrib import admin
from app.models import LinkBlog


@admin.register(LinkBlog)
class LinkBlogAdmin(admin.ModelAdmin):
    list_display= ('pk','created_at','updated_at')
    list_filter=('created_at','updated_at')
