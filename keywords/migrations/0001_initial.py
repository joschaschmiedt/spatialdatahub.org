# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('datasets', '0012_auto_20170412_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=100, unique=True)),
                ('datasets', models.ManyToManyField(to='datasets.Dataset')),
            ],
        ),
    ]