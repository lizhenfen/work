#!/bin/bash
#-*- coding:utf8 -*-

DATE=`date +%Y%m%d`
LOGDIR='/home/lizhen/logs'
BACKDIR='/home/lizhen/backlogs'
NGINXCMD='/data/nginx/sbin/nginx'
TARCMD='/bin/tar'

[ -d ${LOGDIR} ]  || exit 1
[ -d ${BACKDIR} ] || exit 1

# mkdir backup dir every day
if [ ! -d ${BACKDIR}/${DATE} ]
then
    /bin/mkdir -p ${BACKDIR}/${DATE}
else
    exit 1
fi

LOG_TAR(){
    
}

for i in `ls ${LOGDIR}`
do
    /bin/mv ${i} ${BACKDIR}/${DATE} &>/dev/null
done
${NGINXCMD} -s reload
