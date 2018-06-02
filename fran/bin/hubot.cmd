@echo off

call npm install --no-audit
SETLOCAL
SET PATH=node_modules\.bin;node_modules\hubot\node_modules\.bin;%PATH%

SET PORT=8080

for /f "delims=" %%t in (./bin/HUBOT_SLACK_TOKEN.txt) do (
  SET HUBOT_SLACK_TOKEN=%%t
  goto :break_for
)
:break_for

node_modules\.bin\hubot.cmd --name "fran" %*
