#!/bin/bash

tcp_discovery(){
    FIRST=0
    #ss -ltnp | awk -F' ' 'NR>2 {print $4}' | awk -F':' '{print $NF}' | uniq
    tcpinfo=`sudo  ss -ltnp | awk -F' ' 'NR>2 {print $4}' | awk -F':' '{print $NF}' | uniq `
    echo -e "{\n"
    echo  -e "\t\"data\":[\n"
    for i in ${tcpinfo}
    do
        #port=`echo ${i} | awk -F' ' '{print $3}' | awk -F':' '{print $2}' `
        [[ ${FIRST} == 1 ]]  && echo -e "\t,\n"
        FIRST=1
        echo -e "\t\t{\n"
        echo -en "\t\t\"{#PORT}\": ${i}\n"
        echo -e "\t\t}\n"
    
    done

    echo -e "\t]\n"
    echo -e "}\n"
}

if [ "$1" == 'discovery' ];then
    tcp_discovery
fi
if [ "$1" == 'status' ];then
    redis_status $2
fi


