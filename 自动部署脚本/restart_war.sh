#!/bin/bash
set -x

#定义目录
PWDDIR=$(cd `dirname $0`;pwd)

SCRIPT_NAME="service_war.sh" 



#停止当前服务
/bin/bash ${PWDDIR}/${SCRIPT_NAME} stop  &>/dev/null
if [ "$?"  -eq 0 ];then
    #删除检测日志文件
    [ -f ${PWDDIR}/*.log ] && /bin/rm `ls ${PWDDIR}/*.log` -f 
    #删除当前包解压的文件夹
    for i in `ls ${PWDDIR}`
    do
        i=${PWDDIR}/${i}
        [ -f ${i} ] && continue  
        if [[ ${i##*/} != "backup" && ${i##*/} != "new"  && ${i##*/} != "lib" ]];then
            /bin/rm ${i} -rf
            [ "$?" -eq 0 ] && break
        fi
    done
fi

(cd ${PWDDIR}; /bin/bash ${PWDDIR}/${SCRIPT_NAME} start  &>/dev/null)



