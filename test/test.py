import unittest
from src.nns import dist, haversine, nearest, simple_nearest_neighbour, find_next_closest
from src.kdtree import build_kdtree, trucks_kdtree


class Test(unittest.TestCase):

    def test_haversine(self):
        p1 = (39.0661472, -84.70318879999999)
        p2 = (40.3933956, -82.4857181)
        distance = haversine(p1, p2)
        self.assertEqual(distance,  240.2158370923567)

    def test_cartesian_distance(self):
        p1 = (39.0661472, -84.70318879999999)
        p2 = (40.3933956, -82.4857181)
        distance = dist(p1, p2)
        self.assertEqual(distance,  2.5843305943050328)

    def test_build_kdtree(self):
        point_list = [(0, 1, 'p1'), (2, 2, 'p2'), (8, 4, 'p3')]
        kdtree = build_kdtree(point_list)
        expected_kdtree = ((2, 2, 'p2'),
                           ((0, 1, 'p1'), None, None), ((8, 4, 'p3'), None, None))
        self.assertEqual(kdtree, expected_kdtree)

    def test_search_nearest_neighbour_kdtree(self):
        point_list = [(0, 1, 'p1'), (2, 2, 'p2'), (8, 4, 'p3')]
        kdtree = build_kdtree(point_list)

        target_point = (3, 5, 'target')
        expected_nearest_point = 'p2'
        nearest_point = nearest(kdtree, target_point)
        self.assertEqual(nearest_point[-1].current[2], expected_nearest_point)

        target_point = (-3, -5, 'target')
        expected_nearest_point = 'p1'
        nearest_point = nearest(kdtree, target_point)
        self.assertEqual(nearest_point[-1].current[2], expected_nearest_point)

        target_point = (8, -1, 'target')
        expected_nearest_point = 'p3'
        nearest_point = nearest(kdtree, target_point)
        self.assertEqual(nearest_point[-1].current[2], expected_nearest_point)

    def test_simple_nearest_neighbour_search(self):

        point_list = [{'lat': 0, 'lng': 1, 'name': 'p1'},
                      {'lat': 2, 'lng': 2, 'name': 'p2'},
                      {'lat': 8, 'lng': 4, 'name': 'p3'}]

        target_point = {'origin_lat': 3, 'origin_lng': 5, 'name': 'target'}
        expected_nearest_point = {'lat': 2, 'lng': 2, 'name': 'p2'}
        nearest_point = simple_nearest_neighbour(
            target_point, point_list)
        self.assertEqual(nearest_point[-1].current[2], expected_nearest_point)

        target_point = {'origin_lat': -3, 'origin_lng': -5, 'name': 'target'}
        expected_nearest_point = {'lat': 0, 'lng': 1, 'name': 'p1'}
        nearest_point = simple_nearest_neighbour(
            target_point, point_list)
        self.assertEqual(nearest_point[-1].current[2], expected_nearest_point)

        target_point = {'origin_lat': 8, 'origin_lng': -1, 'name': 'target'}
        expected_nearest_point = {'lat': 8, 'lng': 4, 'name': 'p3'}
        nearest_point = simple_nearest_neighbour(
            target_point, point_list)
        self.assertEqual(nearest_point[-1].current[2], expected_nearest_point)

    def test_find_next_closest(self):

        point_list = [{'lat': 0, 'lng': 1, 'truck': 'p1'},
                      {'lat': 2, 'lng': 2, 'truck': 'p2'},
                      {'lat': 8, 'lng': 4, 'truck': 'p3'},
                      {'lat': 8, 'lng': 7, 'truck': 'p4'},
                      {'lat': 8, 'lng': 8, 'truck': 'p5'},
                      {'lat': 8, 'lng': 10, 'truck': 'p6'}]

        
        expected_nearest_point = {'lat': 2, 'lng': 2, 'name': 'p2'}
        tree = trucks_kdtree(point_list)
        t_result = {}

        
        c = {'origin_lat': 2, 'origin_lng': 3, 'name': 'target1'}
        target_point = (c['origin_lat'], c['origin_lng'])
        truck1 = nearest(tree, target_point)
        find_next_closest(t_result, truck1, c)


        c = {'origin_lat': 2, 'origin_lng': 4, 'name': 'target2'}
        target_point = (c['origin_lat'], c['origin_lng'])
        truck2 = nearest(tree, target_point)

        self.assertEqual(truck1[-1].current[2], truck2[-1].current[2])
        find_next_closest(t_result, truck2, c)

        self.assertEqual(len(t_result), 2)
        # make sure the closer closest is selected and second closest assigned to the other cargo
        self.assertTrue(truck1[-1].current[2]['truck'] in t_result)
        self.assertTrue(truck2[-2].current[2]['truck'] in t_result)




if __name__ == '__main__':
    unittest.main()
