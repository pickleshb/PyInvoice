# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-05 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0006_auto_20170804_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='invoice_logo',
            field=models.ImageField(blank=True, null=True, upload_to='invoice_logos'),
        ),
    ]
