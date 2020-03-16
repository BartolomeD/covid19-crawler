#!/bin/bash
for f in $(find html/ -name 'index.html')
do
    echo "$f"
    python src/main.py --html $f
done
echo "FINISHED"