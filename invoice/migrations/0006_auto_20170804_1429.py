# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-04 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_auto_20170804_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='invoice_accent_color',
            field=models.CharField(blank=True, help_text='Colour in hex', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='invoice_background_color',
            field=models.CharField(blank=True, help_text='Colour in hex', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='invoice_primary_color',
            field=models.CharField(blank=True, help_text='Colour in hex', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='invoice_secondary_color',
            field=models.CharField(blank=True, help_text='Colour in hex', max_length=10, null=True),
        ),
    ]