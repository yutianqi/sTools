
#!/bin/bash

if [ -z $1 ]; then
    FILE_NAME="catalina.out"
else
    FILE_NAME=$1
fi

if [ -z $2 ]; then
    EXPECT_STATUS="RUNNABLE"
    # EXPECT_STATUS="WAITING"
    # EXPECT_STATUS="TIMED_WAITING"
    # EXPECT_STATUS="BLOCKED"
else
    EXPECT_STATUS=$2
fi

if [ -z $3 ]; then
    EXPECT_THREAD="NeExecutionContext"
else
    EXPECT_THREAD=$3
fi

main() {
    # echo "$FILE_NAME"
    # echo "$EXPECT_STATUS"
    # echo "$EXPECT_THREAD"
    awk 'BEGIN {
        FS = "\""
        state = ""
        name = ""
        detail = ""
    }

    /^"/ {
        detail = detail"\n"$0
        name = $2
        next
    }

    /^ +java.lang.Thread.State:/ {
        detail = detail"\n"$0
        sub(" *java.lang.Thread.State: *", "", $1)
        state = $1
        next
    }

    $0 == "" {
        if (name != "" && state != ""&& match(name, ".*"expectThread".*") && match(state, expectStatus)) {
            print  detail
        }
        name = ""
        state = ""
        detail = ""
        next
    }

    {
        detail = detail"\n"$0
    }
    END {
        # print expectStatus, v2
    }
    ' expectStatus=$EXPECT_STATUS expectThread=$EXPECT_THREAD $FILE_NAME
}

main