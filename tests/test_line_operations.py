import pytest
import numpy as np
from shapely.geometry import asLineString
from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point


from matplotlib import pyplot as plt

from quarterquarter.line_ops import split_line, calculate_angle, split_intersection


straight_line = LineString(([0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5]))
non_straight_line = LineString(([0, 0], [1, 1], [0, 2]))
non_straight_line_2 = LineString(([0, 0], [2, 3], [8, 0]))
line2 = LineString(([float(a) for a in x.split()]) for x in """152321.9014999997 4109645.352399999, 152305.5596000003 4109243.025900001, 152289.2164000003 4108840.6993,
152272.8749000002 4108438.3731, 152256.5372000001 4108036.047""".split(","))

intersecting_line_a = LineString(([1, 0], [1, 1], [1, 2]))
intersecting_line_b = LineString(([0, 1], [1, 1], [2, 1]))


@pytest.mark.parametrize("line", [
    straight_line,
    non_straight_line,
    non_straight_line_2,
    line2
])
def test_halve_line(line):
    """There should be
    - two lines returned
    - they should be of equal length
    - The last point in the first half should match the first point in the second half
    - The midpoint should intersect the original line
    """
    halves = split_line(line)

    assert len(halves) == 2
    assert np.allclose(halves[0].length, halves[1].length)

    midpoint = Point(halves[0].coords[-1])
    assert midpoint == Point(halves[1].coords[0])
    assert midpoint.buffer(.00000001).intersects(line)


def test_calculate_angle():
    a = Point(0, 0)
    b = Point(1, 1)
    c = Point(2, 0)

    angle = calculate_angle(a, b, c)
    assert np.isclose(angle, 90.0)


def test_split_intersection():
    a_split, b_split = split_intersection(intersecting_line_a, intersecting_line_b)
    assert len(a_split) == 2
    assert len(b_split) == 2

    assert a_split[0] == LineString(([1, 0], [1,1]))
