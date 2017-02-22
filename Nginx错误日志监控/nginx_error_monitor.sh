#!/bin/bash

ERROR_FILE=/data/nginx/logs/error.log
# -m: ǰ̨�������
# -d: ��-mһ������̨������أ���� -o file  ָ������ļ�
inotifywait -m -e close_write ${ERROR_FILE} | while read LINE
do
    content=`tail -n 1 ${ERROR_FILE}`
    python nginx_smtp.py ${content}
done
