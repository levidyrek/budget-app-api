# Generated by Django 2.1.2 on 2019-02-12 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0025_rename_recipient_payee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budgetcategory',
            name='spent',
        ),
    ]
