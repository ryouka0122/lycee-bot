#!/bin/sh

SCRIPT_DIR=$(cd $(dirname $0); pwd)

for name in `cat hubot.lst`
do
  cd "${SCRIPT_DIR}/${name}"
  echo -n "running hubot (${name}) ..."
  sh bin/hubot --adapter slack
  if [ "$?" == "0" ] ; then
    echo "[SUCCESS]"
  else
    echo "[FAIL]"
  fi
done
