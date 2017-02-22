#!/bin/bash

PWDDIR=$(cd `dirname $0`;pwd)

[ -f ${PWDDIR}/appclient.conf ]  && . ${PWDDIR}/appclient.conf || PORT=8080
. /etc/init.d/functions 

SERVICE_NAME=${PWDDIR##*/}
SERVICE_IMAGE=base/tomcat-7
DOCKER_ADDR=192.168.15.198:5000
REMOTE_IMAGE="${DOCKER_ADDR}/${SERVICE_IMAGE}"
IMAGENUMS=`docker images | grep "${SERVICE_IMAGE}" | wc -l`
FULL_SERVICE=vats-api-${SERVICE_NAME}
DATADIR=${PWD}
DOCKER_LOG="${PWDDIR}/${FULL_SERVICE}.log"

[ -f ${DOCKER_LOG} ] && (/bin/rm -rf ${DOCKER_LOG})


# ------ images check ----------
if [ "$IMAGENUMS" -lt 1 ];then
    docker pull ${REMOTE_IMAGE} &>/dev/null
    RETVAL=$?
    [ "$RETVAL" -ne 0 ] && echo "remote images not exists, check it"; exit 2
fi

#------- service manager ---------------
SV=$1

check_logs(){
    timestamp=`date +%s`
    COUNT=0
    while true
    do
        docker logs --since=${timestamp} ${FULL_SERVICE} >> ${DOCKER_LOG}
        if [ `grep "Server startup" ${DOCKER_LOG} | wc -l` -ge 1 ] ; then
            return 0
        fi
        if [ `grep "initialization completed" ${DOCKER_LOG} | wc -l` -ge 1 ]; then
            break
        fi
        if [ $(( ${COUNT} - 100 )) -ge 0 ];then
            echo "${SERVICE_NAME} start failed"
            return 1
        fi
        timestamp=`date +%s`
        COUNT=$(( COUNT + 1 ))
        sleep 2
    done 
}

start1(){
    if [ `docker ps | grep ${FULL_SERVICE} | wc -l` -eq 1 ];then
            echo "${FULL_SERVICE} started"
    elif [ `docker ps -a | grep ${FULL_SERVICE} | wc -l` -eq 1 ]
    then
            docker start ${FULL_SERVICE} &>/dev/null
    else
        if [ `lsof -i:$PORT | wc -l` -ge 1 ];then
            echo "$PORT has started, check it."
            exit 1
        fi
        docker run -d --name ${FULL_SERVICE} --net=host -e HTTP_PORT=$PORT -v ${DATADIR}:/webapps ${SERVICE_IMAGE} &>/dev/null
    fi 
    check_logs
    if [ $? -eq 0 ];then
        echo "${FULL_SERVICE} start successfully."
    else
        echo "${FULL_SERVICE} start failed."
    fi
}

stop1(){
    if [ `docker ps | grep ${FULL_SERVICE} | wc -l` -eq 0 ];then
        if [ `docker ps | grep ${FULL_SERVICE} | wc -l` -eq 0 ];then
            echo "${FULL_SERVICE} stoped"
        fi
    else
        echo "${FULL_SERVICE} stopping"
        docker stop ${FULL_SERVICE} &> /dev/null
        while true
        do
            [ `docker ps | grep ${FULL_SERVICE} | wc -l`  -eq 0 ] && break || sleep 4;
        done
        [ ! -z "${FULL_SERVICE}" ] && rm ${FULL_SERVICE} -rf || echo "${FULL_SERVICE} can't rm, check it"
        echo "${FULL_SERVICE} stoped"
       
    fi
}

restart(){
    stop1
    start1
}


case "${SV}" in
    start)
        start1
        ;;
    stop)
        stop1
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 [start|stop|restart]"
        ;;
esac     
        
