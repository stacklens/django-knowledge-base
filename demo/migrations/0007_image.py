# Generated by Django 3.0.5 on 2020-05-11 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0006_delete_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/%Y%m%d')),
            ],
        ),
    ]
