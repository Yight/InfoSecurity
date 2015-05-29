$("#download").click(function() {
    var userid = $("#userid").val();
    var status = "1"
    if(status=='0') {
        alert("证书正在生成，请等待...");
        window.location.reload();
    }
    else{
        if(userid!="")
        {
            var url =  "/static/CA/"+userid+"/setup.zip";                              //only for test
            // alert(url);
            var win = window.open(url,"_blank");                        //open the url
            if(win!=null){
                win.document.execCommand('SaveAs');                  //download
        }
        else
            alert("打开窗口失败!");
        }
        else
        {
            alert("用户ID不存在!");
        }
    }
    return false;
});