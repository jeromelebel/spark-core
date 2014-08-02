#!/bin/sh

pushd . > /dev/null
tools_path="`pwd`/$0"
cd `dirname $tools_path`

merge_project() {
    project="$1"
    cd "${project}"
    git checkout spark-core-master
    if [ "$?" = "1" ] ; then
        git remote add spark-core "git@github.com:spark/${project}.git"
        git fetch spark-core
        git branch spark-core-master spark-core/master
        git checkout spark-core-master
    fi
    git pull
    git checkout master
    git merge spark-core-master
    cd ..
}

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
cd ..

merge_project core-common-lib
merge_project core-communication-lib
merge_project core-firmware
