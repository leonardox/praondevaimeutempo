from aplicacao.models import Usuario, Atividade


def criar_usuario():
    try:
        usuario = Usuario.objects.get(email='teste@povmt.com')
    except Usuario.DoesNotExist:

        usuario = Usuario(nome='Usuario Teste', email='teste@povmt.com', user_id='id_teste')
        usuario.save()
    return usuario


def remover_usuario(email):
    try:
        Usuario.objects.get(email=email).delete()
    except Usuario.DoesNotExist:
        pass


def remover_atividade(nome, user):
    try:
        Atividade.objects.filter(nome=nome, user=user).delete()
    except Atividade.DoesNotExist:
        pass
