# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-02 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacao', '0002_atividade_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividade',
            name='categoria',
            field=models.CharField(default='LAZER', max_length=14),
            preserve_default=False,
        ),
    ]