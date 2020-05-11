from django.contrib import admin
from .models import Post, UUIDModel, Owner, Group, Person, Human, Baby, MyCar, MyUser, Age

from django.contrib.auth.admin import UserAdmin

ADDITIONAL_FIELDS = ((None, {'fields': ('phone_number',)}),)


class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_FIELDS
    add_fieldsets = UserAdmin.fieldsets + ADDITIONAL_FIELDS


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Post)
admin.site.register(UUIDModel)
admin.site.register(Owner)
admin.site.register(Group)
admin.site.register(Person)
admin.site.register(Human)
admin.site.register(Baby)
admin.site.register(MyCar)
admin.site.register(Age)
