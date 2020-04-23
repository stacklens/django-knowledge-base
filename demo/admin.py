from django.contrib import admin
from .models import Post, UUIDModel, Owner, Group, Person, Human, Baby, MyCar


admin.site.register(Post)
admin.site.register(UUIDModel)
admin.site.register(Owner)
admin.site.register(Group)
admin.site.register(Person)
admin.site.register(Human)
admin.site.register(Baby)
admin.site.register(MyCar)