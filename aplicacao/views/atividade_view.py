from django.shortcuts import render_to_response
from django.views.generic import TemplateView

from aplicacao.models import Atividade


def index(request):
    return render_to_response('index.html')


class ListaAtividades(TemplateView):
    """
    Esta classe lista todas as atividades cadastradas.
    """
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        atividade = Atividade()

        atividade.nome = "programar"
        atividade.tempo_investido = 2
        atividade.save()
        lista_atividades = Atividade.objects.all()
        context = self.get_context_data(lista_atividades=lista_atividades)
        return self.render_to_response(context)
