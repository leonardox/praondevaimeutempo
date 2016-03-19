from django.conf.urls import include, url
from django.contrib import admin

from aplicacao.views import atividade_view
from aplicacao.views.atividade_view import ListaAtividades, AdicionarAtividade, RelatorioSemanal, \
    LoginView, ComparaSemanas

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # URLs das atividades
    url(r'^$', ListaAtividades.as_view(), name='atividades'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^atividade/add$', AdicionarAtividade.as_view(), name='adicionar-atividade'),
    url(r'^atividades/relatorio/semanal$', RelatorioSemanal.as_view(), name='relatorio-semanal'),
    url(r'^usuario/add$', atividade_view.adicionar_usuario, name='add-usuario'),
    url(r'^logout$', atividade_view.logout, name='logout'),
    url(r'^compare$', ComparaSemanas.as_view(), name='compare'),
    url(r'^categoria/(?P<atividade_id>[0-9]+)-(?P<categoria>\w+)', atividade_view.salvar_categoria,
        name='salvar_categoria')


]
