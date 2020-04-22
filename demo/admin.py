from django.contrib import admin
from .models import Post, UUIDModel


admin.site.register(Post)
admin.site.register(UUIDModel)