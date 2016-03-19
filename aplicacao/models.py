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


class Tag(models.Model):
    """
    Esta classe representa uma tag cadastrada pelo usuário
    """
    nome = models.CharField(max_length=140)
    atividade = models.ForeignKey(Atividade)
    usuario = models.ForeignKey(Usuario)

