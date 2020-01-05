#!/bin/bash

# clean
echo "cleaning"
rm -rf build/ 2> /dev/null

echo "copy src/ -> build/"
cp -R src/ build/

# compile
echo "compiling"
mpy-cross --version
find build/ -name "*.py" -exec mpy-cross -march=xtensa {} \;

# remove uncompiled
echo "remove uncompiled from build/"
rm build/*.py

echo "[done]"
