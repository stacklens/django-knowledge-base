`Django`  内置了开箱即用的 `User` 用户模型，但是很多时候难免满足不了实际的开发需求：比方说国内总喜欢收集用户的手机号，这就需要扩展内置 `User` 模型了。

扩展 `User` 模型的途径很多，重点介绍最常用的两种。

### 外链扩展

这种方式完全不改变 `User` 本身的结构，而是用 `OneToOneField` 将扩展字段链接起来，像这样：

```python
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    
    # And other fields you want...


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
```

代码中运用到了信号的概念，即每当 `User`调用 `save()` 方法时，都会自动调用下面的两个函数，从而确保每个 `User` 都对应了一个 `Profile`。如果你不想用信号，自己写逻辑保证它们的对应关系也是可以的，随便你。

这种方式的好处是不改变 `User` 本身的结构，做更改也很灵活。实现也较简单，容易理解。缺点是多了一个外链就多了一层查询，降低了效率。总的来说，一般的小网站对效率没有很高的要求，所以这种方法对大部分人是完全可以接受的。

### 扩展 AbstractUser

`AbstractUser` 其实就是 `User` 的父类抽象模型，它提供了默认 `User` 的全部实现。

这种方式扩展起来也不难：

```python
# models.py

from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    
    # And other fields you want...
```

然后你还要让 Django 知道你现在用的是自定义的模型了，所以要在 `settings.py` 里加上这句：

```python
# settings.py

# xxx 是你自定义的 app 的名称
AUTH_USER_MODEL = 'xxx.MyUser'
```

然后你就发现内置后台中的 `User` 入口消失了，并且普通的 `admin.site.register(MyUser)` 还有问题，即密码居然是用明文存储的。这是因为 Django 不知道应该怎么去处理自定义的模型。因此要改一下 `admin.py` 的注册方式：

```python
# admin.py

from django.contrib.auth.admin import UserAdmin

ADDITIONAL_FIELDS = ((None, {'fields': ('phone_number',)}),)

class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_FIELDS
    add_fieldsets = UserAdmin.fieldsets + ADDITIONAL_FIELDS

admin.site.register(MyUser, MyUserAdmin)
```

这段代码的意思就是说，我现在要注册的这个定制的 `MyUser` 基本沿用默认的实现，并且添加了扩展的字段。再回到后台中，可以看到密码已经哈希过了，并且扩展的字段也都能正常显示了。

这种方式的好处就是把所有字段都整合到同一个表中，并且还具有默认 `User` 的完全实现。缺点就是会很强的改变用户模型的结构，所以尽可能在项目开始时就谨慎考虑，谨慎使用。

> 本文参考了 [How to Extend Django User Model](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html)，文章中还介绍了代理模式扩展和 `AbstractBaseUser` 扩展，有兴趣的读者可以研究一下。