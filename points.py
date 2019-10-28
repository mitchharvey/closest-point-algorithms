#! /usr/bin/env python

from graphics import *
from random import *
from time import sleep
import math
import sys
import json

width = 800
height = 800
N = 20
baseWidth = 6
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

    for p in points:
        c = Circle(p, dotRadius)
        c.setFill("white")
        c.setOutline("white")
        c.draw(win)

    # remove redundant i.e. b = a+1...n
    for a in points:
        for b in points:
            if a == b:
                continue
            l = Line(a, b)
            l.setFill("white")
            l.draw(win)

            d = dist(a, b)
            if d < shortestDist:
                shortestDistLine.undraw()
                shortestDist = d
                shortestDistLine = l.clone()
                shortestDistLine.setFill(color_rgb(255, 10, 214))
                # shortestDistLine.setOutline("white")
                shortestDistLine.setWidth(3)
                shortestDistLine.draw(win)
            l.undraw()

    print("MINIMUM: ", shortestDist)
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

def dist(a, b):
    global compareCount
    compareCount += 1
    xDist = abs(b.getX() - a.getX())
    yDist = abs(b.getY() - a.getY())
    return ((xDist ** 2) + (yDist ** 2)) ** 0.5

if __name__ == "__main__":
    main()
    x = input("")
    print("done")