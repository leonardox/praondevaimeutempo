# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, FormView
from aplicacao.forms import FormAtividade
from aplicacao.models import Atividade
import operator


def index(request):
    return render_to_response('index.html')


class ListaAtividades(TemplateView):
    """
    Esta classe lista todas as atividades cadastradas.
    """

    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        lista_atividades = _get_atividades_semana_atual()
        context = self.get_context_data(
            lista_atividades=lista_atividades,
        )
        return self.render_to_response(context)


class AdicionarAtividade(FormView):
    """Atividade.objects.all().order_by('-data')
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
        atividade.categoria = data['categoria']
        atividade.data = data['data']
        atividade.prioridade = data['prioridade']
        atividade.save()

        return super(AdicionarAtividade, self).form_valid(form)


class RelatorioSemanal(TemplateView):
    """
    Esta classe exibe o relatório semanal
    """
    template_name = 'relatorio_semanal.html'

    def get(self, request, *args, **kwargs):
        resumo, total_horas, total_prioritarias = _get_resume(_get_atividades_semana_atual())
        context = self.get_context_data(resumo=resumo, total_hotas=total_horas,
                                        total_prioritarias=total_prioritarias)
        return self.render_to_response(context)


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


def _get_atividades_semana_atual():
    date = datetime.date.today()
    if date.day == date.weekday():
        start_week = date
    else:
        start_week = date - datetime.timedelta(date.weekday() + 1)

    end_week = start_week + datetime.timedelta(6)
    return Atividade.objects.filter(data__range=[start_week, end_week])


def _get_resume(activity_list):
    resume_dict = {}
    total_horas = 0
    total_prioritarias = 0
    for activity in activity_list:
        if activity.prioridade:
            total_prioritarias += activity.tempo_investido
        if activity.categoria in resume_dict:
            resume_dict[activity.categoria] += activity.tempo_investido
            total_horas += activity.tempo_investido
        else:
            resume_dict[activity.categoria] = activity.tempo_investido
            total_horas += activity.tempo_investido

    return sorted(resume_dict.items(), key=operator.itemgetter(1), reverse=True), total_horas, \
           total_prioritarias
