# Generated by Django 2.2.5 on 2020-03-15 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_post_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title_image',
            field=models.ImageField(default='title_images/default.png', upload_to='title_images'),
        ),
    ]
