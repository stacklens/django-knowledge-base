from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import F
from django.contrib.auth.models import User

from djangoKnowledgeBase.settings import AUTH_USER_MODEL

import uuid

# from django.db.models.signals import post_save
# from django.dispatch import receiver

# MARK: - User 扩展 1
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=20)
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


from django.contrib.auth.models import AbstractUser


# MARK: - User 扩展 2
class MyUser(AbstractUser):
    phone_number = models.CharField(max_length=20)


# 群组
class Group(models.Model):
    username = models.CharField(max_length=100)


# ForeignKey 桥接模型
class Owner(models.Model):
    # 个人
    person = models.OneToOneField(
        AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    # 群组
    group = models.OneToOneField(
        Group,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='owner'
    )

    def get_owner(self):
        # 获取非空 Owner 对象
        if self.person is not None:
            return self.person
        elif self.group is not None:
            return self.group
        raise AssertionError("Neither is set")

    def __str__(self):
        if self.person is not None:
            return self.person.username
        elif self.group is not None:
            return self.group.username
        else:
            return 'No owner here..'


class Post(models.Model):
    # MARK: - ForeignKey 对多个对象
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='posts')

    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)

    views = models.IntegerField(default=0)

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('demo:detail', args=(self.id,))

    def increase_view(self):
        # MARK: - F()
        # self.views += 1
        self.views = F('views') + 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title


# MARK: - UUID
class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    content = models.TextField(default='uuid demo content')

    def __str__(self):
        return self.id


# MARK: - @property
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def full_name_with_midname(self, midname):
        return f"{self.first_name} {midname} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


# MARK: - Model 的继承 - 抽象基类
class Animal(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=5)
    finger_count = models.IntegerField(default=10)

    class Meta:
        abstract = True


class Bird(Animal):
    flying_height = models.IntegerField(default=2000)
    age = models.TextField(default='5 years old')
    finger_count = None


# MARK: - Model 的继承 - 多表继承
class Human(models.Model):
    name = models.CharField(max_length=100)


class Baby(Human):
    age = models.IntegerField(default=0)
    human_ptr = models.OneToOneField(
        Human, on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
    )


# MARK: - Model 的继承 - 代理模式
class Car(models.Model):
    name = models.CharField(max_length=30)


class MyCar(Car):
    class Meta:
        ordering = ["name"]
        proxy = True

    def do_something(self):
        # ...
        pass


# MARK: - F 函数
class Age(models.Model):
    year = models.IntegerField(default=6)
    month = models.IntegerField(default=10)