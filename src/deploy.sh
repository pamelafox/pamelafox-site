#!/bin/sh
python3 src/freeze.py
FILE="src/flaskapp/build/talks/index.html"
echo "*** File - $FILE contents ***"
head -n 40 $FILE
exit 0
