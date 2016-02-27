# -*- coding: utf-8 -*-
from django import forms


class FormAtividade(forms.Form):
    """
    Formulário de uma tividade
    """
    nome = forms.CharField(max_length=50)
    tempo_investido = forms.IntegerField()
    data = forms.DateField()
