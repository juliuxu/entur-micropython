#!/bin/bash

# clean
echo "cleaning"
rm -rf build/ 2> /dev/null

echo "copy src/ -> build/"
cp -R src/ build/

# compile
echo "compiling"
mpy-cross --version
cd build
find . -name "*.py" -exec mpy-cross -march=xtensa -O4 {} \;
cd ..
# remove uncompiled
echo "remove uncompiled from build/"
rm build/*.py
cp src/boot.py build/boot.py
cp src/main.py build/main.py
rm build/boot.mpy
rm build/main.mpy

echo "[done]"
