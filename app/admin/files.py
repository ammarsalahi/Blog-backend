from django.contrib import admin
from app.models import FileBlog


@admin.register(FileBlog)
class FileBlogAdmin(admin.ModelAdmin):
    list_display= ('pk','created_at','updated_at')
    list_filter=('created_at','updated_at')
