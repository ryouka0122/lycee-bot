#!/bin/sh

BASE_DIR=$(cd $(dirname $0)/..; pwd)
LOG_DIR="/app/devops/logs"

for NAME in `cat ${BASE_DIR}/sh/hubot.lst` ; do
  SCRIPT_DIR=${BASE_DIR}/${NAME}

  cd ${SCRIPT_DIR}

  sh ./bin/hubot --adapter slack
  RET=$?
  
  echo -n "running hubot (${NAME}) ..."
  if [ "${RET}" == "0" ] ; then
    echo "[SUCCESS]"
  else
    echo "[FAIL]"
  fi

done

