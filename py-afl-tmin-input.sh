#!/usr/bin/env bash

set -euo pipefail

TARGET=$1
FILENAME=$2
PYTHON_CMD=${PYTHON_CMD:-python3}

TARGET_SCRIPT=$TARGET/fuzz.py
if ! [[ -f "$TARGET_SCRIPT" ]]; then
    echo >&2 "Fuzz target $TARGET/fuzz.py does not exist!"
    exit 1
fi

BASE=$(basename "$FILENAME")
mkdir -p "$TARGET"/crashes
OUTNAME=$TARGET/crashes/$BASE

if [[ -f "$OUTNAME" ]]; then
    echo >&2 "Already processed $FILENAME"
    exit 0
fi

exec py-afl-tmin -i "$FILENAME" -o "$OUTNAME" -- \
     "$PYTHON_CMD" "$TARGET_SCRIPT" @@
