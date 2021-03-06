# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-22 23:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0011_auto_20170422_1619'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterUniqueTogether(
            name='categorybudgetgroup',
            unique_together=set([('owner', 'name', 'budget')]),
        ),
    ]
