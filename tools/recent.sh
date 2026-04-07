#!/bin/bash
N="${1:-10}"
LOG="$(dirname "$0")/../wiki/log.md"
grep "^## \[" "$LOG" | tail -"$N"
