#!/bin/bash
inotifywait -q -m -e close_write --format %e lego.py |
while read events; do
  ./lego.py
done