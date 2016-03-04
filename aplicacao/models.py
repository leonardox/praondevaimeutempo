import django
from django.db import models


class Atividade(models.Model):
    """
    Esta classe representa uma atividade
    """
    nome = models.CharField(max_length=50)
    tempo_investido = models.IntegerField()
    categoria = models.CharField(max_length=14)
    data = models.DateField(default=django.utils.timezone.now)
    prioridade = models.BooleanField(default=False)
