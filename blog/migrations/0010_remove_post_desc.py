# Generated by Django 2.2.5 on 2020-03-15 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='desc',
        ),
    ]
