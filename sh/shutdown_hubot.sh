#!/bin/sh

CUR_DIR=$(cd $(dirname $0) ; pwd)

CNT=`forever list | fgrep -f ${CUR_DIR}/hubot.lst | wc -l`
if [ "$CNT" == "0" ] ; then
  echo "already stoped all bot ..."
  exit 0
fi

forever stopall
exit $?
