#!/bin/sh

#获取JAVA环境
[ -d /usr/local/jdk ] && export JAVA_HOME=/usr/local/jdk && export JRE_HOME=$JAVA_HOME/jre

#设置变量
SERVICE_DIR=$(cd `dirname $0`; pwd )  #当前服务器的目录
APP_NAME=${SERVICE_DIR##*/}    #获取当前APP名称
SERVICE_NAME=vats-service-${APP_NAME}
JAR_NAME=${SERVICE_NAME}\.jar
PID=${SERVICE_NAME}\.pid

case "$1" in
    start)
        nohup $JRE_HOME/bin/java -Xms512m -Xmx512m -jar $JAR_NAME >${APP_NAME}.log 2>&1 &
        echo $! > $PID
        #echo "=== start $SERVICE_NAME"
        ;;
    stop)
        kill `cat $PID`
        rm -rf $PID
        # "=== stop $SERVICE_NAME"
        sleep 5
		##
		## edu-service-aa.jar
		## edu-service-aa-bb.jar
        P_ID=`ps -ef | grep -w "$SERVICE_NAME" | grep -v "grep" | awk '{print $2}'`
        if [ "$P_ID" == "" ]; then
            echo "=== $SERVICE_NAME process not exists or stop success"
        else
            echo "=== $SERVICE_NAME process pid is:$P_ID"
            echo "=== begin kill $SERVICE_NAME process, pid is:$P_ID"
            kill -9 $P_ID
        fi
        ;;

    restart)
        /bin/bash $0 stop
        sleep 2
        /bin/bash $0 start
        echo "=== restart $SERVICE_NAME"
        ;;

    *)
        ## restart
        /bin/bash $0 stop
        sleep 2
        /bin/bash $0 start
        ;;
esac
exit 0

