# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from aplicacao.forms import FormAtividade
from aplicacao.models import Atividade, Usuario
import operator
import base64
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class LoginView(TemplateView):
    """
    Esta classe gerencia o login
    """
    template_name = 'login.html'


def logout(request):
    """
    this class limpa a sessão de um usuário
    """
    request.session['id'] = None
    return redirect("https://mail.google.com/mail/u/0/?logout&hl=en")


def adicionar_usuario(request):
    """
    Classe que adiciona um usuário e inicia a sessão.
    """
    data = request.POST
    nome = data.get('nome')
    email = data.get('email')
    foto = data.get('foto')
    user_id = data.get('user_id')
    try:
        usuario = Usuario.objects.get(email=email)
    except:
        usuario = Usuario(nome=nome, email=email, foto=foto, user_id=user_id)
        usuario.save()

    request.session['id'] = usuario.user_id
    request.session['nome'] = usuario.nome
    if usuario.foto:
        request.session['foto'] = foto
    else:
        request.session[
            'foto'] = 'http://praondevaimeutempo.herokuapp.com/static/dist/img/user9-128x128.png'
    return redirect('atividades')


class ListaAtividades(TemplateView):
    """
    Esta classe lista todas as atividades cadastradas.
    """

    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        try:
            if not request.session or not request.session['id']:
                return redirect('login')
        except:
            return redirect('login')
        lista_atividades = _get_atividades_semana(request.session['id'], 0)
        page = request.GET.get('page')
        max = len(lista_atividades)
        paginator = Paginator(lista_atividades, 10)
        try:
            lista_atividades = paginator.page(page)
        except PageNotAnInteger:
            lista_atividades = paginator.page(1)
        except EmptyPage:
            lista_atividades = paginator.page(paginator.num_pages)
        context = self.get_context_data(
            lista_atividades=lista_atividades,
            foto=request.session['foto'],
            nome=request.session['nome']
        )
        return self.render_to_response(context)


class AdicionarAtividade(FormView):
    """Atividade.objects.all().order_by('-data')
    Esta classe adiciona uma nova atividade ao sistema
    """
    template_name = 'adicionar_atividade.html'
    form_class = FormAtividade
    success_url = '/'

    def get(self, request, *args, **kwargs):
        try:
            if not request.session['id']:
                return redirect('login')
        except:
            return redirect('login')
        context = self.get_context_data(
            foto=request.session['foto'],
            nome=request.session['nome'],
            user_id=request.session['id']
        )
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Realiza tratamento da data antes da validação do formulário.
        """
        data = request.POST
        st = ""
        if(len(request.FILES.keys()) > 0):
            request.FILES[request.FILES.keys()[0]].seek(0)
            st1 = request.FILES[request.FILES.keys()[0]].read()
            st = base64.encodestring(st1)
        my_dict = {}
        for key in data:
            my_dict[key] = data[key]
        my_dict["data"] = _convert_date(my_dict["data"])
        form = FormAtividade(my_dict)

        if form.is_valid():
            return self.form_valid(form, st)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, fotoBase64):
        """
        Este método adiciona uma nova atividade no banco de dados.
        """
        data = form.cleaned_data
        atividade = Atividade()
        atividade.nome = data['nome']
        atividade.tempo_investido = data['tempo_investido']
        if fotoBase64 != "":
            atividade.foto = fotoBase64
        atividade.data = data['data']
        atividade.prioridade = data['prioridade']
        user = Usuario.objects.get(user_id=data['user'])
        atividade.user = user
        atividade.save()

        return super(AdicionarAtividade, self).form_valid(form)


class RelatorioSemanal(TemplateView):
    """
    Esta classe exibe o relatório semanal
    """
    template_name = 'relatorio_semanal.html'

    def get(self, request, *args, **kwargs):
        try:
            if not request.session['id']:
                return redirect('login')
        except:
            return redirect('login')
        resumo, total_horas, total_prioritarias = _get_resume(
            _get_atividades_semana(request.session['id'], 0))
        categs = ["NENHUMA", "TRABALHO", "LAZER"]
        if "categ" in request.GET and request.GET.get("categ") != "NENHUMA":
            atividades_semanas = _get_atividades_por_categoria(request.session['id'], request.GET.get("categ"))
            resumo_categ = _get_resume_categ(atividades_semanas)
            categs.insert(0, categs.pop(categs.index(request.GET.get("categ"))))
            context = self.get_context_data(resumo=resumo, total_hotas=total_horas,
                                total_prioritarias=total_prioritarias,
                                resumo_categ = resumo_categ,
                                categs = categs,
                                foto=request.session['foto'],
                                nome=request.session['nome'])
        else:
            context = self.get_context_data(resumo=resumo, total_hotas=total_horas,
                                        total_prioritarias=total_prioritarias,
                                        categs = categs,
                                        foto=request.session['foto'],
                                        nome=request.session['nome'])
        return self.render_to_response(context)


def _convert_date(date):
    """
    This method converts a date to american pattern.
    :param date: Date to be converted.
    :return: String Date in american pattern.
    """
    formats = ['%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y',
               '%Y/%m/%d', '%Y-%m-%d', '%y/%m/%d', '%y-%m-%d', '%m/%d/%Y']

    for format_date in formats:
        try:
            date = str(datetime.datetime.strptime(date, format_date).date())
            return date
        except ValueError:
            continue
    raise ValueError


def _get_atividades_semana(user_id, semana):
    date = datetime.date.today()
    if date.day == date.weekday():
        start_week = date
    else:
        start_week = date - datetime.timedelta(date.weekday() + 1)

    #semana atual = 0, semana passada = 1 e semana retrasada = 2
    start_week = date.fromordinal(start_week.toordinal() - (semana*7))

    end_week = start_week + datetime.timedelta(6)
    user = Usuario.objects.get(user_id=user_id)
    return Atividade.objects.filter(data__range=[start_week, end_week], user=user.id)

def _get_atividades_por_categoria(user_id, categoria):
    atividades = _get_atividades_semana(user_id, 0)

    lista_por_categoria = []
    for atividade in atividades:
        if atividade.categoria == categoria:
            lista_por_categoria.append(atividade)

    return lista_por_categoria

def _get_resume(activity_list):
    resume_dict = {}
    total_horas = 0
    total_prioritarias = 0
    for activity in activity_list:
        if activity.prioridade:
            total_prioritarias += activity.tempo_investido
        if activity.categoria in resume_dict:
            resume_dict[activity.categoria] += activity.tempo_investido
            total_horas += activity.tempo_investido
        else:
            resume_dict[activity.categoria] = activity.tempo_investido
            total_horas += activity.tempo_investido

    return sorted(resume_dict.items(), key=operator.itemgetter(1), reverse=True), total_horas, \
           total_prioritarias

def _get_resume_categ(activity_list):
    resume_dict = {}
    for activity in activity_list:
        resume_dict[activity.nome] = activity.tempo_investido

    return sorted(resume_dict.items(), key=operator.itemgetter(1), reverse=True)

class ComparaSemanas(TemplateView):
    """
    Exibi pagina de comparação entre as semanas
    """

    template_name = 'compare_semanas.html'

    def get(self, request, *args, **kwargs):
        try:
            if not request.session['id']:
                return redirect('login')
        except:
            return redirect('login')
        resumo1, total_horas1, total_prioritarias1 = _get_resume(
            _get_atividades_semana(request.session['id'], 0))
        resumo2, total_horas2, total_prioritarias2 = _get_resume(
            _get_atividades_semana(request.session['id'], 1))
        resumo3, total_horas3, total_prioritarias3 = _get_resume(
            _get_atividades_semana(request.session['id'], 2))
        print resumo2
        context = self.get_context_data(resumo=resumo1,
                                        total_hotas=total_horas1,
                                        total_prioritarias=total_prioritarias1,
                                        resumo2=resumo2,
                                        total_hotas2=total_horas2,
                                        total_prioritarias2=total_prioritarias2,
                                        resumo3=resumo3,
                                        total_hotas3=total_horas3,
                                        total_prioritarias3=total_prioritarias3,
                                        foto=request.session['foto'],
                                        nome=request.session['nome'])
        return self.render_to_response(context)


def salvar_categoria(request, **kwargs):
    """
    Este metodo recebe uma atividade e salva a categoria.
    """
    atividade = Atividade.objects.get(id=kwargs['atividade_id'])
    atividade.categoria = kwargs['categoria']
    atividade.save()
    return redirect('atividades')
