#!/bin/bash
#Read lines in the centroid ip file, do ping five times wrt ip addresses, and output latencies to the log file.

cat /home/wins/.core/configs/korea-100-router-centroid-ip-list.txt | while read line
do
	#echo $line
	ping $line -i 0.1 -c 2 >> ./latencies.txt
done
mkdir -p /home/wins/.core/configs/latencies/
cp ./latencies.txt /home/wins/.core/configs/latencies/`hostname -f`-latencies.txt
