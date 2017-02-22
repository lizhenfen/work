#!/bin/bash

INOTIFY_FILE=./inotify.conf

inotifywait --fromfile ${INOTIFY_FILE} -r -m  -e close_write | while read DIR FLAG FILE
do
  if [[ ${FILE##*.} != "war" && ${FILE##*.} != "jar" ]]
  then
     continue
  fi
  FILE=`echo ${FILE} | cut -d. -f1`
  ansible-playbook -i hosts deploy.yaml -e "work_dir=${DIR} service_name=${FILE}"
done
