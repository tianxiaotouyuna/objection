#!/bin/bash
# 打开一个新的终端窗口
osascript -e 'tell application "Terminal" to do script "objection --gadget Tiktok explore"'
# 等待一段时间确保终端已经打开并且命令已经执行
sleep 5
# 在同一个终端窗口中执行后续命令
osascript -e 'tell application "Terminal" to do script "ios jailbreak disable" in front window'
sleep 2
# 在同一个终端窗口中执行后续命令
osascript -e 'tell application "Terminal" to do script "ios sslpinning disable" in front window'
