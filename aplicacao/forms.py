from django import forms
from models import Atividade


class FormAtividade(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ("nome", "tempo_investido", "data")
