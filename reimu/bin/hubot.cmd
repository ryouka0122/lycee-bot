@echo off

call npm install
SETLOCAL
SET PATH=node_modules\.bin;node_modules\hubot\node_modules\.bin;%PATH%

SET HUBOT_SLACK_TOKEN=SLACK_TOKEN_KEY

node_modules\.bin\hubot.cmd --name "reimu" %*
