#!/bin/bash

proid=`ps -ef | grep 'hello_busy.py' | grep -v grep | awk '{print $2}'`
echo $proid
echo ${#prodid[@]}
#for var in "${proid[*]}"
#do
  #echo "${var}"
#done
if ["$?" -eq 0];
then
 echo "Jobs are running"
else
 echo "No Jobs"
fi