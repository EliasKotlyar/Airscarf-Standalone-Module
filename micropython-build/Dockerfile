FROM ubuntu:22.04
MAINTAINER elias.kotlyar@gmail.com
# Copied from https://forum.micropython.org/viewtopic.php?f=21&t=12559#p68049

RUN  apt update && \
    DEBIAN_FRONTEND=noninteractive TZ=Europe/Berlin apt install -y \
      git\
     gcc-arm-none-eabi \
     libstdc++-arm-none-eabi-newlib  \
     libnewlib-arm-none-eabi \
     build-essential \
     cmake \
     python3
RUN cd /tmp && git clone https://github.com/micropython/micropython.git
RUN cd /tmp/micropython && git submodule update --init lib/mbedtls
RUN cd /tmp/micropython && make -C mpy-cross




