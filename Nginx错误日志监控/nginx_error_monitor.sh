#!/bin/bash

ERROR_FILE=/data/nginx/logs/error.log
# -m: 前台持续监控
# -d: 和-m一样，后台持续监控，配合 -o file  指定输出文件
inotifywait -m -e close_write ${ERROR_FILE} | while read LINE
do
    content=`tail -n 1 ${ERROR_FILE}`
    python nginx_smtp.py ${content}
done
