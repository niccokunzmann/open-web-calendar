#!/bin/bash

set -e

cd "`dirname \"$0\"`"

(
  cd ..
  if grep -rqI calend''er; then
    grep -rI calend''er
    echo "ERROR: wrong spelling"
    exit 1
  fi
)
