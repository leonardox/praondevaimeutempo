# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.test import TestCase

from Testes import utils
from aplicacao.models import Atividade


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

#class TesteVisualizarRelatorioCategoria(TestCase):

    #def teste_visualizar