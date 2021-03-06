# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-22 20:24
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='BudgetGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('goal_amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('progress', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budgetapp.Budget')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('spent', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budgetapp.Budget')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budgetapp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budgetapp.Budget')),
            ],
        ),
        migrations.CreateModel(
            name='LongTermGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('goal_amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('progress', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('due_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('recipient', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('category_budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budgetapp.CategoryBudget')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budgetapp.CategoryGroup'),
        ),
        migrations.AddField(
            model_name='budgetgoal',
            name='long_term_goal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='budgetapp.LongTermGoal'),
        ),
    ]
