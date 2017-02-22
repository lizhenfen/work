#!/usr/bin/bash
#-*- coding: utf-8 -*-
#author: 
#date: 2016-10-09

HOST="192.168.15.191"
PORT=3306
USER=root
PASSWD=123456
DATE=`date +"%Y-%m-%d"`
DATADIR=/data
BACKUPCMD=`which mysqldump`

"$BACKUPCMD" -h${HOST} -p${PORT} -u${USER} -p${PASSWD}  -A -C --events | gzip > ${DATADIR}/mysql_${DATE}.sql.gz &>/dev/null
if [ "$?" -eq 0 ]
then
    echo "`date +"%Y-%m-%d"` mysql backup successful" | tee ${DATADIR}/state.txt
else
    echo "`date +"%Y-%m-%d"` mysql backup fail" | tee ${DATADIR}/state.txt





