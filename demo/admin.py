from django.contrib import admin
from .models import Post, UUIDModel, Owner, Group, Person


admin.site.register(Post)
admin.site.register(UUIDModel)
admin.site.register(Owner)
admin.site.register(Group)
admin.site.register(Person)