# Generated by Django 3.0.5 on 2020-05-11 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0003_files'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Files',
            new_name='File',
        ),
    ]
