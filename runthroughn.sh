#! /bin/bash

# For a nicer output try one of:
# ./runthroughn.sh 2>&1 | grep -E -- 'BRUTE|CLEVER|real'
# ./runthroughn.sh &>> results.txt ; grep -E -- 'BRUTE|CLEVER|real' results.txt
# Replace 'real' with 'user' or 'sys' if wanted.

for i in 500 1000 1500 2000 2500 3000 3500 4000 4500 5000 ; do
    echo -e "\n"
    ./genPoints.py $i 800 800 autom.json
    echo -e "\nBRUTE: $i"
    time ./pointsNoGUI.py autom.json
    echo -e "\nCLEVER: $i"
    time ./cleverNoGUI.py autom.json
done