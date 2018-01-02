/**
 * 
 */
$(function () {
	
	console.log('ok!');

	$(window).load(function() {
		console.log('load depois do DOM!');
	});
		
	$('.limpar').on('click', function() {
		// Limpa os campos de textos
		$('input[type=text], input[type=password]').each(function(index) {
			$(this).val('');
		});
	});	
	
	$('#logonForm').validate({
        rules: {
        	username: {
                required: true
            },
            password: {
                required: true
            },
            valorCaptcha: {
                required: true
            }
        },
        messages: {
        	username: {
        		required: "Campo deve ser preenchido" 
        	},
        	password: {
        		required: "Campo deve ser preenchido" 
        	},
        	valorCaptcha: {
        		required: "Campo deve ser preenchido" 
        	}
        },
        highlight: function (element) {
            $(element).closest('.control-group').removeClass('success').addClass('error');
        },
    	submitHandler: function(form) {
    		form.submit();
    	}
    });
	
});