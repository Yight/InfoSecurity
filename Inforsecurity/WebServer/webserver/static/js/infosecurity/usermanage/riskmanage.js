;(function( $, window, document, undefined ) {
     $(document).ready(function() {
         $("#settingsubmit").bind("click", function (event) {
             var email_risk = $("#email_check").val()
             var ip_risk = $("#ip_check").val()
             var url_risk = $("#url_check").val()
            if(email_risk<30 || email_risk>100 || ip_risk<30 || ip_risk>100 || url_risk<30 || url_risk>100)
            {
                var message = '风险值应该为30-100间的数字';
                $("#errors").html(message).show();
                event.preventDefault();
            }
         })
     })
}) (jQuery, window, document);
