#!/bin/bash
set -x

TOMCATSHELL="/home/apache-tomcat/bin/catalina.sh"

for dname in `docker ps | awk -F" " 'NR>1{print $NF}'`
do
    `docker stop ${dname}` &>/dev/null
    sleep 1
done
sleep 1

for dname in `docker ps -a | awk -F" " 'NR>1 {print $NF}'`
do
   `docker start ${dname} &>/dev/null`
   if ${dname} == "lbs01";then
       `docker exec ${dname} sed -i '$a192.168.15.200 kafka' /etc/hosts`
   fi
   sleep 1
   `docker exec ${dname} ${TOMCATSHELL} start &>/dev/null` 
done

sleep 1

echo "successfully restarted"
