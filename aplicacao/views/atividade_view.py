from django.shortcuts import render_to_response
from django.views.generic import TemplateView, FormView

from aplicacao.forms import FormAtividade
from aplicacao.models import Atividade
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.template.defaulttags import register

import datetime

def index(request):
    return render_to_response('index.html')


class ListaAtividades(TemplateView):
    """
    Esta classe lista todas as atividades cadastradas.
    """
    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    template_name = 'dashboard.html'
    one_day = datetime.timedelta(days=1)
    def get_week(self, date):
          day_idx = (date.weekday() + 1) % 7  # turn sunday into 0, monday into 1, etc.
          sunday = date - datetime.timedelta(days=day_idx)
          date = sunday
          for n in xrange(7):
            yield date
            date += self.one_day


    def get(self, request, *args, **kwargs):
        current_week = [d.isoformat() for d in self.get_week(datetime.datetime.now().date())]
        converted = list(map(DateFormat, current_week))
        print current_week
        lista_atividades_semana = Atividade.objects.filter(data='2016-03-01')
        print lista_atividades_semana
        lista_atividades = Atividade.objects.all()
        page_data = {
            'lista_atividades' : lista_atividades,
            'lista_atividades_semana' : lista_atividades_semana
        }
        context = self.get_context_data(page_data=page_data)
        return self.render_to_response(page_data)

class AdicionarAtividade(FormView):
    """
    Esta classe adiciona uma nova atividade ao sistema
    """
    template_name = 'adicionar_atividade.html'
    form_class = FormAtividade
    success_url = '/'


    def form_valid(self, form):
        data = form.cleaned_data
        atividade = Atividade()
        atividade.nome = data['nome']
        atividade.tempo_investido = data['tempo_investido']
        atividade.data = data['data']
        atividade.save()

        return super(AdicionarAtividade, self).form_valid(form)
