#!/usr/local/env python3
from collections import namedtuple
import logging
from math import acos, atan2, degrees

from shapely.geometry.point import Point
from shapely.geometry.linestring import LineString
from shapely.ops import split


LabeledLine = namedtuple("LabeledLine", ["label", "line"])


def cut(line, distance):
    """Cuts a line in two at a distance from its starting point

    Source: http://toblerity.org/shapely/manual.html
    :param line:
    :param distance:
    :return:
    """
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance:
            return [
                LineString(coords[:i+1]),
                LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            return [
                LineString(coords[:i] + [(cp.x, cp.y)]),
                LineString([(cp.x, cp.y)] + coords[i:])]


def split_line(line):
    """Split line into two equal halves, preserving original coordinates.

    :param line:
    :return:
    """
    halves = cut(line, distance=line.length/2)
    logging.debug(halves)
    return halves


def calculate_angle(a, b, c):
    """Return the angle between lines a->b and b->c.

    :param a:
    :type a: shapely.geometry.point.Point
    :param b:
    :type b: shapely.geometry.point.Point
    :param c:
    :type c: shapely.geometry.point.Point
    :return: The angle found at point b.
    :rtype: float
    """
    ab = LineString((a, b)).length
    bc = LineString((b, c)).length
    ac = LineString((a, c)).length
    try:
        angle = degrees(acos((ab**2 + bc**2 - ac**2)/(2 * ab * bc)))
    except ValueError:
        logging.debug('AB: {}, BC: {}, AC: {}'.format(ab, bc, ac))
        raise
    return angle


def classify_line(angle):
    """Classify the line as N/S/E/W based on the angle of the line.

    :param direction:
    :type direction: float
    :return:
    """
    if (angle > (90-22.5)) and (angle <= (90+22.5)):
        return "N"
    elif (angle > (135-22.5)) and (angle <= (135+22.5)):
        return "NE"
    elif (angle > (180-22.5)) or (angle <= (-180+22.5)):
        return "E"
    elif (angle > (-135-22.5)) and (angle <= (-135+22.5)):
        return "SE"
    elif (angle > (-90-22.5)) and (angle <= (-90+22.5)):
        return "S"
    elif (angle > (-45-22.5)) and (angle <= (-45+22.5)):
        return "SW"
    elif (angle > (0-22.5)) and (angle <= (0+22.5)):
        return "W"
    elif (angle > (45-22.5)) and (angle <= (45+22.5)):
        return "NW"
    else:
        raise Exception("")


def calculate_line_direction(line):
    """

    :param line:
    :type line: shapely.geometry.linestring.LineString
    :return:
    :rtype: float
    """
    p1 = line.coords[0]
    p2 = line.coords[-1]
    return degrees(atan2(p2[0] - p1[0], p2[1] - p1[1]))


def classify_lines(lines):
    """Since the polygons are oriented in a clockwise direction we are able to distinguish W/E and N/S lines by
    their direction.

    :param lines:
    :return:
    """
    classified_lines = []
    for line in lines:
        direction = calculate_line_direction(line)
        label = classify_line(direction)
        classified_lines.append(LabeledLine(label, line))

    return classified_lines


def split_intersection(a, b):
    """Return geometry collections of line a split by line b and line b split by line a.

    :param a:
    :type a: shapely.geometry.linestring.LineString
    :param b:
    :type b: shapely.geometry.linestring.LineString
    :return:
    :rtype: tuple
    """
    split_a = split(a, b)
    split_b = split(b, a)
    return split_a, split_b