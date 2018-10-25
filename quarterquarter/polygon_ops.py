#!/usr/local/env python3
from collections import namedtuple
import logging

from shapely.geometry import asLineString
from shapely.geometry.multipoint import MultiPoint
from shapely.geometry.linestring import LineString
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.polygon import orient
from shapely.ops import split, linemerge, unary_union

from .line_ops import classify_lines, split_line, calculate_angle, split_intersection

LabeledPolygon = namedtuple("LabeledPolygon", ["label", "polygon"])

MIN_ANGLE = 80
MAX_ANGLE = 100


def split_to_lines(polygon):
    """Split a square-ish polygon into 4 lines.

    :param polygon:
    :type polygon: shapely.geometry.polygon.Polygon
    :return:
    """
    breakpoints = []
    vertices = polygon.exterior.coords

    for i in range(1, len(vertices) + 1):
        a = vertices[i-1]
        try:
            b = vertices[i]
        except IndexError:
            break
        try:
            c = vertices[i+1]
        except IndexError:
            c = vertices[1]
        angle = calculate_angle(a, b, c)
        if MIN_ANGLE < angle < MAX_ANGLE:
            logging.debug("Adding breakpoint: {}".format(angle))
            breakpoints.append(b)
    if len(breakpoints) != 4:
        raise Exception("Expecting 4 breakpoints for polygon, found {}!".format(len(breakpoints)))
    logging.debug(breakpoints)
    lines = split(asLineString(polygon.exterior.coords), MultiPoint(breakpoints))
    return lines


def quarter(polygon):
    """Split the polygon into 4 line strings, classify the lines by their direction to determine
    cardinality.  For each of the 4 lines split at the midpoint while preserving the original coordinates.
    Generate 4 polygons based on the diagram below.

    Eg, the NW polygon is the convex_hull of the following lines
        - first half of the north line
        - first half of the center vertical line
        - first half of the center horizontal line
        - second half of the west line


             1            2
      ---------------------------
      |            |            |
    8 |     NW     |     NE     | 3
      |            |9           |
      |     11     |      12    |
      ---------------------------
      |            |            |
      |            |10          |
    7 |     SW     |     SE     | 4
      |            |            |
      ---------------------------
             6            5

    :param polygon:
    :type polygon: LabeledPolygon
    :return: list of LabeledPolygons
    :rtype: []LabeledPolygon
    """
    label, polygon = polygon.label, polygon.polygon
    try:
        if polygon.type == 'MultiPolygon':
            logging.debug("Multipolygon found, attemping to convert to polygon...")
            polygon = unary_union(polygon)
            if polygon.type == 'MultiPolygon':
                raise Exception("Unable to convert multipolygon to polygon (disjoint)")

        polygon = orient(polygon, sign=-1.0)  # set orientation to clockwise

        lines = split_to_lines(polygon)
        labeled_lines = classify_lines(lines)

        north_lines = split_line(linemerge(MultiLineString([l.line for l in labeled_lines if l.label == "N"])))
        east_lines = split_line(linemerge(MultiLineString([l.line for l in labeled_lines if l.label == "E"])))
        south_lines = split_line(linemerge(MultiLineString([l.line for l in labeled_lines if l.label == "S"])))
        west_lines = split_line(linemerge(MultiLineString([l.line for l in labeled_lines if l.label == "W"])))

        # split the inner lines at their intersection
        center_vertical = LineString((north_lines[0].coords[-1], south_lines[0].coords[-1]))  # straight line between midpoint of north line and midpoint of south line
        center_horizontal = LineString((west_lines[0].coords[-1], east_lines[0].coords[-1]))  # straight line between midpoint of west line and midpoint of east line
        center_verticals, center_horizontals = split_intersection(center_vertical, center_horizontal)

        nw_polygon = LabeledPolygon(
            label="NW" + label,
            polygon=MultiLineString((north_lines[0], center_verticals[0], center_horizontals[0], west_lines[1])).convex_hull
        )
        ne_polygon = LabeledPolygon(
            label="NE" + label,
            polygon=MultiLineString((north_lines[1], center_verticals[0], center_horizontals[1], east_lines[0])).convex_hull
        )
        sw_polygon = LabeledPolygon(
            label="SW" + label,
            polygon=MultiLineString((south_lines[1], center_verticals[1], center_horizontals[0], west_lines[0])).convex_hull
        )
        se_polygon = LabeledPolygon(
            label="SE" + label,
            polygon=MultiLineString((south_lines[0], center_verticals[1], center_horizontals[1], east_lines[1])).convex_hull
        )

        return [nw_polygon, ne_polygon, sw_polygon, se_polygon]
    except Exception as e:
        logging.error("Unable to process polygon! {}; {}".format(polygon, e))
