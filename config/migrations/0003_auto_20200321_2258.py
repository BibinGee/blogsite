# Generated by Django 2.2.5 on 2020-03-21 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_dailyvisitstatistic_ipstatistic_visitstatistic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitstatistic',
            name='visit_number',
            field=models.PositiveIntegerField(default=0, verbose_name='访问总数'),
        ),
    ]
