#!/bin/sh

cd core-common-lib
git pull
cd ..

cd core-communication-lib
git pull
cd ..

cd core-firmware
rm -fr inc src
git checkout .
git checkout spark-master
git fetch
git pull
git checkout master
git merge spark-master
git rm build/core-firmware.bin
git rm build/core-firmware.elf
git rm build/core-firmware.hex
git commit
git push
