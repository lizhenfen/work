import time

def get_pid_current_flow(pid):
    '''
        Inter-|   Receive                                                |  Transmit
        face  |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
        ens192: 6426490453 40296303    0 3364    0     0          0         0 3038629943 31022223    0    0    0     0       0          0
    '''
    pid_net_info = {}
    with open('/proc/%s/net/dev' % pid) as fp:
        data = fp.read().strip('\n').split('\n')
        for line in data:
            if "|" in line:
                continue
            net_flow = line.split()
           
            net_card_name = net_flow[0].strip(": ")
            net_recv_bytes = net_flow[1]
            net_recv_drop  = net_flow[4]
            net_send_bytes = net_flow[9]
            pid_net_info = {
                            'net_card_name': net_card_name,
                            'net_recv_bytes': net_recv_bytes,
                            'net_recv_drop': net_recv_drop,
                            'net_send_bytes': net_send_bytes
                            }
        return  pid_net_info

def caculate_pid_flow(pid, interval=1):
    first = get_pid_current_flow(pid)
    time.sleep(interval)
    curr  = get_pid_current_flow(pid)
    
        
if __name__ == "__main__":
    get_pip_flow(26375)