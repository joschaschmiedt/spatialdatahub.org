# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-22 08:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200, null=True)),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(null=True)),
                ('url', models.URLField(blank=True, max_length=500, null=True)),
                ('dataset_user', models.CharField(blank=True, max_length=500, null=True)),
                ('dataset_password', models.CharField(blank=True, max_length=500, null=True)),
                ('public_access', models.BooleanField(default=True)),
                ('owncloud', models.BooleanField(default=False)),
                ('owncloud_instance', models.CharField(blank=True, max_length=500, null=True)),
                ('owncloud_path', models.CharField(blank=True, max_length=500, null=True)),
                ('dataset_slug', models.SlugField(null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('ext', models.CharField(blank=True, default='geojson', max_length=12, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Account')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='dataset',
            unique_together=set([('account', 'title')]),
        ),
    ]
