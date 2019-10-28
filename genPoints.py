#! /usr/bin/env python
import sys, json, random

if len(sys.argv) < 5:
    print("USAGE: ./genPoints.py number xMax yMax out.json")
    exit(1)

points = []
for x in range(int(sys.argv[1])):
    p = (random.uniform(0, int(sys.argv[2])), random.uniform(0, int(sys.argv[3])))
    points.append(p)
with open(sys.argv[4], "w") as outfile:
    outfile.write(json.dumps(points))
