# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-22 15:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0009_auto_20170226_1204'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='budget',
            unique_together=set([('owner', 'month', 'year')]),
        ),
    ]
