#!/bin/bash
CONTAINER_NAME=airscarf-compiler
IMAGE_NAME=micropython-rp2-build
FIRMWARE_FILENAME=airscarfv1.uf2
docker rm $CONTAINER_NAME
docker container create -i -t --name $CONTAINER_NAME $IMAGE_NAME

docker cp ./../micropython/. $CONTAINER_NAME:/tmp/micropython/ports/rp2/modules
docker exec -w /tmp/micropython/ports/rp2/ $CONTAINER_NAME BOARD=PICO_W make submodule
docker exec -w /tmp/micropython/ports/rp2/ $CONTAINER_NAME BOARD=PICO_W make clean
docker exec -w /tmp/micropython/ports/rp2/ $CONTAINER_NAME BOARD=PICO_W make
docker cp $CONTAINER_NAME:/tmp/micropython/ports/rp2/build-PICO-W/firmware.uf2 $FIRMWARE_FILENAME