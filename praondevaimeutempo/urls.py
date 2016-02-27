from django.conf.urls import include, url
from django.contrib import admin

from aplicacao.views.atividade_view import ListaAtividades

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', ListaAtividades.as_view(), name='atividades'),
]
