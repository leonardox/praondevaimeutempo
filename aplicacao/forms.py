# -*- coding: utf-8 -*-
from django import forms


class FormAtividade(forms.Form):
    """
    Formulário de uma tividade
    """
    ESPORTE_SAUDE = 'ESPORTE/SAÚDE'
    ESTUDOS = 'ESTUDOS'
    LAZER = 'LAZER'
    TRABALHO = 'TRABALHO'

    nome = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tempo_investido = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'type': 'number'}))
    data = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'max-length': '50'}))
    foto = forms.FileField(label='Select a file',
                           help_text='max. 42 megabytes',
                           required=False)
    prioridade = forms.BooleanField(required=False)
    user = forms.CharField(max_length=100, required=False)
    nome_tag = forms.CharField(required=False)
