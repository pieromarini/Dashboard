# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-27 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashby', '0009_document_extension'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails'),
        ),
    ]
