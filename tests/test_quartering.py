import pytest

from shapely.geometry.polygon import Polygon
from shapely.ops import cascaded_union

from quarterquarter import quarter, quarter_quarter, quarter_quarter_quarter


polygon = Polygon(([0,0], [0, 2], [2, 2], [2, 0], [0, 0]))


def test_quarter():
    quarters = quarter(polygon)
    print(quarters)
    assert len(quarters) == 4
    assert cascaded_union([q.polygon for q in quarters]).area == polygon.area


def test_quarter_quarter():
    quarter_quarters = quarter_quarter(polygon)
    for a in quarter_quarters:
        print(a)
    assert len(quarter_quarters) == 16
    assert cascaded_union([q.polygon for q in quarter_quarters]).area == polygon.area


def test_quarter_quarter_quarter():
    quarter_quarter_quarters = quarter_quarter_quarter(polygon)
    for a in quarter_quarter_quarters:
        print(a)
    assert len(quarter_quarter_quarters) == 64
    assert cascaded_union([q.polygon for q in quarter_quarter_quarters]).area == polygon.area
