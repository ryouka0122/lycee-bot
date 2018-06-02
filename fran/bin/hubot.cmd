@echo off

call npm install --no-audit
SETLOCAL
SET PATH=node_modules\.bin;node_modules\hubot\node_modules\.bin;%PATH%

export PORT=8080

node_modules\.bin\hubot.cmd --name "fran" %*
