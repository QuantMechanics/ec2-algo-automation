#!/bin/bash
  
proId=(`ps -ef | grep 'hello_busy.py' | grep -v grep | awk '{print $2}'`)
#proIdlen= ${#proId[*]}
#echo $prodIdlen
if [ ${#proId[*]} -gt 0 ]
then
 echo "Total processes running with given filename are: ${#proId[*]}"
 pkill -f 'hello_busy.py'
else
 echo "No processes running"
fi