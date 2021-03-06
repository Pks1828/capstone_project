# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 03:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constituents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'db_table': 'constituents',
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'django_migrations',
            },
        ),
        migrations.CreateModel(
            name='Indexes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'indexes',
            },
        ),
        migrations.CreateModel(
            name='Ohlc',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('open', models.FloatField(blank=True, null=True)),
                ('high', models.FloatField(blank=True, null=True)),
                ('low', models.FloatField(blank=True, null=True)),
                ('close', models.FloatField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'OHLC',
            },
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sec_name', models.CharField(blank=True, max_length=255, null=True)),
                ('yahoo_ticker', models.CharField(blank=True, max_length=25, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'security',
            },
        ),
        migrations.CreateModel(
            name='TopPicks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'top_picks',
            },
        ),
    ]
