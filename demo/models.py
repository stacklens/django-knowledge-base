from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import F
from django.contrib.auth.models import User

import uuid


# 群组
class Group(models.Model):
    username = models.CharField(max_length=100)


# ForeignKey 桥接模型
class Owner(models.Model):
    # 个人
    person = models.OneToOneField(
        User,
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
