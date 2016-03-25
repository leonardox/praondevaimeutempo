# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.test import TestCase

from Testes import utils
from aplicacao.models import Atividade, Tag
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

class TesteVisualizarRelatorioPorTags(TestCase):
    """
    Esta classe realiza os testes relacionados com a visualização de atividades por tags especificas
    """
    def teste_usuario_sem_tag(self):
        usuario = utils.criar_usuario()

        atividade01 = Atividade(nome="Teste_01", tempo_investido=1, categoria='Lazer',
                              user=usuario)
        atividade01.save()

        lista_de_tags = atividade_view.recupera_atividade_tag(usuario.user_id, 'Olar')#tag não exite no BD

        self.assertTrue(len(lista_de_tags)==0)
        self.assertEqual(lista_de_tags, [])

    def teste_usuario_com_tag(self):
        usuario = utils.criar_usuario()

        atividade01 = Atividade(nome="Teste_01", tempo_investido=1, categoria='Lazer',
                              user=usuario)

        atividade02 = Atividade(nome="Teste_02", tempo_investido=2, categoria='Lazer',
                              user=usuario)
        atividade01.save()
        atividade02.save()

        atividade_view._salvar_tags('olar top', usuario, atividade01)
        atividade_view._salvar_tags('show top', usuario, atividade02)

        lista_de_atividades = atividade_view.recupera_atividade_tag(usuario.user_id, 'top')

        self.assertTrue(len(lista_de_atividades)==2)#top esta cadastrado nas atividade 01 e 02
        self.assertEqual(lista_de_atividades[0].nome, atividade01.nome)#lista_de_atividades[0] == atividade01

        #recuperando todas as tags de um usuario
        lista_tags = atividade_view.recupera_tags_usuario(usuario.user_id)#foram cadastradas 4 tags
        self.assertTrue('olar' in lista_tags)
        self.assertTrue('tagNaoCadastrada' not in lista_tags)


