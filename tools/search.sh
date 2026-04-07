#!/bin/bash
# Usage: ./tools/search.sh <query>
QUERY="$*"
WIKI_DIR="$(dirname "$0")/../wiki"
echo "=== Searching wiki for: $QUERY ==="
grep -ril "$QUERY" "$WIKI_DIR" | sed "s|$WIKI_DIR/||"
echo ""
echo "=== Context ==="
grep -ri --include="*.md" -n "$QUERY" "$WIKI_DIR" | sed "s|$WIKI_DIR/||" | head -40
