#!/bin/bash

IP=$3
PORT=$4
REDISCMD="redis-cli -h $IP -p $PORT"

redis_discovery(){
    FIRST=1
    ipinfo=`sudo ss -ltnp | grep redis-server | awk -F' ' '{print $4}'`
    echo -e "{\n"
    echo  -e "\t\"data\":[\n"
    for i in ipinfo
    do
        ip=`echo ${i} | awk -F':' '{print $1}' `
        port=`echo ${i} | awk -F':' '{print $2}' `
        if [ ${ip} != '0.0.0.0' ];then
            ip=127.0.0.1
        fi
        [[ ${FIRST} == 1 ]]  && echo "\t,\n"
        FIRST=0
        echo -e "\t\t{\n"
        echo -e "\t\t\"{#REDISIP}\":\"${ip}\",\n"
        echo -e "\t\t\"{#REDISPORT}\":\"${port}\"\n"
        echo -e "\t\t}\n"
    
    done

    echo -e "\t]\n"
    echo -e "}\n"
}
redis_status(){

    case $2 in
        Mem)
            mem=`${REDISCMD} info | grep "used_memory:" | cut -d: -f2`
            echo $mem
            ;;
        Version)
            version=`${REDISCMD} info | grep "redis_version:" | cut -d: -f2`
            echo $version
            ;;
        Uptime)
            uptime=`${REDISCMD} info | grep "uptime_in_seconds:" | cut -d: -f2`
            echo $uptime
            ;;
        Client_num)
            client_num=`${REDISCMD} info | grep "connected_clients:" | cut -d: -f2`
            echo $client_num
            ;;
        Receive_bytes)
            receive_bytes=`${REDISCMD} info | grep "total_net_input_bytes:" | cut -d: -f2`
            echo $Receive_bytes
            ;;
        Send_bytes)
            Send_bytes=`${REDISCMD} info | grep "total_net_output_bytes:" | cut -d: -f2`
            echo $Send_bytes
            ;;
        Rejected_connections)
            rejected_connections=`${REDISCMD} info | grep "rejected_connections:" | cut -d: -f2`
            echo $rejected_connections
            ;;   
        Hits_num)
            hits_num=`${REDISCMD} info | grep "keyspace_hits:" | cut -d: -f2`
            echo $hits_num
            ;;           
        Lose_num)
            lose_num=`${REDISCMD} info | grep "keyspace_misses:" | cut -d: -f2`
            echo $Lose_num
            ;; 
        *)
            echo "Usage: $0 status Mem|Version|Uptime|Client_num|Receive_bytes|Rejected_connections|Hits_num|Lose_num"
            ;;
    esac
}

if [ "$1" == 'discovery' ];then
    redis_discovery
fi
if [ "$1" == 'status' ];then
    redis_status $2
fi


