# Generated by Django 5.1.1 on 2024-11-11 07:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LaTavolaAplikazioa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='iritzia',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='iritzia',
            name='izarrak',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
    ]
