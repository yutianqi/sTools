#!/bin/bash

FILE_NAME="catalina.out"

declare -A threadInfo

main() {
    echo "$FILE_NAME"

    while IFS= read -r line; do
        line=$(echo "$line" | tr -d '\r\n')  # Remove any trailing carriage returns or newlines

        if [ -z "$line" ]; then
            if [ ${#threadInfo[@]} -eq 0 ]; then
                continue
            fi
            echo "${threadInfo[@]}"
            threadInfo=()
            continue
        fi

        if [[ $line == \"* ]]; then
            threadInfo["name"]=$(echo "$line" | cut -d'"' -f2)
            continue
        fi

        if [[ $line == "java.lang.Thread.State:"* ]]; then
            threadInfo["state"]=$(echo "$line" | sed 's/java.lang.Thread.State: //')
            continue
        fi

    done < "$FILE_NAME"
}

main




