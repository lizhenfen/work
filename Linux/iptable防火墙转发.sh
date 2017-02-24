Iptables -X
Iptables -F
Iptables -Z
Iptables -t nat -I PREROUTING -d 192.168.15.68 -p tcp --dport 5222 -j DNAT -to 192.168.15.127:5222
Iptables -t nat -A POSTROUTING -s 0/0 -j MASQUERADE
Iptables -t nat -A POSTROUTING -d 192.168.15.68 -p tcp --dport 5222 -j SNAT -to 192.168.15.127:5222
