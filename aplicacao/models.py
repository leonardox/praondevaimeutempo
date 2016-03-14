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
    nome = models.CharField(max_length=50)
    tempo_investido = models.IntegerField()
    categoria = models.CharField(max_length=14)
    data = models.DateField(default=django.utils.timezone.now)
    prioridade = models.BooleanField(default=False)
    user = models.ForeignKey(Usuario)
    _foto = models.TextField(blank=True)

    def set_foto(self, foto):
        self._foto = base64.encodestring(foto)

    def get_foto(self):
        return base64.decodestring(self._foto)
    foto = property(get_foto, set_foto)
