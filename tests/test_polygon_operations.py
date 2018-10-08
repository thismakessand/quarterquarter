import pytest
import numpy as np
from shapely.geometry.linestring import LineString
from shapely.geometry.polygon import Polygon

from quarterquarter.polygon_ops import split_to_lines


def test_split_to_lines():
    polygon = Polygon(([0, 0], [0, 1], [1, 1], [1, 0], [0, 0]))

    lines = split_to_lines(polygon)
    print(lines[0])
