#! /usr/bin/env python

from graphics import *
from random import *
from time import sleep
import math
import sys
import json

N = 0
width = 800
height = 800
baseWidth = 16
dotRadius = 2
maxDist = 999999

compareCount = 0
shortestDist = maxDist
shortestDistLine = Line(Point(0,0), Point(0,0))
win = GraphWin("Points", width, height)
win.setBackground("black")

def main():
    if len(sys.argv) < 2:
        print("Specify points")
        exit(1)

    global shortestDist, shortestDistLine, N
    points = getPoints()
    N = len(points)

    points.sort(key=lambda x: x.getX(), reverse=False)
    yPoints = points.copy()
    yPoints.sort(key=lambda x: x.getY(), reverse=False)

    for p in points:
        c = Circle(p, dotRadius)
        c.setFill("white")
        c.setOutline("white")
        c.draw(win)

    minimum = locate(points, yPoints)
    print("MINIMUM: ", minimum)
    print("COMPARES: ", compareCount)
    print("N^2        = {}\nN log(N^2) = {}\nN log(N)   = {}\nN          = {}"
        .format(N**2, N*math.log(N**2, 2), N*math.log(N, 2), N))

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
    # print("POINTS:", points, "MIDEL:", midEl, "PASS1:", points[:midEl+1], "PASSB", points[midEl+1:], "\n")
    midX = (points[midEl].getX() + points[midEl + 1].getX())/2
    midLine = Line(Point(midX, 0), Point(midX, height))
    midLine.setFill("green")
    width = math.floor((len(points)/N) * baseWidth)
    midLine.setWidth(width)
    midLine.draw(win)

    leftX = points[0:midEl+1]
    rightX = points[midEl+1:len(points)]
    leftY, rightY = ySorted(yPoints, midX)
    # print("midx", midX)
    # for x in leftY:
    #     print("left", x)
    # for x in rightY:
    #     print("right", x)
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

    # l = Line(Point(midX, 0), Point(midX, height))
    # l.setFill("pink")
    # l.draw(win)

    r = Rectangle(rectLow, rectHigh)
    r.setOutline("blue")
    r.setWidth(3)
    r.draw(win)
    strip = restrictSet(yPoints, rectLow, rectHigh)

    # th(7n)
    for i in range(len(strip)):
        for j in range(min(7, len(strip)-i-1)): # check the 7 following points, if there are at least 7
            minimum = min(minimum, dist(strip[i], strip[i + j + 1]))

    r.undraw()
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
                # x.undraw()
                # c = Circle(x, 3)
                # c.setFill("green")
                # c.draw(win)
    # sleep(3)
    return retset

def dist(a, b):
    global compareCount
    compareCount += 1
    l = Line(a, b)
    l.setFill("pink")
    l.draw(win)
    xDist = abs(b.getX() - a.getX())
    yDist = abs(b.getY() - a.getY())
    # sleep(1)
    l.undraw()
    return ((xDist ** 2) + (yDist ** 2)) ** 0.5


if __name__ == "__main__":
    main()
    # x = input("")
    print("done")