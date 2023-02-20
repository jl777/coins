#!/bin/bash

scriptpath="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

cd $scriptpath
cd ../icons

IMAGES_TO_RESIZE="$(find . -iname "*.png" -type f -exec identify -format '%w %h %i\n' '{}' \; | awk '$1>128 || $2>128' | awk '{print $3}')"

echo $IMAGES_TO_RESIZE | while read line; do
    mogrify -resize 128x128 $line
done
