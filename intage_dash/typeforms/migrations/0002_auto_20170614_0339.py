# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-14 03:39
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('typeforms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeform',
            name='payload',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'data': ''}),
        ),
    ]