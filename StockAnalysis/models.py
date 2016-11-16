# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Ohlc(models.Model):
    id = models.BigAutoField(primary_key=True)
    sec = models.ForeignKey('Security', models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'OHLC'


class Constituents(models.Model):
    index = models.ForeignKey('Indexes', models.DO_NOTHING, blank=True, null=True)
    sec = models.ForeignKey('Security', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'constituents'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Indexes(models.Model):
    index_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indexes'


class Security(models.Model):
    sec_name = models.CharField(max_length=255, blank=True, null=True)
    yahoo_ticker = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'security'


class TopPicks(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    sec = models.ForeignKey(Security, models.DO_NOTHING, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'top_picks'
