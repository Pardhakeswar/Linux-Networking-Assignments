#!/bin/bash
#CPU Usage monitoring script for question 4 

echo 'Load Monitor Script Starting...'
echo 'Enter the Threshold X1 for setting High CPU alert'
read X1
echo 'Enter the Theshold X5 for setting very HIGH CPU alert'
read X5
echo 'Enter The granularity value T in seconds'
read Tg
echo 'Enter total time T in minutes'
read T
echo 'Executing the  Script...' 

count=0
Tcount=$(( $T*60 ))
Tcount=$(( $Tcount/$Tg ))

while [[ $(echo "$count < $Tcount"| bc) -eq 1 ]]
do
sleep $Tg 

timestamp="$(date)"

L1=$(uptime|cut -d "l" -f 2|cut -d ":" -f 2 |cut -d ',' -f 1|cut -d ' ' -f 2 )
L5=$(uptime|cut -d "l" -f 2|cut -d ":" -f 2 |cut -d ',' -f 2|cut -d ' ' -f 2 )
L15=$(uptime|cut -d "l" -f 2|cut -d ":" -f 2|cut -d ',' -f 3|cut -d ' ' -f 2 )
comma=','

result=$timestamp$comma$L1$comma$L5$comma$L15
#echo "$result" 
#log the result in Log.csv file 
echo $result>>Log.csv
#for generating graph only ( uncomment to write to the .dat file)
#echo "$count $L1">>graph.dat

if [[ $(echo "$L5 >= $X5" |bc -l)  -eq 1 ]]; then  
if [[ $(echo "$L1 > $L5" |bc -l) -eq 1 ]]; then 
# alert
echo "very HIGH CPU usage"
#logging the alert 
echo "$timestamp,very HIGH CPU usage,$L5">>alert.csv
fi
fi

if [[ $(echo "$L1 >= $X1" |bc -l)  -eq 1 ]]; then 
#alert
echo "HIGH CPU usage"
#logging the alert
echo "$timestamp,HIGH CPU usage,$L1">>alert.csv
fi

count=$(($count+1)) 
done

echo "exiting the script" 
exit 1
