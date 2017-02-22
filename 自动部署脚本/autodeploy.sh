#!/bin/bash
set -x

#定义目录
PWDDIR=$(cd `dirname $0`;pwd)
BACKUP_DIR="${PWDDIR}/backup"
PACKAGE_DIR="${PWDDIR}/new"
CMD="/bin/mv"

#判断是否包是否存在
if [ -f ${PACKAGE_DIR}/*.war ];then
    SCRIPT_NAME="service_war.sh" 
    PACKAGE_NAME=`ls ${PACKAGE_DIR}/*.war`
fi
if [ `ls ${PACKAGE_DIR}/*.jar 2>/dev/null | wc -l` -ge 1 ];then
    SCRIPT_NAME="service_jar.sh" 
    /bin/rm `ls ${PACKAGE_DIR}/*sources*.jar` -rf
    PACKAGE_NAME=`ls ${PACKAGE_DIR}/*.jar`
    [ -x  ${PACKAGE_DIR}/lib ] && /bin/cp -ap ${PACKAGE_DIR}/lib ${PWDDIR}
fi

# 若包不存在，退出部署
if [ -z ${SCRIPT_NAME} ];then
    exit 1
fi
if [ -z ${PACKAGE_NAME} ];then
    exit 1
fi

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

# backup the war or jar
[ ! -x ${BACKUP_DIR} ] && mkdir -p ${BACKUP_DIR}
${CMD} "${PWDDIR}/${PACKAGE_NAME##*/}" ${BACKUP_DIR} &>/dev/null

# pull or push new package 
/bin/cp ${PACKAGE_NAME} ${PWDDIR}

[ $? -ne 0 ] && exit 1
(cd ${PWDDIR}; /bin/bash ${PWDDIR}/${SCRIPT_NAME} start  &>/dev/null)



