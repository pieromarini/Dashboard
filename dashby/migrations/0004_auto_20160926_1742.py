# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashby', '0003_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to='/'),
        ),
    ]
