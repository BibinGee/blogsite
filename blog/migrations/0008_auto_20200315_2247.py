# Generated by Django 2.2.5 on 2020-03-15 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200315_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title_image',
            field=models.ImageField(default='title_images/default.png', upload_to='title_images'),
        ),
    ]
