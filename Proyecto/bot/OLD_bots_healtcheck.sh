#!/bin/bash


bot_id=$1
bot_name=$2
#w_path=$3
port=$3
message=$4
if [ "$message" = "" ];then
	message="fldsmdfr"
fi
#w_path="/opt/alloxentric/chatscript_bots/${w_path}/chatscript"	
w_path="/opt/alloxentric"
cd $w_path
id_check=$( printf "test\n:reset\n:who" | ${w_path}/ChatScript/BINARIES/LinuxChatScript64 client=localhost:${port} )
id_check=$(echo "$id_check" | awk  -F "talking to " '{print $2}' | tr -d '\n')
id_check=$(echo "$id_check" | cut  -d' ' -f 1)
if [ "$id_check" = "$bot_id" ]; then
	status_build="OK"
else
	status_build="ERROR"
	id_check=$( printf "test\n:BUILD ${bot_name}\n:reset\n:who" | ${w_path}/ChatScript/BINARIES/LinuxChatScript64 client=localhost:${port} )
	id_check=$(echo "$id_check" | awk  -F "talking to " '{print $2}' | tr -d '\n')
	id_check=$(echo "$id_check" | cut  -d' ' -f 1)
	 if [ "$id_check" = "$bot_id" ]; then
		 status_build="OK"
	 else
		status_build="ERROR"
		exit 1	
	 fi	
fi
start=$(date +%s%N)
response_check=$( printf "test\n:reset\n${message}" | ${w_path}/ChatScript/BINARIES/LinuxChatScript64 client=localhost:${port} )
end=$(date +%s%N)
diff=$((end-start))
real_time=$((diff/1000000))
response_check=`echo ${response_check#*$message} | tr -d '\n'`
response_check=`echo "$response_check" | tr -d ' '`
if [[ $response_check =~ .*\{.* ]]; then
	status_response="OK"
	if [ "$real_time" -gt 1000 ]; then
		status_response="WARN"
	elif [ "$real_time" -gt 5000 ]; then
		status_response="ERROR"
		exit 1
	fi
else
	status_response="ERROR ($real_time ms)"
	if [ "$status_build" = "OK" ]; then
		exit 1
	fi
fi
exit 0



