
def upstream_parse(fname):
    tmp_config = {
        "{": 0
    }
    upstream_dict ={}
    with open(fname) as fp:
        for line in fp:
            line = line.strip()
            if "{" in line:
                tmp_config["{"] += 1
            if line.startswith("upstream"):
                #upstream_name = line.lstrip().split()[1]
                upstream_name = line.split()[1]
                upstream_dict[upstream_name] = []

                continue
            if tmp_config.get("{") >0:
                if line.startswith("server") and "{" not in line:
                    ip = line.strip(";\n").split()[1]
                    if not ip[0].isdigit(): continue
                    upstream_dict[upstream_name].append(ip)

            if "}" in line:
                tmp_config["{"] -= 1
    return upstream_dict

def sub_conf(fname):
    tmp_files = []
    with open(fname) as fp:
        for line in fp:
            line = line.strip()
            if line.startswith("include"):
                fnames = line.strip(";\n").split()[-1]
                tmp_files.append(fnames)
    return tmp_files

def server_name(fname):
    tmp_config = {
        "{": 0
    }
    upstream_dict ={}
    with open(fname) as fp:
        for line in fp:
            line = line.lstrip()
            if "{" in line:
                tmp_config["{"] += 1
            if "upstream" in line:
                upstream_name = line.lstrip().split()[1]
                upstream_dict[upstream_name] = []

                continue
            if tmp_config.get("{") >0:
                if line.startswith("server") and "{" not in line:
                    ip = line.strip(";\n").split()[1]
                    if not ip[0].isdigit(): continue
                    upstream_dict[upstream_name].append(ip)

            if "}" in line:
                tmp_config["{"] -= 1
    return upstream_dict

def proxy_parse(fname):
    tmp_config = {
        "{": 0
    }
    upstream_dict ={}
    listen_port = 0
    with open(fname) as fp:
        for line in fp:
            line = line.strip()
            if "{" in line:
                tmp_config["{"] += 1
            '''
                server_name： 可能不存在
                listen： 存在
            '''
            if "listen" in line and line.startswith("listen"):
                port = line.split()[1]
                upstream_dict[port] = {}
                listen_port = 1
                continue
            if listen_port:
                if "server_name" in line and line.startswith("server_name"):
                    server_name = line.split()[1]
                    upstream_dict[port][server_name] = []
                    listen_port = 0
                    continue
                else:
                    server_name = "localhost"
                    upstream_dict[port][server_name] = []
                    listen_port = 0 
                    continue
            '''
            if "server_name" in line and line.startswith("server_name"):
                #upstream_name = line.lstrip().split()[1]
                server_name = line.split()[1]
                #upstream_dict[port][server_name] = []
            '''
            #说明配置在段落内部
            if tmp_config.get("{") >0:
                if line.startswith("proxy_pass"):
              
                    ip = line.strip(";\n").split()[1]
                    upstream_dict[port][server_name].append(ip)

            if "}" in line:
                tmp_config["{"] -= 1
    return upstream_dict

    
def parse_subconf():
    import glob
    t = upstream_parse('nginx.conf')
    print(t)
    f_name = sub_conf('nginx.conf')
    for i in f_name:
        print(i)
        m = glob.glob(i)
        print('*'*10)
        for j in m:
            print(upstream_parse(j))
  
  
if __name__ == "__main__":
    t = proxy_parse('nginx.conf')
    print(t)
    parse_subconf()