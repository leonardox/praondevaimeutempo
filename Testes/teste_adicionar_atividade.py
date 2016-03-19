# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.test import TestCase

from Testes import utils
from aplicacao.models import Atividade
from aplicacao.views import atividade_view


class TesteAdicionarAtividade(TestCase):
    """
    Esta classe realiza os testes relacionados com a criação de atividades
    """
    def teste_adicionar_ativiade_sucesso(self):
        usuario = utils.criar_usuario()
        atividade = Atividade(nome="Teste_01", tempo_investido=1, categoria='Lazer',
                              user=usuario)
        atividade.save()
        atividade_db = Atividade.objects.filter(nome='Teste_01', user=usuario).values()[0]
        self.assertIsNotNone(atividade_db)
        self.assertEqual(atividade.nome, atividade_db['nome'])
        self.assertEqual(atividade.user.id, atividade_db['user_id'])

        utils.remover_atividade('Teste_01', usuario.id)

    def teste_adiciona_atividade_sem_usuario(self):
        atividade = Atividade(nome="Teste_01", tempo_investido=1, categoria='Lazer')
        try:
            atividade.save()
            self.fail("Atividade foi salva")
        except IntegrityError:
            pass

    def teste_adiciona_atividade_sem_nome(self):
        usuario = utils.criar_usuario()
        atividade = Atividade(tempo_investido=1, categoria='Lazer', user=usuario)
        try:
            atividade.save()
            self.fail("Atividade foi salva")
        except IntegrityError:
            pass

class TesteVisualizarRelatorioCategoria(TestCase):
    """
    Esta classe realiza os testes relacionados com a visualização de atividades por uma categoria especifica
    """
    def teste_visualizar_atividade_lazer(self):
        usuario = utils.criar_usuario()

        atividade01 = Atividade(nome="Teste_01", tempo_investido=1, categoria='Lazer',
                              user=usuario)

        atividade02 = Atividade(nome="Teste_02", tempo_investido=2, categoria='Lazer',
                              user=usuario)
        atividade01.save()
        atividade02.save()

        atividade_db = Atividade.objects.filter(nome='Teste_01', user=usuario).values()[0]

        atv_view = atividade_view._get_atividades_por_categoria(usuario.user_id, 'Lazer')

        self.assertTrue(len(atv_view)==2)
        self.assertEqual(atividade_db['nome'], atv_view[0].nome)

        resumo_categ = atividade_view._get_resume_categ(atv_view)
        resumo_atv01 = resumo_categ[0]

        self.assertEquals(resumo_atv01[0], 'Teste_02')

        utils.remover_atividade('Teste_01', usuario.id)
        utils.remover_atividade('Teste_02', usuario.id)

    def teste_atividade_categoria_nao_cadastrada(self):
        usuario = utils.criar_usuario()

        atv_view = atividade_view._get_atividades_por_categoria(usuario.user_id, 'Trabalho')
        self.assertTrue(len(atv_view)==0)