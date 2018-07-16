#!/usr/bin/env bash

set -euo pipefail

TARGET=$1
PYTHON_CMD=${PYTHON_CMD:-python3}

TARGET_SCRIPT=$TARGET/fuzz.py
if ! [[ -f "$TARGET_SCRIPT" ]]; then
    echo >&2 "Fuzz target $TARGET/fuzz.py does not exist!"
    exit 1
fi
if [[ -d "$TARGET"/corpus.new ]]; then
    echo >&2 "Previous (failed) new corpus exists at $TARGET/corpus.new!"
    echo >&2 "Unable to continue when this directory exists!"
    exit 1
fi
if [[ -d "$TARGET"/corpus.old ]]; then
    echo >&2 "Previous (failed) old corpus exists at $TARGET/corpus.old!"
    echo >&2 "Unable to continue when this directory exists!"
    exit 1
fi

workdir=$(mktemp -d "$TARGET"/cmin-workdir.XXXXXX)
function cleanup()
{
    rm -rf "$workdir"
    if [[ -d "$TARGET"/corpus.new ]]; then
        rm -rf "$TARGET"/corpus.new
    fi
}
trap cleanup EXIT
mkdir "$workdir"/max

DIRS=(
    "$TARGET"/in
    "$TARGET"/corpus
)

DATAROOT=/dev/shm/python-stdlib-$TARGET

queue_dirs=$(find "$DATAROOT" -mindepth 2 -maxdepth 2 -type d -name queue)
while read -r queue_dir; do
    if [[ -z "$queue_dir" ]]; then
        break
    fi
    DIRS+=("$queue_dir")
done <<< "$queue_dirs"

for directory in "${DIRS[@]}"; do
    echo "Going through directory $directory"
    files=$(find "$directory" -type f 2>/dev/null || :)
    if [[ -z "$files" ]]; then
        continue
    fi
    while read -r filename; do
        # Protect against sudden file losses:
        cp -p "$filename" "$workdir"/.copy || continue
        read -r checksum _ <<< "$(sha256sum -b "$workdir"/.copy)"
        # Duplicate file, no need to continue:
        if [[ -f "$workdir/max/$checksum".in ]]; then
            continue
        fi
        mv "$workdir"/.copy "$workdir"/max/"$checksum".in
    done <<< "$files"
done

py-afl-cmin -m 200 -i "$workdir"/max -o "$workdir"/min -- \
    "$PYTHON_CMD" "$TARGET_SCRIPT" @@

cp -rp "$workdir"/min "$TARGET"/corpus.new
mv "$TARGET"/corpus "$TARGET"/corpus.prev 2>/dev/null || :
mv "$TARGET"/corpus.new "$TARGET"/corpus
rm -rf "$TARGET"/corpus.prev
