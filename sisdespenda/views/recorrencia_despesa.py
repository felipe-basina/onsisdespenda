# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db import connection
from collections import namedtuple
from ..models import RecorrenciaDespesaTbl, TipoDespesaTbl
from ..models import RecorrenciaDespesaForm
import datetime
import itertools

@login_required(login_url='/accounts/login/')
def recorrencia_despesa_list(request):
	dict_recorrencia_despesa = definir_valores_recorrencia_template(request)
	return render(request, 'onsis/recorrencia_despesa_list.html', { 'template': dict_recorrencia_despesa, 'cd_reg': 0 })

@login_required(login_url='/accounts/login/')
def recorrencia_despesa_new(request, pk=0):
	dict_recorrencia = {}

	if request.method == "POST":
		form = RecorrenciaDespesaForm(request.POST)
		if form.is_valid():
			recorrencia = form.save(commit=False)
			if int(pk) > 0: recorrencia.cd_registro = pk
			recorrencia.cd_usuario = request.user.id
			recorrencia.dt_criacao = datetime.datetime.utcnow().replace(tzinfo=utc)
			recorrencia.save()
			
			dict_recorrencia = definir_valores_recorrencia_template(request)
			dict_recorrencia['mensagem'] = 'Recorrência salva com sucesso!'
			dict_recorrencia['status'] = 'success'
		else:
			dict_recorrencia = definir_valores_recorrencia_template(request)
			dict_recorrencia['mensagem'] = 'Não foi possível salvar a recorrência!'
			dict_recorrencia['status'] = 'danger'
		pk=0
	else:
		dict_recorrencia = definir_valores_recorrencia_template(request)

		try:
			recorrencia_despesa = recuperar_recorrencia_usuario_por_id_recorrencia_despesa(request, pk)
		except RecorrenciaDespesaTbl.DoesNotExist:
			dict_recorrencia['mensagem'] = 'Registro não encontrado!'
			dict_recorrencia['status'] = 'danger'
			return render(request, 'onsis/recorrencia_despesa_list.html', {'template': dict_recorrencia, 'cd_reg': 0})

		form = RecorrenciaDespesaForm(initial={'cd_registro': recorrencia_despesa.cd_registro, 
												'dia_recorrencia': recorrencia_despesa.dia_recorrencia, 
												'mes_recorrencia': recorrencia_despesa.mes_recorrencia, 
												'recorrencia': recorrencia_despesa.recorrencia, 
												'ds_despesa': recorrencia_despesa.ds_despesa, 
												'cd_tipo_despesa': recorrencia_despesa.cd_tipo_despesa, 
												'vl_despesa': recorrencia_despesa.vl_despesa})
		
		
		dict_recorrencia['form'] = form
		form.fields['cd_tipo_despesa'].queryset = recuperar_todos_tipo_despesa_usuario(request)

	return render(request, 'onsis/recorrencia_despesa_list.html', { 'template': dict_recorrencia, 'cd_reg': pk })

@login_required(login_url='/accounts/login/')
def recorrencia_despesa_remove(request, pk):
	try:
		recorrencia_despesa = recuperar_recorrencia_usuario_por_id_recorrencia_despesa(request, pk)

		if recorrencia_despesa:
			recorrencia_despesa.delete()        
			dict_recorrencia = definir_valores_recorrencia_template(request)
			dict_recorrencia['mensagem'] = 'Recorrência removida com sucesso!'
			dict_recorrencia['status'] = 'success'
	except:
		dict_recorrencia = definir_valores_recorrencia_template(request)
		dict_recorrencia['mensagem'] = 'Recorrência não encontrada!'
		dict_recorrencia['status'] = 'danger'
        
	return render(request, 'onsis/recorrencia_despesa_list.html', { 'template': dict_recorrencia })

######################################
#          Funcoes diversas          #
######################################

# Recuperar recorrencia por usuario e id despesa
def recuperar_recorrencia_usuario_por_id_recorrencia_despesa(request, pk):
	return RecorrenciaDespesaTbl.objects.get(cd_registro=pk, cd_usuario=request.user.id)

# Recuperar todas as recorrencias definidas pelo usuario
def recuperar_recorrencias_usuario(request):
	return RecorrenciaDespesaTbl.objects.filter(cd_usuario=request.user.id).order_by('dt_criacao')

# Tipo de despesa: recuperar tudo por usuario
def recuperar_todos_tipo_despesa_usuario(request):
	return TipoDespesaTbl.objects.filter(cd_usuario__in=[0, request.user.id]).order_by('ds_tipo_despesa')

def definir_valores_recorrencia_template(request):
	dict_recorrencia = {}

	recorrencias = recuperar_recorrencias_usuario(request)
	dict_recorrencia['recorrencias'] = recorrencias

	form = RecorrenciaDespesaForm()
	form.fields['cd_tipo_despesa'].queryset = recuperar_todos_tipo_despesa_usuario(request)
	dict_recorrencia['form'] = form

	return dict_recorrencia