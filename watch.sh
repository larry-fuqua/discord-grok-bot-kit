#!/bin/sh
DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
cd "$DIR"
PYTHON="${DIR}/venv/bin/python3"
if [ ! -x "$PYTHON" ]; then
  PYTHON=python3
fi
while true; do
  "$PYTHON" "$DIR/relay.py" >> "$DIR/relay.log" 2>&1
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) relay exited $?, restart in 3s" >> "$DIR/relay.log"
  sleep 3
done
