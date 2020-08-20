from django.contrib import admin
from scrap.models import Post

# Register your models here.
class AdminPost(admin.ModelAdmin):
    list_display=['title','status']
admin.site.register(Post,AdminPost)
