# Generated by Django 2.0.6 on 2020-04-23 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0013_bird'),
    ]

    operations = [
        migrations.AddField(
            model_name='bird',
            name='age',
            field=models.TextField(default='5 years old'),
        ),
    ]
