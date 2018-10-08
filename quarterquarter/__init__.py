from . import polygon_ops


def quarter(polygon):
    labeled_polygon = polygon_ops.LabeledPolygon(label="", polygon=polygon)
    quarters = polygon_ops.quarter(labeled_polygon)
    return quarters


def quarter_quarter(polygon):
    labeled_polygon = polygon_ops.LabeledPolygon(label="", polygon=polygon)
    quarters = polygon_ops.quarter(labeled_polygon)
    qq = []
    if not quarters:
        return qq
    for q in quarters:
        qqs = polygon_ops.quarter(q)
        qq.extend(qqs or [])
    return qq


def quarter_quarter_quarter(polygon):
    labeled_polygon = polygon_ops.LabeledPolygon(label="", polygon=polygon)
    quarters = polygon_ops.quarter(labeled_polygon)
    qqq = []
    if not quarters:
        return qqq
    for q in quarters:
        quarter_quarters = polygon_ops.quarter(q)
        if not quarter_quarters:
            return qqq
        for qq in quarter_quarters:
            qqqs = polygon_ops.quarter(qq)
            qqq.extend(qqqs or [])
    return qqq
