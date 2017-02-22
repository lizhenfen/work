#!/usr/bin/bash

nginx_active_num(){
     curl 127.0.0.1:5000/nginx_status -s | sed -n '1p' | awk -F' ' '{print $3}'
}

nginx_request_num() {
    r1=`curl 127.0.0.1:5000/nginx_status -s | sed -n "3p" | awk '{print $1}'`
    sleep 1
    h1=`curl 127.0.0.1:5000/nginx_status -s | sed -n "3p" | awk '{print $2}'`
    echo $(( ${h1} - ${r1} ))
}

nginx_read_num() {
   curl 127.0.0.1:5000/nginx_status -s | sed -n "\$p" | awk '{print $2}'
}

nginx_write_num() {
   curl 127.0.0.1:5000/nginx_status -s | sed -n "\$p" | awk '{print $2}'
}
nginx_wait_num() {
   curl 127.0.0.1:5000/nginx_status -s | sed -n "\$p" | awk '{print $2}'
}

$1
