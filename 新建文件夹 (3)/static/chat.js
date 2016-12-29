$(document).ready(function(){
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function(){};
    
    //重新定义发送表单的 messageform 的 submit 事件
    $("#messageform").live("submit", function(){
        newMessage($(this));
        return False;
    });
    
    //定义发送表单的 messageform 的keypass事件 ， 按下回车直接发送
    $("#messageform").live("keypass", function(e){
       if (e.KeyCode == 13){
            newMessage($(this));
            return False; 
       } 
    });
    
    //重新把页面的焦点设置在 message的控件上
    $("#message").select();
    //调用下面的函数
    updater.start()
});

function newMessage(form){
    var message = form.formToDict();  //调用jquery.fin.formToDict
    updater.socket.send(JSON.stringify(message));  //生成json字符串
    form.find("input[type=text]").val("").select();
}

jQuery.fn.fromToDict = function(){
    var fields = this.serializeArray();
    var json = {}
    for (var i=0; i< fields.length; i++){
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

var updater = [
    socket: null,
    
    start: function(){
        
    },
]