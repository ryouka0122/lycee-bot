#!/bin/sh

SHELL_DIR=$(cd $(dirname $0) ; pwd)

# -------------------------------------------
# check execute user
if [ "$(whoami)" != "ec2-user" ] ; then
  echo "this shell is only ec2-user."
  exit 1
fi

# -------------------------------------------
COMMAND=$1
HUBOT_NAME=$2

# -------------------------------------------
# validation

case ${COMMAND} in
 "start" | "stop")
   ;;
 *)
   echo "Invalid Command [${COMMAND}]"
   exit 1
   ;;
esac

if [ -z "$(fgrep ${HUBOT_NAME} ${SHELL_DIR}/hubot.lst)" ] ; then
  echo "Invalid hubot name [${HUBOT_NAME}]"
  exit 1
fi

# -------------------------------------------
# load bashrc (for 'npm' command)
RES=`whereis npm | grep -o npm | wc -l`
if [ "1" == "${RES}" ] ; then
  echo "load bashrc"
  source ~/.bashrc
fi

# -------------------------------------------
# stop forever process
if [ -z "$(forever list | fgrep ${HUBOT_NAME})" ] ; then
  echo "ALREADY STOPPED PROCESS... (${HUBOT_NAME})"
else
  forever stop ${HUBOT_NAME}
  RET=$?

  if [ "0" != "$RET" ] ; then
    echo "failure forever process (uid=${HUBOT_NAME})"
    exit $RET
  fi
fi

# -------------------------------------------
# start forever process via hubot startup script
if [ "start" == "${COMMAND}" ] ; then
  HUBOT_ROOTDIR=$(cd $(dirname $0)/..; pwd)
  SCRIPT_DIR=${HUBOT_ROOTDIR}/${HUBOT_NAME}

  cd ${SCRIPT_DIR}

  sh ./bin/hubot --adapter slack
  RET=$?
  
  echo -n "running hubot (${HUBOT_NAME}) ..."
  if [ "0" == "${RET}" ] ; then
    echo "[SUCCESS]"
  else
    echo "[FAIL]"
  fi
  exit $RET
fi

exit 0
