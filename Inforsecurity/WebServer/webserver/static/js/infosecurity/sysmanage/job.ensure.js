;(function( $, window, document, undefined ) {
    $(document).ready(function(){
    //定义删除job的确认对话框
        if( $.fn.dialog  ) {
            $("#delete_top_ensure_dialog").dialog({
                autoOpen: false,
                title: "删除大类确认",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: [{
                    id:"t_ensure_delete",
                    text:"确定",
                    click:function(){
                        $("#delete_top").submit();
                    }
                    },
                    {
                    id:"t_cancel_delete",
                    text:"取消",
                    click:function(){
                        $("#delete_top_ensure_dialog").dialog("close");
                    }
                }]
            });
            $("#delete_sub_ensure_dialog").dialog({
                autoOpen: false,
                title: "删除小类确认",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: [{
                    id:"s_ensure_delete",
                    text:"确定",
                    click:function(){
                        $("#delete_sub").submit();
                    }
                    },
                    {
                    id:"s_cancel_delete",
                    text:"取消",
                    click:function(){
                        $("#delete_sub_ensure_dialog").dialog("close");
                    }
                }]
            });
        }
        //以下是实现当没有选择或输入增加或删除的类别时给出提示
        $("#add_top_category_click").bind("click", function (event) {
            var add_top_category = $("#add_top_category").val()
            if (!add_top_category){
                var message = '请输入你要添加的大类';
                $("#errors").html(message).show();
                event.preventDefault();
                }
            });
        $("#add_sub_category_click").bind("click", function (event) {
            var add_sub_category = $("#add_sub_category").val()
            var add_sub_category_top = $("#add_sub_category_top").val()
            if(!(add_top_category && add_sub_category_top)){
                var message = '请输入你要添加的小类';
                $("#errors").html(message).show();
                event.preventDefault();
                }
            });
        $("#delete_top_category_click").bind("click", function (event) {
            var delete_top_category = $("#delete_top_category").val()
            if (!delete_top_category){
                var message = '请输入你要删除的大类';
                $("#errors").html(message).show();
                event.preventDefault();
                }
            else{
                $("#delete_top_ensure_dialog").dialog("open");
                event.preventDefault();
            }
            });
        $("#delete_sub_category_click").bind("click", function (event) {
            var delete_sub_category = $("#delete_sub_category").val()
            var delete_sub_category_top = $("#delete_sub_category_top").val()
            if (delete_sub_category && delete_sub_category_top){
                $("#delete_sub_ensure_dialog").dialog("open");
                event.preventDefault();
                }
            else{
                var message = '请输入你要删除的小类';
                $("#errors").html(message).show();
                event.preventDefault();
                }
            });
    });
}) (jQuery, window, document);
