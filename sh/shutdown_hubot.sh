#!/bin/sh

CNT=`forever list | fgrep -f hubot.lst | wc -l`
if [ "$CNT" == "0" ] ; then
  echo "already stoped all bot ..."
  exit 0
fi

forever stopall

