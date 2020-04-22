from django.db import models
from django.utils import timezone
from django.urls import reverse

import uuid


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('demo:detail', args=(self.id,))

    def __str__(self):
        return self.title


# MARK: - UUID
class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    content = models.TextField(default='uuid demo content')

    def __str__(self):
        return self.id
