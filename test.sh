#!/usr/bin/env bash

set -euo pipefail

TARGET=$1
INSTANCE=${2:-1}
PYTHON_CMD=${PYTHON_CMD:-python3}

TARGET_SCRIPT=$TARGET/fuzz.py
if ! [[ -f "$TARGET_SCRIPT" ]]; then
    echo >&2 "Fuzz target $TARGET/fuzz.py does not exist!"
    exit 1
fi
INDIR=$TARGET/in

AFL_ID=$TARGET-$INSTANCE

echo >&2 "Running $AFL_ID with $PYTHON_CMD"

while read -r filename; do
    echo >&2 "Running for $filename"
    "$PYTHON_CMD" "$TARGET_SCRIPT" "$filename"
done <<< "$(find "$INDIR" -type f)"
