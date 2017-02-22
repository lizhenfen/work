#!/bin/bash
#-*- coding:utf8 -*-

DATE=`date +%Y%m%d`
LOGDIR='/data/nginx/logs'
BACKDIR='/data/nginx/backlogs'
NGINXCMD='/data/nginx/sbin/nginx'
TARCMD='/bin/tar'

[ -d ${LOGDIR} ]  || exit 1
[ -d ${BACKDIR} ] && /bin/mkdir -p ${BACKDIR}

# mkdir backup dir every day
if [ ! -d ${BACKDIR}/${DATE} ]
then
    /bin/mkdir -p ${BACKDIR}/${DATE}
else
    exit 1
fi

for i in `ls ${LOGDIR}`
do
    /bin/mv ${LOGDIR}/${i} ${BACKDIR}/${DATE}/ &>/dev/null
done
${NGINXCMD} -s reload
