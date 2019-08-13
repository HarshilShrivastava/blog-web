from django.contrib import admin
from .models import post
class PostModelAdmin(admin.ModelAdmin):
    list_display=["title","updated","timestamp"]
    list_display_links=["updated"]
    list_editable=["title"]
    list_filter=["updated","timestamp"]
    search_fields=["title","content"]
    class meta:
        model=post
# Register your models here.
admin.site.register(post,PostModelAdmin)