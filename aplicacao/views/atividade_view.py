# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, FormView

from aplicacao.forms import FormAtividade
from aplicacao.models import Atividade


def index(request):
    return render_to_response('index.html')


class ListaAtividades(TemplateView):
    """
    Esta classe lista todas as atividades cadastradas.
    """
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        lista_atividades = Atividade.objects.all().order_by('-data')
        context = self.get_context_data(lista_atividades=lista_atividades)
        return self.render_to_response(context)


class AdicionarAtividade(FormView):
    """
    Esta classe adiciona uma nova atividade ao sistema
    """
    template_name = 'adicionar_atividade.html'
    form_class = FormAtividade
    success_url = '/'

    def post(self, request, *args, **kwargs):
        """
        Realiza tratamento da data antes da validação do formulário.
        """
        data = request.POST

        my_dict = {}
        for key in data:
            my_dict[key] = data[key]
        my_dict["data"] = _convert_date(my_dict["data"])
        form = FormAtividade(my_dict)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Este método adiciona uma nova atividade no banco de dados.
        """
        data = form.cleaned_data
        atividade = Atividade()
        atividade.nome = data['nome']
        atividade.tempo_investido = data['tempo_investido']
        atividade.data = data['data']
        atividade.save()

        return super(AdicionarAtividade, self).form_valid(form)


def _convert_date(date):
    """
    This method converts a date to american pattern.
    :param date: Date to be converted.
    :return: String Date in american pattern.
    """
    formats = ['%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y',
               '%Y/%m/%d', '%Y-%m-%d', '%y/%m/%d', '%y-%m-%d', '%m/%d/%Y']

    for format_date in formats:
        try:
            date = str(datetime.datetime.strptime(date, format_date).date())
            return date
        except ValueError:
            continue
    raise ValueError
