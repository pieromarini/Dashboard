# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-27 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashby', '0010_document_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='thumbnail',
            field=models.ImageField(blank=True, default='/home/piero/Development/WebApps/Dashboard/media/img/xlsx.png', null=True, upload_to='thumbnails'),
        ),
    ]
