# -*- coding: utf-8 -*-
from django import forms


class FormAtividade(forms.Form):
    """
    Formulário de uma tividade
    """
    nome = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tempo_investido = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'type': 'number'}))
    foto = forms.FileField(label='Select a file',
                           help_text='max. 42 megabytes',
                           required=False)
    prioridade = forms.BooleanField(required=False)
    tags = forms.CharField(max_length=140, widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=False)
    user = forms.CharField(max_length=100, required=False)
