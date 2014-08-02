#!/bin/sh

dfu-util -d 1d50:607f -a 0 -s 0x08005000:leave -D spark-core/core-firmware/build/core-firmware.bin
