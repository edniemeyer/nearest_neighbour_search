from collections import namedtuple
from pprint import pformat
from operator import itemgetter
from .nns import dist, haversine

class Node(namedtuple('Node', 'current left_child right_child')):
    def __repr__(self):
        return pformat(tuple(self))

    def nearest(self, point, closest=None, min_dist=None, depth=0):
        distance = dist(self.current, point)
        if distance < min_dist[-1]:
            min_dist.append(distance)
            closest.append(self)
        if self is None:
            return
        if self.left_child is None and self.right_child is None:
            return
        else:
            k = len(point)
            axis = depth % k
            if self.left_child is not None and point[axis] < self.current[axis]:
                self.left_child.nearest(point, closest, min_dist, depth+1)
                if self.right_child is not None and point[axis] + min_dist[-1] >= self.current[axis]:
                    self.right_child.nearest(point, closest, min_dist, depth+1)
            elif self.right_child is not None:
                self.right_child.nearest(point, closest, min_dist, depth+1)
                if self.left_child is not None and point[axis] - min_dist[-1] <= self.current[axis]:
                    self.left_child.nearest(point, closest, min_dist, depth+1)


def build_kdtree(point_list, depth=0):
    try:
        k = len(point_list[0])-1  # assumes all points have the same dimension
    except IndexError as e:  # if not point_list:
        return None
    # Select axis based on depth so that axis cycles through all valid values
    axis = depth % k

    # Sort point list and choose median as pivot element
    point_list.sort(key=itemgetter(axis))
    #point_list = sorted(point_list, key=lambda point: dist(point,(0,0)))
    median = len(point_list) // 2  # choose median

    # Create node and construct subtrees
    return Node(
        point_list[median],
        build_kdtree(point_list[:median], depth + 1),
        build_kdtree(point_list[median + 1:], depth + 1)
    )


def trucks_kdtree(trucks):
    point_list = []
    for t in trucks:
        point_list.append((t['lat'], t['lng'], t))

    return build_kdtree(point_list)
