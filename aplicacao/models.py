# -*- coding: utf-8 -*-
import base64

import django
from django.db import models


class Usuario(models.Model):
    """
    Esta classe representa um usuário
    """
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    foto = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)


class Atividade(models.Model):
    """
    Esta classe representa uma atividade
    """
    nome = models.CharField(max_length=50, null=False, default=None)
    tempo_investido = models.IntegerField()
    categoria = models.CharField(max_length=14, blank=True)
    data = models.DateField(default=django.utils.timezone.now)
    prioridade = models.BooleanField(default=False)
    user = models.ForeignKey(Usuario)
    foto = models.TextField(blank=True, null=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.nome == '':
            raise ValidationError('Empty error message')


class Tag(models.Model):
    nome_tag = models.CharField(max_length=14, blank=True)


class ATIVIDADE_TAG(models.Model):
    Atvidade_id = models.ForeignKey(Atividade)
    tag_id = models.ForeignKey(Tag)
