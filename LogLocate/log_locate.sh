#!/bin/bash

read -p "Input: " input_string 

file_name=$(echo $(pwd) | cut -d "/" -f1-6)"/etc/log4j/log4j2.xml"
IFS='.' read -ra parts <<< "$input_string"
for ((i=${#parts[@]}; i>=1; i--)); do
    concatenated=""
    for ((j=0; j<i; j++)); do
        concatenated="$concatenated${parts[j]}."
    done
    concatenated=${concatenated%?}
    appender=$(grep -A 3 "\"$concatenated\"" $file_name | grep "AppenderRef" | cut -d "\"" -f2)

    if [ "$appender" != "" ] ; then
        line=$(grep -A 3 "$appender\"" $file_name  | grep fileName)
        regex='fileName="([^"]+)"'
        if [[ $line =~ $regex ]]; then
            extracted_string="${BASH_REMATCH[1]}"
            echo "match[$concatenated], logFile=$extracted_string"
            break
        fi
    fi
done


read -p "Input: " s;f=$(echo $(pwd)|cut -d/ -f1-6)"/etc/log4j/log4j2.xml";IFS='.' read -ra p <<< "$s";for((i=${#p[@]};i>=1;i--)); do c="";for((j=0;j<i;j++));do c="$c${p[j]}.";done;c=${c%?};a=$(grep -A 3 "\"$c\"" $f|grep "AppenderRef"|cut -d "\"" -f2);if [ "$a" != "" ];then l=$(grep -A 3 "$a\"" $f|grep fileName);regex='fileName="([^"]+)"';if [[ $l =~ $regex ]];then e="${BASH_REMATCH[1]}";echo "match[$c], logFile=$e";break;fi;fi;done