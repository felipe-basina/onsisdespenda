# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.timezone import utc
import datetime
from sisdespenda.views import evento
from sisdespenda.models import AlteraSenhaForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth

def login_req(request):
    return render(request, 'onsis/entrypoint/login.html', )

def logout_user(request):
    '''
    if request.user.id:
        evento.evento_new(request, 'LOGOUT USUÁRIO')
    '''
    auth.logout(request)
    return render(request, 'onsis/entrypoint/login.html', {'mensagem': 'Você saiu do sistema!', 'status': 'info'})
	
def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render(request, 'onsis/entrypoint/login.html', {'mensagem': 'usuário/senha inválidos', 'status': 'danger'})

@login_required(login_url='/accounts/login/')    
def set_user_password_form(request):
    form = AlteraSenhaForm()
    return render(request, 'onsis/altera_senha.html', {'form': form})
    
@login_required(login_url='/accounts/login/')    
def change_user_password(request):
    senha = request.POST['senha']
    nova_senha = request.POST['nova_senha']
    
    if senha != nova_senha:
        return render(request, 'onsis/altera_senha.html',
                      {'mensagem': 'Atencao! As senhas nao conferem!', 'status': 'warning'})
    
    mensagem = 'Senha alterada com sucesso!'
    status = 'info'
    
    try:

        user = request.user
        user.set_password(nova_senha)
        user.save()
    
    except Exception:
        mensagem = "Nao foi possivel alterar a sua senha. Por favor, tente novamente mais tarde ou entre em contato com o adminstrador"
        status = 'danger'
    
    return render(request, 'onsis/altera_senha.html', {'mensagem': mensagem, 'status': status})