# -*- coding: utf-8 -*-
from django import forms


class FormAtividade(forms.Form):
    """
    Formulário de uma tividade
    """

    nome = forms.CharField(max_length=50, widget= forms.TextInput(attrs={'class':'form-control'}))
    tempo_investido = forms.IntegerField(widget= forms.TextInput(attrs={'class':'form-control'}))
    data = forms.DateField(widget= forms.TextInput(attrs={'class':'form-control', 'max-length':'50'}))

