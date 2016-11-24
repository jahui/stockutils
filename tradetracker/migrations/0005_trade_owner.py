# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-24 20:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tradetracker', '0004_auto_20161118_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
