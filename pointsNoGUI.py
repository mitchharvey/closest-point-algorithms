#! /usr/bin/env python

from random import *
import math
import sys
import json
import pointclass

width = 800
height = 800
N = 20
baseWidth = 6
dotRadius = 2
margin = 10
maxDist = 999999

compareCount = 0

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

def main():
    global compareCount
    pointclass.setup()
    points = getPoints()
    N = len(points)

    shortestDist = maxDist

    # remove redundant i.e. b = a+1...n
    for ax in range(len(points)):
        a = points[ax]
        for bx in range(ax, len(points)):
            b = points[bx]
            if a == b:
                continue

            d = dist(a, b)

            if d < shortestDist:
                shortestDist = d

    print("MINIMUM: ", shortestDist)
    print("COMPARES: ", compareCount)
    # print("N^2        = {}\nN log(N^2) = {}\nN log(N)   = {}\nN          = {}"
    #     .format(N**2, N*math.log(N**2, 2), N*math.log(N, 2), N))

def getPoints():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as inPoints:
            pointLocations = json.loads(inPoints.read())
            points = [Point(a[0], a[1]) for a in pointLocations]
    else:
        points = []
        for x in range(N):
            p = Point(uniform(margin, width-margin), uniform(margin, height-margin))
            points.append(p)
    return points

def dist(a, b):
    global compareCount
    compareCount += 1
    xDist = abs(b.getX() - a.getX())
    yDist = abs(b.getY() - a.getY())
    return ((xDist ** 2) + (yDist ** 2)) ** 0.5

if __name__ == "__main__":
    main()
    print("done")