# Generated by Django 2.0.6 on 2020-04-23 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0011_auto_20200423_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
    ]
