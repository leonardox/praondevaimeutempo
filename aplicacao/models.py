# -*- coding: utf-8 -*-
import os
import urllib

import django
from django.core.files import File
from django.db import models


class Usuario(models.Model):
    """
    Esta classe representa um usuário
    """
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    foto = models.ImageField(upload_to='praondevaimeutempo/static/profiles')
    foto_url = models.URLField(blank=True)
    user_id = models.CharField(max_length=100)

    @staticmethod
    def create(nome, email, foto_url, user_id):
        usuario = Usuario()
        if foto_url and not usuario.foto:

            result = urllib.urlretrieve(foto_url)
            usuario.foto.save(
                os.path.basename(foto_url),
                File(open(result[0]))
            )
        usuario.nome = nome
        usuario.email = email
        usuario.foto_url = foto_url
        usuario.user_id = user_id
        usuario.save()
        return usuario


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
