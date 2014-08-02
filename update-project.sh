#!/bin/sh

pushd . > /dev/null
tools_path="`pwd`/$0"
cd `dirname $tools_path`
cd ../..

cd core-firmware
git checkout master
git pull
cd ../core-common-lib
git checkout master
git pull
cd ../core-communication-lib
git checkout master
git pull
cd ..

git commit -m "latest core" core-firmware core-common-lib core-communication-lib

popd > /dev/null
