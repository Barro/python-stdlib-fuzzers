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

exec py-afl-fuzz -i "$INDIR" -o "$OUTDIR" "$INSTANCE_TYPE" "$AFL_ID" -- \
     "$PYTHON_CMD" "$TARGET_SCRIPT" @@
