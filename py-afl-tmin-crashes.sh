#!/usr/bin/env bash

set -euo pipefail

TARGET=$1
PYTHON_CMD=${PYTHON_CMD:-python3}

TARGET_SCRIPT=$TARGET/fuzz.py
if ! [[ -f "$TARGET_SCRIPT" ]]; then
    echo >&2 "Fuzz target $TARGET/fuzz.py does not exist!"
    exit 1
fi

workdir=$(mktemp -d)
function cleanup()
{
    rm -rf "$workdir"
}
trap cleanup EXIT

crashes=$(find "$TARGET"/crashes-raw/ -type f -name '*.in')

while read -r filename; do
    if [[ -z "$filename" ]]; then
        break
    fi
    BASE=$(basename "$filename" .in)
    mkdir -p "$TARGET"/crashes
    OUTNAME=$TARGET/crashes/$BASE.in

    if [[ -e "$OUTNAME" ]]; then
        continue
    fi

    py-afl-tmin -m 200 -i "$filename" -o "$workdir"/tmin -- \
        "$PYTHON_CMD" "$TARGET_SCRIPT" @@
    (ulimit -v 200000; "$PYTHON_CMD" "$TARGET_SCRIPT" "$workdir"/tmin 1>/dev/null 2>"$workdir"/backtrace) || :
    ./normalize-backtrace.py < "$workdir"/backtrace > "$workdir"/backtrace.normalized
    read -r stack_trace_sum _ <<< "$(sha256sum -b "$workdir"/backtrace.normalized)"
    # After tmin operation, multiple different stack backtraces can
    # actually be just different instances of the same
    # problem. Symbolically link to indicate the duplicates.
    if [[ -e "$TARGET/crashes/$stack_trace_sum.in" ]]; then
        ln -s "$stack_trace_sum.in" "$OUTNAME"
        continue
    fi
    cp "$workdir"/tmin "$TARGET/crashes/$stack_trace_sum.in"
    cp "$workdir"/backtrace.normalized "$TARGET/crashes/$stack_trace_sum.backtrace.txt"
    if [[ ! -e "$OUTNAME" ]]; then
        ln -s "$stack_trace_sum.in" "$OUTNAME"
    fi
done <<< "$crashes"
