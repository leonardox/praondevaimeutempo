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

    CATEGORIA = (("ESPORTE/SAÚDE", ESPORTE_SAUDE), ('ESTUDOS', ESTUDOS), ('LAZER', LAZER),
                 ('TRABALHO', TRABALHO))
    nome = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tempo_investido = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'type': 'number'}))
    categoria = forms.ChoiceField(choices=CATEGORIA,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    data = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'max-length': '50'}))

    prioridade = forms.BooleanField(required=False)
