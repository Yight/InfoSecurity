(function($) {
	$(document).ready(function() {	
	    var sendverifycode = 0;
		$("#mws-login-form form").validate({
			rules: {
				username: {required: true}, 
				password: {required: true},
			}, 
			errorPlacement: function(error, element) {  
			}, 
			invalidHandler: function(form, validator) {
				if($.fn.effect) {
					$("#mws-login").effect("shake", {distance: 6, times: 2}, 35);
				}
			}
		});
		
		if($.fn.placeholder) {
			$('[placeholder]').placeholder();
		};
		
		
		$("#fogetpwd").click(function(){
		    username=$("#username").val();
		    if (username == "")
		        alert("请输入用户名");
		    else
		        location.href = '/accounts/fogetpwd/?username='+username;
		});
		
		$("#register").click(function(){
		    location.href = '/accounts/register/';
		});
		
		$("#phonecerify").click(function(){
		    if($("#username").val()){
		        $.getJSON('/accounts/sendverifycode/',{
                    username:$("#username").val(),
                },
                function(data) {
                    sendverifycode = data;
                    alert(sendverifycode);
                });
		    }else{
		        alert("请输入用户名");
		    }
	    });
	});
}) (jQuery);
