# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-16 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradetracker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trade',
            old_name='price_bought',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='trade',
            old_name='date_bought',
            new_name='trade_date',
        ),
        migrations.RemoveField(
            model_name='trade',
            name='date_sold',
        ),
        migrations.RemoveField(
            model_name='trade',
            name='price_sold',
        ),
        migrations.AddField(
            model_name='trade',
            name='trade_type',
            field=models.BooleanField(default=None),
        ),
    ]
