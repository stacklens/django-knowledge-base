from django.contrib import admin
from .models import Post, UUIDModel, Owner, Group


admin.site.register(Post)
admin.site.register(UUIDModel)
admin.site.register(Owner)
admin.site.register(Group)