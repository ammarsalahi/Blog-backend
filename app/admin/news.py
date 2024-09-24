from django.contrib import admin

@admin.register()
class NewsAdmin(admin.ModelAdmin):
    list_display= ('title','released_at','created_at','updated_at')
    list_filter=('released_at','created_at','updated_at')
    search_fields = ("title","description")