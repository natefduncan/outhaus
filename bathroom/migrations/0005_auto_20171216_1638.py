# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-16 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bathroom', '0004_auto_20171216_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restroom',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='restroom',
            name='lng',
            field=models.FloatField(default=0),
        ),
    ]
