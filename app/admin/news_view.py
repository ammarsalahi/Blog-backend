from django.contrib import admin
from app.models import NewsView


@admin.register(NewsView)
class NewsViewAdmin(admin.ModelAdmin):
    list_display= ('pk','created_at','updated_at')
    list_filter=('created_at','updated_at')
