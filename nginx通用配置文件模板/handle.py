
def filehandle(template_name, save__file_name, project_name=None, template_param=None):
    
    project_path = os.path.join(TEMPLATE_PATH, project_name)
    loader = template.Loader(project_path)
    t = loader.load(template_name)
    with open(save__file_name, 'wb') as fd:
        fd.write(t.generate(**template_param))
        
def check_url(url):
    '''
            初始URL： https://192.168.15.37:10210/vats-api-order/service/v1/order.create
        重定向的URL:  https://apis.vats.com.cn/order/service/v1/order.create
        接受参数:
            st = "192.168.15.37/vats-api-order/xxx/pp" 
        check_url(st)
    '''
    res_dict = {}
    domain_ip, domain_uri, other_uri = url.split("/", maxsplit=2)
    if ":" in domain_ip:
        ip, port = domain_ip.split(":")
        port = int(port)
    else:
        ip = domain_ip
        port = 80
        
    if "-"  in domain_uri:
        uri = domain_uri.split("-")[-1]
    else:
        uri = domain_uri
    res_dict = {
                "ip": ip,
                "port": port,
                "uri": uri
                }    
    return res_dict
    
    
   