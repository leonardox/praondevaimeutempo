# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-15 18:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacao', '0003_atividade__foto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='atividade',
            old_name='_foto',
            new_name='foto',
        ),
    ]