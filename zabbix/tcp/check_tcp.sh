#!/bin/bash

tcp_discovery(){
    FIRST=0
    local IFS=$'\n'
    #ss -ltnp | awk -F' ' 'NR>2 {print $4}' | awk -F':' '{print $NF}' | uniq
    #tcpinfo=`sudo  ss -ltnp | awk -F' ' 'NR>2 {print $4,$NF}' `
    tcpinfo=`sudo ss -ltnp | awk -F' ' 'NR>2 {print $4}' | awk -F':' '{print $NF}' | sort | uniq `
    echo -e "{"
    echo  -e "\t\"data\":["
    for i in ${tcpinfo}
    do
        IFS=$' \t\n'
        #port=`echo ${i} | awk -F' ' '{print $1}' | awk -F':' '{print $NF}'`
        #program=`echo ${i} | awk -F':' '{print $NF}'`
        [[ ${FIRST} == 1 ]]  && echo -e ","
        FIRST=1
        echo -e "\t\t{"
        echo -e "\t\t\"{#PORT}\": ${i},"
        #echo -e "\t\t\"{#PROGRAM}\": ${program}\n"
        echo -en "\t\t}"
    
    done

    echo -e "\n\t]"
    echo -e "}"
}

if [ "$1" == 'discovery' ];then
    tcp_discovery
fi
if [ "$1" == 'status' ];then
    redis_status $2
fi


