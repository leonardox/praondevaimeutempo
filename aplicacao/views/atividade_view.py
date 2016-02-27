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

        lista_atividades = Atividade.objects.all()
        context = self.get_context_data(lista_atividades=lista_atividades)
        return self.render_to_response(context)

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
