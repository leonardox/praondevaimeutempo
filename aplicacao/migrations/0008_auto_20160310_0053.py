# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-10 00:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacao', '0007_auto_20160309_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='foto',
            field=models.ImageField(upload_to=b'praondevaimeutempo/static/profiles'),
        ),
    ]