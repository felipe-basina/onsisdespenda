/**
 * Scripts geral
 */
$(function() {

	var endpoint = '/static';
   
    var dtTipoRenda = $('#tipo-renda, #tipo-despesa').dataTable({
        dom: 'lBfrtip',
            buttons: [
                {
                  extend: 'excelHtml5',
                  title: 'tipo-excel-online-sisdespenda_' + new Date().yyyymmdd(),
                  exportOptions: {
                    columns: [ 0, 1, 2 ]
                  }
                },
                {
                  extend: 'pdfHtml5',
                  orientation: 'landscape',
                  pageSize: 'LEGAL',
                  title: 'tipo-pdf-online-sisdespenda_' + new Date().yyyymmdd(),
                  exportOptions: {
                    columns: [ 0, 1, 2 ]
                  },
                  customize : function(doc) {
                    doc.defaultStyle.alignment = 'center';
                    doc.styles.tableHeader.alignment = 'center';
                    doc.content[1].table.widths = 
                        Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                  }
                }
            ],
		pagingType : 'simple', // Remove a paginação por números das páginas
		aoColumnDefs : [ // Remove o item para ordenação dos dois últimos elementos
		{
			bSortable : false,
			aTargets : [ -1, -2 ]
		} ]
	});
    
	// Ordena pelos valores da segunda coluna
	dtTipoRenda.fnSort([[1, 'asc']]);
    
    $('#recorrencia-despesa-tbl').dataTable({
        dom: 'lBfrtip',
            buttons: [
                {
                  extend: 'excelHtml5',
                  title: 'recorrencia-excel-online-sisdespenda_' + new Date().yyyymmdd(),
                  exportOptions: {
                    columns: [ 0, 1, 2, 3, 4, 5 ]
                  }
                },
                {
                  extend: 'pdfHtml5',
                  orientation: 'landscape',
                  pageSize: 'LEGAL',
                  title: 'recorrencia-pdf-online-sisdespenda_' + new Date().yyyymmdd(),
                  exportOptions: {
                    columns: [ 0, 1, 2, 3, 4, 5 ]
                  },
                  customize : function(doc) {
                    doc.defaultStyle.alignment = 'center';
                    doc.styles.tableHeader.alignment = 'center';
                    doc.content[1].table.widths = 
                        Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                  }
                }
            ],
    pagingType : 'simple', // Remove a paginação por números das páginas
    aoColumnDefs : [ // Remove o item para ordenação dos dois últimos elementos
    {
      bSortable : false,
      aTargets : [ -1, -2 ]
    } ],
        bSort: false,
    responsive: true
  });
    
    $('#despesa-tbl').dataTable({
        dom: 'lBfrtip',
            buttons: [
                {
                  extend: 'excelHtml5',
                  title: 'despesa-excel-online-sisdespenda_' + new Date().yyyymmdd(),
                  exportOptions: {
                    columns: [ 0, 1, 2, 3, 4, 5 ]
                  }
                },
                {
                  extend: 'pdfHtml5',
                  orientation: 'landscape',
                  pageSize: 'LEGAL',
                  title: 'despesa-pdf-online-sisdespenda_' + new Date().yyyymmdd(),
                  exportOptions: {
                    columns: [ 0, 1, 2, 3, 4, 5 ]
                  },
                  customize : function(doc) {
                    doc.defaultStyle.alignment = 'center';
                    doc.styles.tableHeader.alignment = 'center';
                    doc.content[1].table.widths = 
                        Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                  }
                }
            ],
		pagingType : 'simple', // Remove a paginação por números das páginas
		aoColumnDefs : [ // Remove o item para ordenação dos dois últimos elementos
		{
			bSortable : false,
			aTargets : [ -1, -2 ]
		} ],
        bSort: false,
		responsive: true
	});
    
    $('#renda-tbl').dataTable({
        dom: 'lBfrtip',
            buttons: [
                {
                  extend: 'excelHtml5',
                  title: 'renda-excel-online-sisdespenda_' + new Date().yyyymmdd(),
                  exportOptions: {
                    columns: [ 0, 1, 2, 3, 4 ]
                  }
                },
                {
                  extend: 'pdfHtml5',
                  orientation: 'landscape',
                  pageSize: 'LEGAL',
                  title: 'renda-pdf-online-sisdespenda_' + new Date().yyyymmdd(),
                  exportOptions: {
                    columns: [ 0, 1, 2, 3, 4 ]
                  },
                  customize : function(doc) {
                    doc.defaultStyle.alignment = 'center';
                    doc.styles.tableHeader.alignment = 'center';
                    doc.content[1].table.widths = 
                        Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                  }
                }
            ],
		pagingType : 'simple', // Remove a paginação por números das páginas
		aoColumnDefs : [ // Remove o item para ordenação dos dois últimos elementos
		{
			bSortable : false,
			aTargets : [ -1, -2 ]
		} ],
        bSort: false,
		responsive: true
	});
           
	var relatorio = $('#despesa-real-mes-tbl, #despesa-real-ano-tbl, #renda-mes-tbl, #renda-ano-tbl, #evento-tbl').dataTable({
		order : [ [ 0, 'desc' ] ],
		pagingType : 'simple', // Remove a paginação por números das páginas
		aoColumnDefs : [ // Remove o item para ordenação dos dois últimos elementos
		{
			bSortable : false,
			aTargets : [ ]
		} ],
        dom: 'lBfrtip',
            buttons: [
                {
                  extend: 'excelHtml5',
                  title: 'relatorio-excel-online-sisdespenda_' + new Date().yyyymmdd()
                },
                {
                  extend: 'pdfHtml5',
                  orientation: 'landscape',
                  pageSize: 'LEGAL',
                  title: 'relatorio-pdf-online-sisdespenda_' + new Date().yyyymmdd(),
                  customize : function(doc) {
                    doc.defaultStyle.alignment = 'center';
                    doc.styles.tableHeader.alignment = 'center';
                    doc.content[1].table.widths = 
                        Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                  }
                }
            ]
	});
		
    relatorio.fnSort([[0, 'desc']]);    
        
	$('#despesa-fut-ano-tbl').dataTable({
		order : [ [ 0, 'desc' ] ],
		pagingType : 'simple', // Remove a paginação por números das páginas
		aoColumnDefs : [ // Remove o item para ordenação dos dois últimos elementos
		{
			bSortable : false,
			aTargets : [ ]
		} ],
        dom: 'lBfrtip',
            buttons: [
                {
                  extend: 'excelHtml5',
                  title: 'despfutura-excel-online-sisdespenda_' + new Date().yyyymmdd()
                },
                {
                  extend: 'pdfHtml5',
                  orientation: 'landscape',
                  pageSize: 'LEGAL',
                  title: 'despfutura-pdf-online-sisdespenda_' + new Date().yyyymmdd(),
                  customize : function(doc) {
                    doc.defaultStyle.alignment = 'center';
                    doc.styles.tableHeader.alignment = 'center';
                    doc.content[1].table.widths = 
                        Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                  }
                }
            ]
	});
	
	$('#despesa-fut-mes-tbl').dataTable({
        order : [ [ 0, 'desc' ] ],
		pagingType : 'simple', // Remove a paginação por números das páginas
		aoColumnDefs : [ // Remove o item para ordenação dos dois últimos elementos
		{
			bSortable : false,
			aTargets : [ ]
		} ]
	});	
	
	$('#despesa-futura-tbl').dataTable({
		pagingType : 'simple', // Remove a paginação por números das páginas
		aoColumnDefs : [ // Remove o item para ordenação dos dois últimos elementos
		{
			bSortable : false,
			aTargets : [ -1, -2 ]
		} ],
        bSort: false,
		responsive: true,
        dom: 'lBfrtip',
            buttons: [
                {
                  extend: 'excelHtml5',
                  title: 'despesa-excel-online-sisdespenda_' + new Date().yyyymmdd(),
                  exportOptions: {
                    columns: [ 0, 1, 2, 3, 4, 5 ]
                  }
                },
                {
                  extend: 'pdfHtml5',
                  orientation: 'landscape',
                  pageSize: 'LEGAL',
                  title: 'despesa-pdf-online-sisdespenda_' + new Date().yyyymmdd(),
                  exportOptions: {
                    columns: [ 0, 1, 2, 3, 4, 5 ]
                  },
                  customize : function(doc) {
                    doc.defaultStyle.alignment = 'center';
                    doc.styles.tableHeader.alignment = 'center';
                    doc.content[1].table.widths = 
                        Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                  }
                }
            ]
	});
    
    $('#relacao-mes-tbl, #relacao-ano-tbl').dataTable({		
		order : [ [ 0, 'desc' ] ],
		pagingType : 'simple', // Remove a paginação por números das páginas
		aoColumnDefs : [ // Remove o item para ordenação dos dois últimos elementos
		{
			bSortable : false,
			aTargets : [ ]
		} ],
        dom: 'lBfrtip',
            buttons: [
                {
                  extend: 'excelHtml5',
                  title: 'relacao-excel-online-sisdespenda_' + new Date().yyyymmdd()
                },
                {
                  extend: 'pdfHtml5',
                  orientation: 'landscape',
                  pageSize: 'LEGAL',
                  title: 'relacao-pdf-online-sisdespenda_' + new Date().yyyymmdd(),
                  customize : function(doc) {
                    doc.defaultStyle.alignment = 'center';
                    doc.styles.tableHeader.alignment = 'center';
                    doc.content[1].table.widths = 
                        Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                  }
                }
            ]
	});

    var dtSaldo = $('#saldo-tbl').dataTable({
        ordering: false, // Remove a ordenação
		pagingType : 'simple', // Remove a paginação por números das páginas
        dom: 'lBfrtip',
            buttons: [
                {
                  extend: 'excelHtml5',
                  title: 'saldo-excel-online-sisdespenda_' + new Date().yyyymmdd()
                },
                {
                  extend: 'pdfHtml5',
                  orientation: 'landscape',
                  pageSize: 'LEGAL',
                  title: 'saldo-pdf-online-sisdespenda_' + new Date().yyyymmdd(),
                  customize : function(doc) {
                    doc.defaultStyle.alignment = 'center';
                    doc.styles.tableHeader.alignment = 'center';
                    doc.content[1].table.widths = 
                        Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                  }
                }
            ]
	});
    
  // Posiciona os botões para exportar dados data table
  $('.dt-buttons').css('margin-left', '15px');
    
	$(window).load(function() {
		console.log('load depois do DOM!');
		if ($('#id_vl_renda').val() === null) {
			$('#id_vl_renda').val('');
		}

		if ($('#despesaId').val() === null) {
			$('#valorDespesa').val('');
		}
		
		$('#wait').css('display', 'none');
		$('#show_content').css('display', 'block');
	});
	
	$('.limpar').on('click', function() {
		// Limpa os campos de textos
		$('input[type=date], input[type=number], input[type=text], input[type=password]').each(function(index) {
			$(this).val('');
		});

		// Limpa o item selecionado
		$('select[id=id_cd_tipo_renda], select[id=id_cd_tipo_despesa]').val('');
	});	

    
    $('#alterSenhaForm').submit(function() {
        try {
            
            var senha = $('#senha').val();
            var nova_senha = $('#nova_senha').val();
            
            if (senha === '' || nova_senha === '') {
                
                 BootstrapDialog.show({
                    title: 'Atenção!',
                    message: 'As senhas devem ser preenchidas',
                    type: BootstrapDialog.TYPE_WARNING,
                    buttons: [{
                        label: 'entendi',
                        cssClass: 'btn-warning',
                        action: function(dialogItself){
                            dialogItself.close();
                        }
                    }]
                });
                
                return false;
                
            } else if (senha.length < 7 || nova_senha.length < 7) {

                 BootstrapDialog.show({
                    title: 'Atenção!',
                    message: 'As senhas devem ter no mínimo 7 caracteres',
                    type: BootstrapDialog.TYPE_WARNING,
                    buttons: [{
                        label: 'entendi',
                        cssClass: 'btn-warning',
                        action: function(dialogItself){
                            dialogItself.close();
                        }
                    }]
                });
                
                return false;
                
            } else if (senha !== nova_senha) {
                
                 BootstrapDialog.show({
                    title: 'Atenção!',
                    message: 'As senhas não conferem, por favor, digite a mesma senha',
                    type: BootstrapDialog.TYPE_DANGER,
                    buttons: [{
                        label: 'entendi',
                        cssClass: 'btn-danger',
                        action: function(dialogItself){
                            dialogItself.close();
                        }
                    }]
                });
                
                return false;

            } else {
                return true;
            }
            
        } catch (e) {
            console.log('ERRO ao alterar a senha: ' + e);
        }
    
    });
    
	/*** Validação de formulários ***/
	/*
	$('#tipoRendaForm, #tipoRendaAtualizacaoForm').validate({
        rules: {
        	ds_tipo_renda: {
                required: true
            }
        },
        messages: {
        	ds_tipo_renda: {
        		required: "Campo deve ser preenchido" 
        	}
        },
        highlight: function (element) {
            $(element).closest('.control-group').removeClass('success').addClass('error');
        },
        success: function (element) {
            element.addClass('valid')
                .closest('.control-group').removeClass('error').addClass('success');
        },
    	submitHandler: function(form) {
    		form.submit();
    	}
    });

	$('#rendaForm, #rendaAtualizacaoForm').validate({
        rules: {
        	dt_renda: {
                required: true
            },
            cd_tipo_renda: {
                required: true
            },
            vl_renda: {
                required: true
            }
        },
        messages: {
        	dt_renda: {
        		required: "Uma data deve ser definida" 
        	},
            cd_tipo_renda: {
                required: "Um valor deve ser selecionado"
            },
            vl_renda: {
                required: "Campo deve ser preenchido"
            }
        },
        highlight: function (element) {
            $(element).closest('.control-group').removeClass('success').addClass('error');
        },
        success: function (element) {
            element.addClass('valid')
                .closest('.control-group').removeClass('error').addClass('success');
        },
    	submitHandler: function(form) {
    		form.submit();
    	}
    });

	$('#despesaForm, #despesaAtualizacaoForm').validate({
        rules: {
        	dt_despesa: {
                required: true
            },
            vl_despesa: {
                required: true
            },
            cd_tipo_despesa: {
                required: true
            }
        },
        messages: {
        	dt_despesa: {
        		required: "Uma data deve ser definida" 
        	},
            vl_despesa: {
                required: "Campo deve ser preenchido"
            },
        	cd_tipo_despesa: {
                required: "Campo deve ser preenchido"
            }
        },
        highlight: function (element) {
            $(element).closest('.control-group').removeClass('success').addClass('error');
        },
        success: function (element) {
            element.addClass('valid')
                .closest('.control-group').removeClass('error').addClass('success');
        },
    	submitHandler: function(form) {
    		form.submit();
    	}
    });
	
    $('#tipoDespesaForm, #tipoDespesaAtualizacaoForm').validate({
        rules: {
            ds_tipo_despesa: {
                required: true
            }
        },
        messages: {
            ds_tipo_despesa: {
                required: "Campo deve ser preenchido" 
            }
        },
        highlight: function (element) {
            $(element).closest('.control-group').removeClass('success').addClass('error');
        },
        success: function (element) {
            element.addClass('valid')
                .closest('.control-group').removeClass('error').addClass('success');
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
	
    $('#alterSenhaForm').validate({
        rules: {
            senha: {
                required: true,
                minlength: 7,
            },
            nova_senha: {
                required: true,
                minlength: 7,
                equalTo : "#senha"
            }
        },
        messages: {
            senha: {
                required: "Campo deve ser preenchido",
                minlength: "A senha deve ter pelo menos 7 caracteres"                
            },
            nova_senha: {
                required: "Campo deve ser preenchido",
                minlength: "A senha deve ter pelo menos 7 caracteres" ,
                equalTo: "A senha não confere. Por favor, digite o mesmo valor novamente"
            }
        },
        highlight: function (element) {
            $(element).closest('.control-group').removeClass('success').addClass('error');
        },
        success: function (element) {
            element.addClass('valid')
                .closest('.control-group').removeClass('error').addClass('success');
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
    */
	/*** FIM Validação de formulários ***/
});

function confirmarOperacao(endpoint, tipo, mensagem) {
	
	var tipo_ = BootstrapDialog.TYPE_PRIMARY;
	
	if (tipo === 'danger') {
		tipo_ = BootstrapDialog.TYPE_DANGER;
	}
	
	//var botao = 'btn-primary'
	var botao = 'btn-' + tipo;
	
	BootstrapDialog.confirm({
        title: 'Confirma?',
        message: mensagem,
        //type: BootstrapDialog.TYPE_PRIMARY, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
        type: tipo_,
        closable: true, // <-- Default value is false
        draggable: true, // <-- Default value is false
        btnCancelLabel: 'depois', // <-- Default value is 'Cancel',
        btnOKLabel: 'sim', // <-- Default value is 'OK',
        btnOKClass: botao, // <-- If you didn't specify it, dialog type will be used,
        callback: function(result) {
            if (result) {
            	window.location.href = endpoint;
            }
        }
    });
}

Date.prototype.yyyymmdd = function() {
	  var mm = this.getMonth() + 1; // getMonth() is zero-based
	  var dd = this.getDate();
      return [this.getFullYear(), !mm[1] && '0', mm, dd].join(''); // padding
	  //return [this.getFullYear(), !mm[1] && '0', mm, !dd[1] && '0', dd].join(''); // padding
};

function recuperarRegistroPorMes(endpoint, mes, indice) {
	try {
        console.log('indice: ' + indice);
        if (indice == '0') {
            window.location.href = endpoint + mes;
        } else {
            window.location.href = endpoint + mes + '/' + indice;
        }
		
	} catch (e) {
		console.log(' ---> Erro: ' + e);
	} 
}

function recuperarRegistroPorAno(endpoint, ano) {
	try {

        window.location.href = endpoint + ano;
		
	} catch (e) {
		console.log(' ---> Erro: ' + e);
	} 
}