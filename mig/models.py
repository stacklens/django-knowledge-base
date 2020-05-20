from django.db import models
from django.utils import timezone


class Pen(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2)
    color = models.CharField(default='black', max_length=20)
    purchase_date = models.DateTimeField(default=timezone.now)
    # 手动删除 0003 文件后，添加此字段
    # length = models.IntegerField(default=10)