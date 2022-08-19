# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def pagina_nao_encontrada(request):
    return render(request, '404.html')


@login_required(login_url='/accounts/login/')
def inicio(request):
    '''
    evento.evento_new(request, 'LOGIN USUÁRIO')
    '''
    mensagem = 'Olá %s, seja bem-vindo(a)!' % request.user
    return render(request, 'onsis/inicio.html', {'mensagem': mensagem, 'status': 'info'})
