# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.timezone import utc
import datetime
from . import evento
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth

def pagina_nao_encontrada(request):
    return render_to_response('404.html')

@login_required(login_url='/accounts/login/')
def inicio(request):
    '''
    evento.evento_new(request, 'LOGIN USUÁRIO')
    '''
    mensagem = 'Olá %s, seja bem-vindo(a)!' % (request.user)
    return render(request, 'onsis/inicio.html', {'mensagem': mensagem, 'status': 'info'})
