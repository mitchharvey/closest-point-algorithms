#! /usr/bin/env python

from graphics import *
from random import *
from time import sleep
import math
import sys
import json

width = 800
height = 800
N = 500
baseWidth = 16
dotRadius = 2
margin = 10
maxDist = 999999

compareCount = 0
shortestDist = maxDist
shortestDistLine = Line(Point(0,0), Point(0,0))
win = GraphWin("Points", width, height)
win.setBackground("black")

def main():
    global shortestDist, shortestDistLine
    points = getPoints()
    N = len(points)

    points.sort(key=lambda x: x.getX(), reverse=False)

    for p in points:
        c = Circle(p, dotRadius)
        c.setFill("white")
        c.setOutline("white")
        c.draw(win)


    minimum = locate(points)
    print("MINIMUM: ", minimum)
    print("COMPARES: ", compareCount)
    print("N^2        = {}\nN log(N^2) = {}\nN log(N)   = {}\nN          = {}"
        .format(N**2, N*math.log(N**2, 2), N*math.log(N, 2), N))

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


def locate(points):
    if len(points) == 2:
        return dist(points[0], points[1])
    if len(points) <= 1:
        return maxDist
    midEl = math.floor((len(points)-1)/2)
    # print("POINTS:", points, "MIDEL:", midEl, "PASS1:", points[:midEl+1], "PASSB", points[midEl+1:], "\n")
    midX = (points[midEl].getX() + points[midEl + 1].getX())/2
    midLine = Line(Point(midX, 0), Point(midX, height))
    midLine.setFill("green")
    width = math.floor((len(points)/N) * baseWidth)
    midLine.setWidth(width)
    midLine.draw(win)

    leftSet = points[0:midEl+1]
    rightSet = points[midEl+1:len(points)]
    leftMin = locate(leftSet)
    rightMin = locate(rightSet)
    LRMin = distBetweenSets(leftSet, rightSet, midX, leftMin)
    return min([leftMin, rightMin, LRMin])

def distBetweenSets(setA, setB, midX, leftMin):
    minimum = maxDist
    for a in setA:
        # Get a subset of setB of all the points that are in the rectangle of (dist, 2*dist)
        rectLow = Point(midX, a.getY() - leftMin)
        rectHigh = Point(midX + leftMin, a.getY() + leftMin)
        compSet = restrictSet(setB, rectLow, rectHigh)
        r = Rectangle(rectLow, rectHigh)
        r.setOutline("blue")
        r.setWidth(3)
        r.draw(win)
        for b in compSet:
            minimum = min([minimum, dist(a, b)])
        r.undraw()
    return minimum

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
    x = input("")
    print("done")