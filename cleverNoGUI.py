#! /usr/bin/env python

import math
import sys
import json
import pointclass

width = 800
height = 800
baseWidth = 16
dotRadius = 2
maxDist = 999999

compareCount = 0
shortestDist = maxDist

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

def main():
    if len(sys.argv) < 2:
        print("Specify points")
        exit(1)

    global shortestDist, shortestDistLine, N
    pointclass.setup()
    points = getPoints()
    N = len(points)

    points.sort(key=lambda x: x.getX(), reverse=False)
    yPoints = points.copy()
    yPoints.sort(key=lambda x: x.getY(), reverse=False)

    minimum = locate(points, yPoints)
    print("MINIMUM: ", minimum)
    print("COMPARES: ", compareCount)
    # print("N^2        = {}\nN log(N^2) = {}\nN log(N)   = {}\nN          = {}"
    #     .format(N**2, N*math.log(N**2, 2), N*math.log(N, 2), N))

def getPoints():
    with open(sys.argv[1], "r") as inPoints:
        pointLocations = json.loads(inPoints.read())
        points = [Point(a[0], a[1]) for a in pointLocations]
    return points

def locate(points, yPoints):
    if len(points) <= 3:
        retMin = maxDist
        for a in points:
            for b in points:
                if a == b:
                    continue
                retMin = min(retMin, dist(a, b))
        return retMin
    
    midEl = math.floor((len(points)-1)/2)
    midX = (points[midEl].getX() + points[midEl + 1].getX())/2

    leftX = points[0:midEl+1]
    rightX = points[midEl+1:len(points)]
    leftY, rightY = ySorted(yPoints, midX)
    leftMin = locate(leftX, leftY)
    rightMin = locate(rightX, rightY)
    LRMin = min(leftMin, rightMin)

    centerMin = distBetweenSets(yPoints, midX, LRMin)
    return min(LRMin, centerMin)

# O(n)
def distBetweenSets(yPoints, midX, LRMin):
    minimum = maxDist
    rectLow = Point(midX - LRMin, 0)
    rectHigh = Point(midX + LRMin, height)

    strip = restrictSet(yPoints, rectLow, rectHigh)

    # th(7n)
    for i in range(len(strip)):
        for j in range(min(7, len(strip)-i-1)): # check the 7 following points, if there are at least 7
            minimum = min(minimum, dist(strip[i], strip[i + j + 1]))

    return minimum

# th(n)
def ySorted(set, midX):
    leftY = []
    rightY = []
    for p in set:
        if p.getX() < midX:
            leftY.append(p)
        elif p.getX() > midX:
            rightY.append(p)
        else:
            print("ERROR:", p.getX(), p.getY(), midX)
    return leftY, rightY


# th(n)
def restrictSet(set, lowerBound, higherBound):
    retset = []
    for x in set:
        if x.getX() >= lowerBound.getX() and x.getY() >= lowerBound.getY():
            if x.getX() <= higherBound.getX() and x.getY() <= higherBound.getY():
                retset.append(x)
    return retset

def dist(a, b):
    global compareCount
    compareCount += 1
    xDist = abs(b.getX() - a.getX())
    yDist = abs(b.getY() - a.getY())
    return ((xDist ** 2) + (yDist ** 2)) ** 0.5


if __name__ == "__main__":
    main()
    print("done")