#!/bin/bash
# zookeeper and kafka  start the two service and stop them
#chkconfig: 2345 88 22
#description:  the scripts for start zookeeper , kafka
#                              stop  kafka,  zookeeper

APPDIR="/opt/kafka8"
ZKSTART=${APPDIR}/bin/zookeeper-server-start.sh
ZKSTOP=${APPDIR}/bin/zookeeper-server-stop.sh
KAFSTART=${APPDIR}/bin/kafka-server-start.sh
KAFSTOP=${APPDIR}/bin/kafka-server-stop.sh

ZKCONF=${APPDIR}/config/zookeeper.properties
KAFCONF=${APPDIR}/config/server.properties

[ ! -d ${APPDIR} ] && (echo "${APPDIR} is not exists"; exit 1)

do_zk_start(){
    nohup ${ZKSTART} ${ZKCONF} &>/dev/null &
    if [ $? -eq 0 ];then
        sleep 1
        echo "zookeeper start successfully"
        exit 0
    fi
}
do_zk_stop(){
    ps ax | grep -i 'zookeeper' | grep -v grep | awk '{print $1}' | xargs kill -SIGINT  &>/dev/null
    [ $? -eq 0 ] && (sleep1;echo "zookeeper stop successfully"; exit 0 ) 
}
do_kf_start(){
    nohup ${KAFSTART} ${KAFCONF} &>/dev/null &
    if [ $? -eq 0 ];then
        sleep 1
        echo "kafka start successfully"
        exit 0
    fi
}
do_kf_stop(){
    ps ax | grep -i 'kafka\.Kafka' | grep java | grep -v grep | awk '{print $1}' | xargs kill -SIGINT &>/dev/null
    [ $? -eq 0 ] && (sleep1;echo "kafka stop successfully"; exit 0 ) 
}
do_restart(){
    do_zk_stop
    do_kf_stop
    do_zk_start
    do_kf_start
}
case $1 in
    start)
        do_zk_start
        do_kf_start
        ;;
    stop)
        do_kf_stop
        do_zk_stop
        ;;
    restart)
        do_restart
        ;;
    *)
        echo "Usage: $0 [start|stop|restart]"
        exit 2
        ;;
esac