#!/bin/bash

scriptpath="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

cd $scriptpath
cd ..
rsync -a -v --ignore-existing icons_original/ icons/ #copy missing images from icons_original to icons
cd icons

IMAGES_TO_RESIZE="$(find . -iname "*.png" -type f -exec identify -format '%w %h %i\n' '{}' \; | awk '$1>120 || $2>120' | awk '{print $3}')"

echo $IMAGES_TO_RESIZE | while read line; do
    mogrify -trim +repage -fuzz 20% -resize 128x128 $line # needs imagemagick installed
done
