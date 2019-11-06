#! /bin/bash
n=4096
for i in {0..10}; do
    ((n*=2))
    echo ""
    echo $n
    ./genPoints.py $n 800 800 autom.json
    ./pointsClever.py autom.json
done