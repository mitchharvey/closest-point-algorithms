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
baseWidth = 20
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
    mult = (len(points)/N)
    width = math.floor(mult * baseWidth)
    col = math.floor(mult * 255)
    midLine.setFill(color_rgb(128, col, 0))
    midLine.setWidth(width)
    midLine.draw(win)

    leftSet = points[0:midEl+1]
    rightSet = points[midEl+1:len(points)]
    leftMin = locate(leftSet)
    rightMin = locate(rightSet)
    LRMin = distBetweenSets(leftSet, rightSet)
    return min([leftMin, rightMin, LRMin])


def distBetweenSets(setA, setB):
    minimum = maxDist
    for a in setA:
        for b in setB:
            minimum = min([minimum, dist(a, b)])
    return minimum


def dist(a, b):
    global compareCount
    compareCount += 1
    l = Line(a, b)
    l.setFill("pink")
    l.draw(win)
    xDist = abs(b.getX() - a.getX())
    yDist = abs(b.getY() - a.getY())
    l.undraw()
    return ((xDist ** 2) + (yDist ** 2)) ** 0.5


if __name__ == "__main__":
    main()
    x = input("")
    print("done")