# Generated by Django 2.2.5 on 2020-03-15 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20200315_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='desc',
            field=models.CharField(blank=True, max_length=1024, verbose_name='摘要'),
        ),
    ]
