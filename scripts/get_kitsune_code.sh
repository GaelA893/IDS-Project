#!/usr/bin/env bash
# Fetch the authors' reference implementation (MIT license) into external/.
# We don't copy it into our repo so our own commits stay clearly separate from theirs.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p external
if [ -d external/Kitsune-py/.git ]; then
  git -C external/Kitsune-py pull --ff-only
else
  git clone --depth 1 https://github.com/ymirsky/Kitsune-py external/Kitsune-py
fi
echo "Pinned commit: $(git -C external/Kitsune-py rev-parse HEAD)  <- record this in the wiki Reproduction-Log"
