from math import radians, cos, sin, asin, sqrt
from collections import namedtuple


def dist(p1, p2):
    return sqrt((p1[0] - p2[0])**2 +
                (p1[1] - p2[1])**2)


def haversine(p1, p2):
    """Haversine formula to calculate distance between two coordinates in KM"""
    R = 6369.345  # Earth Radius at latitude 40N
    lat1 = p1[0]
    lon1 = p1[1]
    lat2 = p2[0]
    lon2 = p2[1]

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c


def simple_nearest_neighbour(cargo, trucks):
    """Returns info about the nearest point and distance to target using naive approach"""
    point = (cargo['origin_lat'], cargo['origin_lng'])
    min_dist = float('inf')
    nearest_truck = []
    # to be in the same structure as Kdtree
    Point = namedtuple('Node', 'current left_child right_child')
    for t in trucks:
        # using cartesian distance to be comparable to kdtree
        distance = dist(point, (t['lat'], t['lng']))
        # to make it realistic, should use haversine formula
        # distance = haversine(point, (t['lat'], t['lng']))
        if distance < min_dist:
            min_dist = distance
            nearest_truck.append(Point((t['lat'], t['lng'],t), None, None))
    return nearest_truck


def nearest(node, point):
    """Returns info about the nearest point and distance to target"""
    closest = []
    min_dist = [float('inf')]

    node.nearest(point, closest, min_dist)
    return closest


def find_next_closest(selected, to_select, c, i=0):
    """Recursive call to select next closest point, if already selected"""
    point = (c['origin_lat'], c['origin_lng'])
    distance = haversine(to_select[i-1].current, point)
    if to_select[i-1].current[2]['truck'] in selected:
        if selected[to_select[i-1].current[2]['truck']][0] > distance:
            to_reselect = selected[to_select[i-1].current[2]['truck']][2]
            c_to_reselect = selected[to_select[i-1].current[2]['truck']][1]
            selected.update(
                {to_select[i-1].current[2]['truck']: [distance, c, to_select]})
            find_next_closest(selected,
                              to_reselect,
                              c_to_reselect
                              )
        else:
            find_next_closest(selected, to_select, c, i-1)
    else:
        selected.update(
            {to_select[i-1].current[2]['truck']: [distance, c, to_select]})
