from django.db import models


class Student(models.Model):
    """学生"""
    name = models.CharField(max_length=20)


class Info(models.Model):
    """学生的基本情况"""
    age = models.IntegerField()


class Address(models.Model):
    """学生的家庭住址"""
    home = models.CharField(max_length=100)
