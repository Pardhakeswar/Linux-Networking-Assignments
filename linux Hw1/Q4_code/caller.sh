#!/bin/bash
#caller  sh file for cronjob 

if pidof =o %PPID -x "q4.sh">>/dev/null; then
echo "Script already running " 
exit 1
fi

$HOME/HW1/q4.sh
