#!/usr/bin/env bash

set -euo pipefail

TARGET=$1
PYTHON_CMD=${PYTHON_CMD:-python3}

TARGET_SCRIPT=$TARGET/fuzz.py
if ! [[ -f "$TARGET_SCRIPT" ]]; then
    echo >&2 "Fuzz target $TARGET/fuzz.py does not exist!"
    exit 1
fi
INDIR=$TARGET/in

# corpus/ directory within a target provides seed corpus with much
# larger coverage than what the manually created in/ directory does.
if [[ -d "$TARGET"/corpus ]]; then
    INDIR=$TARGET/corpus
fi

OUTDIR=/dev/shm/python-stdlib-$TARGET

INSTANCE=0
# afl-fuzz locks its working directory, use that information to find
# the next available ID
for instance_id in $(seq 1 "$(nproc)"); do
    instance_dir=$OUTDIR/$TARGET-$instance_id
    if [[ ! -d "$instance_dir" ]]; then
        INSTANCE=$instance_id
        break
    fi
    flock -n "$instance_dir" -c echo > /dev/null || continue
    INSTANCE=$instance_id
    break
done

if [[ "$INSTANCE" == 0 ]]; then
    echo >&2 "Already have $(nproc) afl-fuzz instances running for this target!"
    echo >&2 "Refusing to start any more of them!"
    exit 1
fi

INSTANCE_TYPE=-M
if [[ "$INSTANCE" != 1 ]]; then
    INSTANCE_TYPE=-S
fi

AFL_ID=$TARGET-$INSTANCE

echo >&2 "Running $AFL_ID with $PYTHON_CMD at $OUTDIR/$AFL_ID"

PARAMS=(
    -m 200
    -i "$INDIR"
    -o "$OUTDIR"
    "$INSTANCE_TYPE" "$AFL_ID"
)

if [[ -f "$TARGET"/"$TARGET".dict ]]; then
    PARAMS+=(-x "$TARGET"/"$TARGET".dict)
fi

export PYTHONHASHSEED=1234
exec py-afl-fuzz "${PARAMS[@]}" -- "$PYTHON_CMD" "$TARGET_SCRIPT" @@
