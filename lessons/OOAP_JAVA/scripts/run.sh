#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: ./run.sh ClassName [args...]"
    exit 1
fi
# Run Java directly with -ea flag and full classpath
java -ea -cp target/classes:target/dependency/* "$1" "${@:2}"