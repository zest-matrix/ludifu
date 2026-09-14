#!/bin/bash
# Verifies every section in CONTENT-MANIFEST.txt still exists. Run after every edit.
fail=0
while IFS='|' read -r file id marker; do
  [[ "$file" =~ ^#.*$ || -z "$file" ]] && continue
  if ! grep -q "id=\"$id\"" "$file" 2>/dev/null; then
    echo "  ✗ MISSING SECTION: $file #$id"; fail=1; continue
  fi
  if ! grep -q "$marker" "$file" 2>/dev/null; then
    echo "  ✗ MISSING CONTENT: $file #$id (marker: '$marker')"; fail=1
  fi
done < CONTENT-MANIFEST.txt
[ $fail -eq 0 ] && echo "  ✓ All sections and content markers present"
exit $fail
