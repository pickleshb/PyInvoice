# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-16 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_auto_20170416_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='utr',
            field=models.BooleanField(default=False),
        ),
    ]