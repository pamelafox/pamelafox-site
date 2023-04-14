#!/bin/sh
python3 freeze.py
FILE="flaskapp/build/talks/index.html"
echo "*** File - $FILE contents ***"
head -n 40 $FILE
exit 0
