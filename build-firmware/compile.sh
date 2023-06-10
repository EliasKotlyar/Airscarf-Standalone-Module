#!/bin/bash
get_abs_filename() {
  # $1 : relative filename
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}
RP2040_FIRMWARE_FILE=rp2-pico-w-20230610-unstable-v1.20.0-189-gfd277704c
FIRMWARE_FILENAME=airscarfv21
FILEDIR=$(get_abs_filename "../src")
echo $FILEDIR
./dir2uf2.py $FILEDIR --filename $FIRMWARE_FILENAME --append-to=$RP2040_FIRMWARE_FILE.uf2
rm $FIRMWARE_FILENAME.bin
rm $FIRMWARE_FILENAME.uf2
mv $RP2040_FIRMWARE_FILE-$FIRMWARE_FILENAME.uf2 $FIRMWARE_FILENAME.uf2
