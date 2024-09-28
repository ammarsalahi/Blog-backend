from django.contrib import admin
from app.models import Timer

@admin.register(Timer)
class TimerAdmin(admin.ModelAdmin):
    list_display=('publish_date','created_at')
    list_filter=('created_at','updated_at')
