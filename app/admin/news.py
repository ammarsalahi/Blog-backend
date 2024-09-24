from django.contrib import admin
from app.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display= ('title','created_at','updated_at')
    list_filter=('created_at','updated_at')
    search_fields = ("title","description")