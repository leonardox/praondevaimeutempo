# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-09 23:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacao', '0006_atividade_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='foto_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='foto',
            field=models.ImageField(upload_to=b'profiles'),
        ),
    ]