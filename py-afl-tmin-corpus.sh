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

corpus=$(find "$TARGET"/corpus/ -type f -name '*.in')
files=$(echo "$corpus" | wc -l)

current_file=1
while read -r filename; do
    if [[ -z "$filename" ]]; then
        break
    fi
    echo >&2 "Processing $current_file/$files"
    current_file=$(( current_file + 1 ))

    py-afl-tmin -m 200 -i "$filename" -o "$workdir"/tmin -- \
        "$PYTHON_CMD" "$TARGET_SCRIPT" @@
    if cmp --quiet "$filename" "$workdir"/tmin; then
        continue
    fi
    read -r input_checksum _ <<< "$(sha256sum -b "$workdir"/tmin)"
    cp -p "$workdir"/tmin "$TARGET/corpus/$input_checksum.in"
    rm "$filename"
done <<< "$corpus"

echo
