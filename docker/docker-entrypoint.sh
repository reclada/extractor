#!/usr/bin/env bash

set -e

if [ "$1" = 'job' ]; then
  exec reclada-dicts-extractor $DOC_ID
fi

exec "$@"
