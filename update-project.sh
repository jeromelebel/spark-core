#!/bin/sh

pushd . > /dev/null
tools_path="`pwd`/$0"
cd `dirname $tools_path`

git checkout master
git submodule update --init --recursive

popd > /dev/null
