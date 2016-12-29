$(document).ready(function(){
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function(){};
    
    //���¶��巢�ͱ��� messageform �� submit �¼�
    $("#messageform").live("submit", function(){
        newMessage($(this));
        return False;
    });
    
    //���巢�ͱ��� messageform ��keypass�¼� �� ���»س�ֱ�ӷ���
    $("#messageform").live("keypass", function(e){
       if (e.KeyCode == 13){
            newMessage($(this));
            return False; 
       } 
    });
    
    //���°�ҳ��Ľ��������� message�Ŀؼ���
    $("#message").select();
    //��������ĺ���
    updater.start()
});

function newMessage(form){
    var message = form.formToDict();  //����jquery.fin.formToDict
    updater.socket.send(JSON.stringify(message));  //����json�ַ���
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