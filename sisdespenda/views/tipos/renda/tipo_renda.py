# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.timezone import utc
import datetime
from sisdespenda.models import TipoRendaTbl
from sisdespenda.models import TipoRendaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

@login_required(login_url='/accounts/login/')
def tipo_renda_list(request):
	tipos = recuperar_todos_tipo_renda_usuario(request)
	form = TipoRendaForm()
	return render(request, 'onsis/tipos/renda/tipo_renda_list.html', {'tipos':tipos, 'form': form, 'cd_reg': 0})

@login_required(login_url='/accounts/login/')
def tipo_renda_new(request):

    if request.method == "POST":
        form = TipoRendaForm(request.POST)
        if form.is_valid():
            tipo = form.save(commit=False)
            
            # Verifica se existe registro com o mesmo nome definido no formulario
            tipo_renda_existente = verificar_existencia_tipo_renda(tipo.ds_tipo_renda)

            if tipo_renda_existente:            
                tipos = recuperar_todos_tipo_renda_usuario(request)
                
                mensagem_erro = 'Nao foi possivel definir novo tipo renda: valor [ ' + tipo.ds_tipo_renda + ' ] ja cadastrado!'

                return render(request, 'onsis/tipos/renda/tipo_renda_list.html', {'form': TipoRendaForm(),
                                                                        'tipos': tipos, 
                                                                        'cd_reg': 0,
                                                                        'mensagem': mensagem_erro, 
                                                                        'status': 'danger'})                

            tipo.cd_usuario = request.user.id
            tipo.dt_criacao = datetime.datetime.utcnow().replace(tzinfo=utc)
            tipo.dt_atualizacao = datetime.datetime.utcnow().replace(tzinfo=utc)
            tipo.save()
            
            form = TipoRendaForm()
            
            tipos = recuperar_todos_tipo_renda_usuario(request)
            return render(request, 'onsis/tipos/renda/tipo_renda_list.html', {'form': form,
                                                                    'tipos': tipos, 
                                                                    'cd_reg': 0,
                                                                    'mensagem': 'Tipo renda salvo com sucesso!', 
                                                                    'status': 'success'})
    else:
        form = TipoRendaForm()
    return render(request, 'onsis/tipos/renda/tipo_renda_list.html', {'form': form})
    
@login_required(login_url='/accounts/login/')	
def tipo_renda_update(request, pk):
    print ('Registro selecionado: %s' % pk)

    tipos = recuperar_todos_tipo_renda_usuario(request)
    
    if not pk:
        return render(request, 'onsis/tipos/renda/tipo_renda_list.html', {'form': form,
                                                              'tipos': tipos,  
                                                              'cd_reg': 0,
                                                              'mensagem': 'Registro invalido!', 
                                                              'status': 'danger'})
    try:
        
        tipo_cadastrado = TipoRendaTbl.objects.get(cd_registro=pk, cd_usuario=request.user.id)
    
    except TipoRendaTbl.DoesNotExist:
        form = TipoRendaForm()    

        return render(request, 'onsis/tipos/renda/tipo_renda_list.html', {'form': form,
                                                              'tipos': tipos,  
                                                              'cd_reg': 0,
                                                              'mensagem': 'Registro nao encontrado!', 
                                                              'status': 'danger'})
    
    if request.method == "POST":
        form = TipoRendaForm(request.POST)
        if form.is_valid():
            tipo = form.save(commit=False)

            # Verifica se existe registro com o mesmo nome definido no formulario
            tipo_renda_existente = verificar_existencia_tipo_renda(tipo.ds_tipo_renda)
            
            '''
            Verificar se o tipo renda selecionado para edicao trata-se do mesmo 
            existente na base de dados, dessa forma permite com que o tipo de renda editado
            possa ter a caixa alterada
            '''
            if tipo_cadastrado.ds_tipo_renda.upper() != tipo.ds_tipo_renda.upper() and tipo_renda_existente:          
                tipos = recuperar_todos_tipo_renda_usuario(request)
                
                mensagem_erro = 'Nao foi possivel atualizar tipo renda: valor [ ' + tipo.ds_tipo_renda + ' ] ja cadastrado!'

                return render(request, 'onsis/tipos/renda/tipo_renda_list.html', {'form': form,
                                                                        'tipos': tipos, 
                                                                        'cd_reg': pk,
                                                                        'mensagem': mensagem_erro, 
                                                                        'status': 'danger'}) 

            try:
            
                descricao = unicode(tipo.ds_tipo_renda)
                
            except TypeError:
            
                descricao = tipo.ds_tipo_renda
                
            except NameError:
            
                descricao = tipo.ds_tipo_renda            
            
            novo_tipo = TipoRendaTbl(cd_registro=pk,
                                    dt_criacao=tipo_cadastrado.dt_criacao,
                                    cd_usuario=tipo_cadastrado.cd_usuario,
                                    dt_atualizacao=datetime.datetime.utcnow().replace(tzinfo=utc),
                                    ds_tipo_renda=descricao)
            novo_tipo.save(force_insert=False)
            
            form = TipoRendaForm()
            
            tipos = recuperar_todos_tipo_renda_usuario(request)
            return render(request, 'onsis/tipos/renda/tipo_renda_list.html', {'form': form,
                                                                    'tipos': tipos, 
                                                                    'cd_reg': 0,
                                                                    'mensagem': 'Tipo renda atualizado com sucesso!', 
                                                                    'status': 'success'})
    else:
        form = TipoRendaForm()
        tipos = recuperar_todos_tipo_renda_usuario(request)

    return render(request, 'onsis/tipos/renda/tipo_renda_list.html', {'form': form,
                                                          'tipos': tipos,  
                                                          'cd_reg': 0,
                                                          'mensagem': 'Nao foi possivel atualizar tipo de renda!', 
                                                          'status': 'danger'})
	
@login_required(login_url='/accounts/login/')
def tipo_renda_edit(request, pk):
    tipos = recuperar_todos_tipo_renda_usuario(request)
    
    try:
        
        tipo = TipoRendaTbl.objects.get(cd_registro=pk, cd_usuario=request.user.id)
        
    except TipoRendaTbl.DoesNotExist:
        form = TipoRendaForm()
        
        return render(request, 'onsis/tipos/renda/tipo_renda_list.html', {'form': form, 'mensagem': 'Tipo renda não encontrado!', 'status': 'danger', 'tipos': tipos})
    
    if not tipo:
    
        return render(request, 'onsis/tipos/renda/tipo_renda_list.html', {'mensagem': 'Tipo renda não encontrado!', 'status': 'danger', 'tipos': tipos})
        
    else:
        
        form = TipoRendaForm(initial={'cd_registro': tipo.cd_registro, 'ds_tipo_renda': tipo.ds_tipo_renda})
        print ('form %s' % form)
        
        return render(request, 'onsis/tipos/renda/tipo_renda_list.html',
                      {'form': form, 'mensagem': 'Tipo renda selecionado para edição!',
                               'status': 'info', 
                               'tipos': tipos,
                               'cd_reg': pk})

######################################
#          Funcoes diversas          #
######################################

# Tipo de renda: recuperar tudo por usuario
def recuperar_todos_tipo_renda_usuario(request):
    return TipoRendaTbl.objects.filter(cd_usuario__in=[0, request.user.id]).order_by('-dt_atualizacao')
    
# Verificar se existe tipo de renda especifico    
def verificar_existencia_tipo_renda(ds_tipo_renda):
    tipo_renda_existente = TipoRendaTbl.objects.filter(ds_tipo_renda__iexact=ds_tipo_renda)

    if tipo_renda_existente:
        return True
    else:
        return False