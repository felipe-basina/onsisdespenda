# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms

class TipoDespesaTbl(models.Model):
    cd_registro = models.BigAutoField(primary_key=True)
    ds_tipo_despesa = models.CharField(max_length=60)
    dt_criacao = models.DateTimeField(default=timezone.now)
    dt_atualizacao = models.DateTimeField(default=timezone.now)
    cd_usuario = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'tipo_despesa_tbl'
        verbose_name = ('Tipo de despesa')
		
    def __str__(self):
        return self.ds_tipo_despesa
    
    # Permite com que esse campo receba caracteres especiais
    def __unicode__(self):
        return self.ds_tipo_despesa
        
class TipoDespesaForm(ModelForm):
    class Meta:
        model = TipoDespesaTbl
        fields = ['ds_tipo_despesa']
        labels = {
            'ds_tipo_despesa': ('Descrição tipo de despesa')
        }
        widgets = {
            'ds_tipo_despesa': forms.TextInput(attrs={'class': 'form-control',}),
        }

class DespesaTbl(models.Model):
    cd_registro = models.BigAutoField(primary_key=True)
    vl_despesa = models.DecimalField(max_digits=1000, decimal_places=2)
    dt_despesa = models.DateTimeField()
    ds_despesa = models.CharField(max_length=100)
    dt_criacao = models.DateTimeField()
    dt_atualizacao = models.DateTimeField()
    cd_usuario = models.BigIntegerField()
    cd_recorrencia_despesa = models.BigIntegerField()
    cd_tipo_despesa = models.ForeignKey('TipoDespesaTbl', models.DO_NOTHING, db_column='cd_tipo_despesa', blank=True, null=True)

    class Meta:
        ordering = ['-dt_despesa']
        managed = True
        db_table = 'despesa_tbl'
        verbose_name = ('Despesa')

class DespesaForm(ModelForm):
    class Meta:
        model = DespesaTbl
        fields = ['dt_despesa', 'vl_despesa', 'cd_tipo_despesa', 'ds_despesa']
        labels = {
            'dt_despesa': ('Data da despesa'),
            'vl_despesa': ('Valor da despesa'),
            'cd_tipo_despesa': ('Tipo de despesa'),
            'ds_despesa': ('Descrição da despesa'),
        }
        widgets = {
            'dt_despesa': forms.DateInput(format=('%d/%m/%Y'),
                                             attrs={'class':'form-control', 'type':'date',                                             
                                            'placeholder':'Selecione uma data'}),
            'vl_despesa': forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}),
            'cd_tipo_despesa': forms.Select(attrs={'class': 'form-control',}),
            'ds_despesa': forms.TextInput(attrs={'class': 'form-control',}),
        }

    def __init__(self, *args, **kwargs):
        # Construtor pai
        super(DespesaForm, self).__init__(*args, **kwargs)
        # Define qual campo no formulario nao sera mais obrigatorio
        self.fields['ds_despesa'].required = False
       
class RecorrenciaDespesaTbl(models.Model):
    cd_registro = models.BigAutoField(primary_key=True)
    cd_usuario = models.BigIntegerField()
    vl_despesa = models.DecimalField(max_digits=1000, decimal_places=2)
    ds_despesa = models.CharField(max_length=100)
    cd_tipo_despesa = models.ForeignKey('TipoDespesaTbl', models.DO_NOTHING, db_column='cd_tipo_despesa', blank=True, null=True)
    recorrencia = models.CharField(max_length=1)
    dia_recorrencia = models.IntegerField()
    mes_recorrencia = models.IntegerField()
    dt_criacao = models.DateTimeField()

    class Meta:
        ordering = ['-dt_criacao']
        managed = True
        db_table = 'recorrencia_despesa_tbl'
        verbose_name = ('Recorrencia despesa')

RECORRENCIA_OPCOES = (
    ('M', 'mês'),
    ('A', 'ano')
)

DIAS_OPCOES = [(str(i), str(i)) for i in range(1, 32)]
MESES_OPCOES = [(str(i), str(i)) for i in range(1, 13)]

class RecorrenciaDespesaForm(ModelForm):
    class Meta:
        model = RecorrenciaDespesaTbl
        fields = ['dia_recorrencia', 'mes_recorrencia', 'recorrencia', 'vl_despesa', 'cd_tipo_despesa', 'ds_despesa']
        labels = {
            'dia_recorrencia': ('Dia da recorrência'),
            'mes_recorrencia': ('Mês da recorrência'),
            'recorrencia': ('Tipo da recorrência'),
            'vl_despesa': ('Valor da despesa'),
            'cd_tipo_despesa': ('Tipo de despesa'),
            'ds_despesa': ('Descrição da despesa'),
        }
        widgets = {
            'dia_recorrencia': forms.Select(choices=DIAS_OPCOES, attrs={'class': 'form-control tamanho_caixa',}),
            'mes_recorrencia': forms.Select(choices=MESES_OPCOES, attrs={'class': 'form-control tamanho_caixa',}),
            'recorrencia': forms.RadioSelect(choices=RECORRENCIA_OPCOES, attrs={'class': 'custom_radio form-control',}),
            'vl_despesa': forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}),
            'cd_tipo_despesa': forms.Select(attrs={'class': 'form-control',}),
            'ds_despesa': forms.TextInput(attrs={'class': 'form-control',}),
        }

class EventoTbl(models.Model):
    cd_registro = models.BigAutoField(primary_key=True)
    ds_evento = models.CharField(max_length=100)
    dt_evento = models.DateTimeField()
    cd_usuario = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'evento_tbl'
        verbose_name = ('Evento')

class TipoRendaTbl(models.Model):
    cd_registro = models.BigAutoField(primary_key=True)
    ds_tipo_renda = models.CharField(max_length=60)
    dt_criacao = models.DateTimeField(default=timezone.now)
    dt_atualizacao = models.DateTimeField(default=timezone.now)
    cd_usuario = models.BigIntegerField()
    #cd_usuario = models.ForeignKey('UsuarioTbl', models.DO_NOTHING, db_column='cd_usuario', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_renda_tbl'
        verbose_name = ('Tipo de renda')
		
    def __str__(self):
        return self.ds_tipo_renda
    
    # Permite com que esse campo receba caracteres especiais
    def __unicode__(self):
        return self.ds_tipo_renda

class TipoRendaForm(ModelForm):
    class Meta:
        model = TipoRendaTbl
        fields = ['ds_tipo_renda']
        labels = {
            'ds_tipo_renda': ('Descrição tipo de renda')
        }
        widgets = {
            'ds_tipo_renda': forms.TextInput(attrs={'class': 'form-control',}),
        }
      
class RendaTbl(models.Model):
    cd_registro = models.BigAutoField(primary_key=True)
    vl_renda = models.DecimalField(max_digits=1000, decimal_places=2)
    dt_renda = models.DateTimeField()
    dt_criacao = models.DateTimeField()
    dt_atualizacao = models.DateTimeField()
    cd_tipo_renda = models.ForeignKey('TipoRendaTbl', models.DO_NOTHING, db_column='cd_tipo_renda', blank=True, null=True)
    cd_usuario = models.BigIntegerField()
    #cd_usuario = models.ForeignKey('UsuarioTbl', models.DO_NOTHING, db_column='cd_usuario', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'renda_tbl'
        verbose_name = ('Renda')

class RendaForm(ModelForm):
    class Meta:
        model = RendaTbl
        fields = ['dt_renda', 'vl_renda', 'cd_tipo_renda']
        labels = {
            'dt_renda': ('Data da renda'),
            'vl_renda': ('Valor da renda'),
            'cd_tipo_renda': ('Tipo de renda'),
        }
        widgets = {
            'dt_renda': forms.DateInput(format=('%d/%m/%Y'),
                                             attrs={'class':'form-control', 'type':'date',                                             
                                            'placeholder':'Selecione uma data'}),
            'vl_renda': forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}),
            'cd_tipo_renda': forms.Select(attrs={'class': 'form-control',}),
        }
        
class AlteraSenhaForm(forms.Form):
    class Meta:
        senha = forms.CharField(label='Senha', max_length=100)
        nova_senha = forms.CharField(label='Nova senha', max_length=100)