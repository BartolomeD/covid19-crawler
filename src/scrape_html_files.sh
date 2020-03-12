#!/bin/bash
for f in $(find /home/rojas/corona/ -name 'index.html')
do
    echo "$f"
    python main.py --html $f
done
echo "FINISHED"