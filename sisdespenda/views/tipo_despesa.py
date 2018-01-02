# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.timezone import utc
import datetime
from ..models import TipoDespesaTbl
from ..models import TipoDespesaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

@login_required(login_url='/accounts/login/')
def tipo_despesa_list(request):
	tipos = recuperar_todos_tipo_despesa_usuario(request)
	form = TipoDespesaForm()
	return render(request, 'onsis/tipo_despesa_list.html', {'tipos':tipos, 'form': form, 'cd_reg': 0})

@login_required(login_url='/accounts/login/')
def tipo_detail(request, pk):
	tipo = get_object_or_404(TipoDespesaTbl, pk=pk)
	return render(request, 'onsis/tipo_detail.html', {'tipo': tipo})

@login_required(login_url='/accounts/login/')	
def tipo_despesa_new(request):

    if request.method == "POST":
        form = TipoDespesaForm(request.POST)
        if form.is_valid():
            tipo = form.save(commit=False)
            
            # Verifica se existe registro com o mesmo nome definido no formulario
            tipo_despesa_existente = verificar_existencia_tipo_despesa(tipo.ds_tipo_despesa)

            if tipo_despesa_existente:            
                tipos = recuperar_todos_tipo_despesa_usuario(request)
                
                mensagem_erro = 'Nao foi possivel definir novo tipo despesa: valor [ ' + tipo.ds_tipo_despesa + ' ] ja cadastrado!'

                return render(request, 'onsis/tipo_despesa_list.html', {'form': TipoDespesaForm(), 
                                                                        'tipos': tipos, 
                                                                        'cd_reg': 0,
                                                                        'mensagem': mensagem_erro, 
                                                                        'status': 'danger'})                

            tipo.cd_usuario = request.user.id
            tipo.dt_criacao = datetime.datetime.utcnow().replace(tzinfo=utc)
            tipo.dt_atualizacao = datetime.datetime.utcnow().replace(tzinfo=utc)
            tipo.save()
            
            form = TipoDespesaForm()
            
            tipos = recuperar_todos_tipo_despesa_usuario(request)
            return render(request, 'onsis/tipo_despesa_list.html', {'form': form, 
                                                                    'tipos': tipos, 
                                                                    'cd_reg': 0,
                                                                    'mensagem': 'Tipo despesa salvo com sucesso!', 
                                                                    'status': 'success'})
    else:
        form = TipoDespesaForm()
    return render(request, 'onsis/tipo_despesa_list.html', {'form': form})
    
@login_required(login_url='/accounts/login/')	
def tipo_despesa_update(request, pk):
    print ('Registro selecionado: %s' % pk)

    tipos = recuperar_todos_tipo_despesa_usuario(request)
    
    if not pk:
        return render(request, 'onsis/tipo_despesa_list.html', {'form': form,
                                                              'tipos': tipos,  
                                                              'cd_reg': 0,
                                                              'mensagem': 'Registro invalido!', 
                                                              'status': 'danger'})
    try:
        
        tipo_cadastrado = TipoDespesaTbl.objects.get(cd_registro=pk, cd_usuario=request.user.id)
    
    except TipoDespesaTbl.DoesNotExist:
        form = TipoDespesaForm()    

        return render(request, 'onsis/tipo_despesa_list.html', {'form': form,
                                                              'tipos': tipos,  
                                                              'cd_reg': 0,
                                                              'mensagem': 'Registro nao encontrado!', 
                                                              'status': 'danger'})
    
    if request.method == "POST":
        form = TipoDespesaForm(request.POST)
        if form.is_valid():
            tipo = form.save(commit=False)

            # Verifica se existe registro com o mesmo nome definido no formulario
            tipo_despesa_existente = verificar_existencia_tipo_despesa(tipo.ds_tipo_despesa)
            
            '''
            Verificar se o tipo despesa selecionado para edicao trata-se do mesmo 
            existente na base de dados, dessa forma permite com que o tipo de despesa editado
            possa ter a caixa alterada
            '''
            if tipo_cadastrado.ds_tipo_despesa.upper() != tipo.ds_tipo_despesa.upper() and tipo_despesa_existente:          
                tipos = recuperar_todos_tipo_despesa_usuario(request)
                
                mensagem_erro = 'Nao foi possivel atualizar tipo despesa: valor [ ' + tipo.ds_tipo_despesa + ' ] ja cadastrado!'

                return render(request, 'onsis/tipo_despesa_list.html', {'form': form, 
                                                                        'tipos': tipos, 
                                                                        'cd_reg': pk,
                                                                        'mensagem': mensagem_erro, 
                                                                        'status': 'danger'}) 

            try:
            
                descricao = unicode(tipo.ds_tipo_despesa)
                
            except TypeError:
            
                descricao = tipo.ds_tipo_despesa
                
            except NameError:
            
                descricao = tipo.ds_tipo_despesa            
            
            novo_tipo = TipoDespesaTbl(cd_registro=pk,
                                    dt_criacao=tipo_cadastrado.dt_criacao,
                                    cd_usuario=tipo_cadastrado.cd_usuario,
                                    dt_atualizacao=datetime.datetime.utcnow().replace(tzinfo=utc),
                                    ds_tipo_despesa=descricao)
            novo_tipo.save(force_insert=False)
            
            form = TipoDespesaForm()
            
            tipos = recuperar_todos_tipo_despesa_usuario(request)
            return render(request, 'onsis/tipo_despesa_list.html', {'form': form, 
                                                                    'tipos': tipos, 
                                                                    'cd_reg': 0,
                                                                    'mensagem': 'Tipo despesa atualizado com sucesso!', 
                                                                    'status': 'success'})
    else:
        form = TipoDespesaForm()
        tipos = recuperar_todos_tipo_despesa_usuario(request)

    return render(request, 'onsis/tipo_despesa_list.html', {'form': form,
                                                          'tipos': tipos,  
                                                          'cd_reg': 0,
                                                          'mensagem': 'Nao foi possivel atualizar tipo de despesa!', 
                                                          'status': 'danger'})
	
@login_required(login_url='/accounts/login/')
def tipo_despesa_edit(request, pk):
    tipos = recuperar_todos_tipo_despesa_usuario(request)
    
    try:
        
        tipo = TipoDespesaTbl.objects.get(cd_registro=pk, cd_usuario=request.user.id)
        
    except TipoDespesaTbl.DoesNotExist:
        form = TipoDespesaForm()
        
        return render(request, 'onsis/tipo_despesa_list.html', {'form': form,'mensagem': 'Tipo despesa não encontrado!', 'status': 'danger', 'tipos': tipos})
    
    if not tipo:
    
        return render(request, 'onsis/tipo_despesa_list.html', {'mensagem': 'Tipo despesa não encontrado!', 'status': 'danger', 'tipos': tipos})
        
    else:
        
        form = TipoDespesaForm(initial={'cd_registro': tipo.cd_registro, 'ds_tipo_despesa': tipo.ds_tipo_despesa})
        print ('form %s' % form)
        
        return render(request, 'onsis/tipo_despesa_list.html', 
                              {'form': form, 'mensagem': 'Tipo despesa selecionado para edição!', 
                               'status': 'info', 
                               'tipos': tipos,
                               'cd_reg': pk})

######################################
#          Funcoes diversas          #
######################################

# Tipo de despesa: recuperar tudo por usuario
def recuperar_todos_tipo_despesa_usuario(request):
    return TipoDespesaTbl.objects.filter(cd_usuario__in=[0, request.user.id]).order_by('-dt_atualizacao')
    
# Verificar se existe tipo de despesa especifico    
def verificar_existencia_tipo_despesa(ds_tipo_despesa):
    tipo_despesa_existente = TipoDespesaTbl.objects.filter(ds_tipo_despesa__iexact=ds_tipo_despesa)

    if tipo_despesa_existente:
        return True
    else:
        return False