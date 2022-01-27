#!/bin/bash
#
# Add requirement anchors and links (if not already there)
#
# Note that requirement definitions must be at the beginning of a line,
# possibly preceded by '*' characters.

for file in $(find . -name '*.md'); do
    echo ---- $file ----
    # ths first pattern handles anchors, and the second handles links
    sed -E \
        -e 's/^(\**)(R-[A-Z][A-Z0-9]*\.[0-9]+[a-z]?)/\1[\2]{}/' \
        -e 's/(^|[^[])(R-[A-Z][A-Z0-9]*\.[0-9]+[a-z]?)([^]]|$)/\1[\2]()\3/g' \
        $file >$file.edited
    /bin/mv -f $file.edited $file
done
