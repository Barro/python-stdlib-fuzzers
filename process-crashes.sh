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
OUTDIR=/dev/shm/python-stdlib-$TARGET

INSTANCE_TYPE=-M
if [[ "$INSTANCE" != 1 ]]; then
    INSTANCE_TYPE=-S
fi

AFL_ID=$TARGET-$INSTANCE

echo >&2 "Running $AFL_ID with $PYTHON_CMD"

while read -r filename; do
    "$PYTHON_CMD" "$TARGET_SCRIPT" "$filename" && continue
    stack_trace_sha256=$(
        "$PYTHON_CMD" "$TARGET_SCRIPT" "$filename" 1>/dev/null 2>"$OUTDIR"/current-crash) || :
    echo >&2 "$PYTHON_CMD" "$TARGET_SCRIPT" "$filename"
    read -r stack_trace_sum _ <<< "$(sha256sum -b "$OUTDIR"/current-crash)"
    mkdir -p "$TARGET"/crashes-raw
    cp "$filename" "$TARGET"/crashes-raw/"$stack_trace_sum".in
done <<< "$(find "$OUTDIR" -type f | grep crashes/id | sort)"
