;(function( $, window, document, undefined ) {

    $(document).ready(function() {
    //定义用户信息修改确认对话框
        if( $.fn.dialog  ) {
            $("#userinfo_change_ensure_dialog").dialog({
                autoOpen: false,
                title: "修改信息确认",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: [{
                    id:"ensure_change",
                    text:"确定",
                    click:function(){
                        $("#register-form").submit();
                        $("#userinfo_change_ensure_dialog").dialog("close");
                    }
                    },
                    {
                    id:"cancel_change",
                    text:"取消",
                    click:function(){
                        $("#userinfo_change_ensure_dialog").dialog("close");
                    }
                }]
            });
        }
        //初始化job1和job2的两个选择框
        $('.mws-form .mws-form-item>.ui-spinner,.mws-form .mws-form-item>.select2-container,.mws-form .mws-form-item>.fileinput-holder .fileinput-preview').attr('style','width:73%;padding-right: 89px;');
        $("#job1").jCombo("/register/job/",{
            initial_text : "-右边为您当前设置的职业-",
        });
        $('#job2').jCombo('/register/job?id=',{
            parent:'#job1',
            initial_text : "--请选择--",
        });
        //如果选择的是自己输入问题的话，第二个输入框中必须要输入值，将其只读属性去掉
        question = $('#select_question').val()
        if (question == "自己输入问题") $('#custom_question').attr('readonly',false);
        $('#select_question').change(function(){
            if($('#select_question option:selected').text() == '自己输入问题'){
                $('#custom_question').attr('readonly',false);
            }else{
                $('#custom_question').attr('readonly',true).val('');
            }
        });
        //点击确认按钮时调用对话框
        $('#submit_info').bind("click",function(event){
            $("#userinfo_change_ensure_dialog").dialog("open");
            event.preventDefault();
        });
        //点击重置按钮时将一些值清空
        $('#reset').bind("click",function(){
            $("#mobile").attr("value","");
            $("#email").attr("value","");
            $("#telephone").attr("value","");
            $("#workspace").attr("value","");
            $("#address").attr("value","");
        });
    });

}) (jQuery, window, document);
