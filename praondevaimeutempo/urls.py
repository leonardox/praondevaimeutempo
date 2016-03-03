from django.conf.urls import include, url
from django.contrib import admin

from aplicacao.views.atividade_view import ListaAtividades, AdicionarAtividade, RelatorioSemanal

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # URLs das atividades
    url(r'^$', ListaAtividades.as_view(), name='atividades'),
    url(r'^atividade/add$', AdicionarAtividade.as_view(), name='adicionar-atividade'),
    url(r'^atividades/relatorio/semanal$', RelatorioSemanal.as_view(), name='relatorio-semanal'),
]
