from django.db import models


class Atividade(models.Model):
    """
    Esta classe representa uma atividade
    """
    nome = models.CharField(max_length=50)
    tempo_investido = models.IntegerField()
