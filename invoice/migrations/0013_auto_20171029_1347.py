# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-29 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0012_auto_20171029_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='person',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
