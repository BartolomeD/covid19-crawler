#!/bin/bash
for f in $(find /home/ubuntu/daniel/covid19-crawler/html/ -name 'index.html')
do
    echo "$f"
    python src/main.py --html $f
done
echo "FINISHED"