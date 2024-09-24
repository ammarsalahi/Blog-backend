from django.contrib import admin
from accounts.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =('full_name','is_superuser','is_staff','created_at','updated_at')
    list_filter = ('is_superuser','is_staff','created_at','updated_at')
    search_fields = ('first_name','last_name','username','email')
