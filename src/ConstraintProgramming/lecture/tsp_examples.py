# Example input for Travelling Salesman
#
# @author: Tobias Mérinat

import numpy as np
import copy
from sklearn.neighbors import DistanceMetric


#  Some classes that represent different exercise types
class TspExample:
    """ abstract base class """

    def __init__(self, names, nodes, num_vehicles=1):
        self.names = names
        self.nodes = nodes
        self.num_vehicles = num_vehicles
        self.num_cities = len(names)
        self.depot_index = 0

    def distance(self, a, b):
        raise NotImplementedError()


class Precomputed(TspExample):
    def distance(self, a, b):
        return self.nodes[a][b]


class Euclidean(TspExample):
    def distance(self, a, b):
        x = np.array((*self.nodes[a], *self.nodes[b])).reshape(2, 2)
        return DistanceMetric.get_metric('euclidean').pairwise(x)[0][1]


class Manhattan(TspExample):
    def distance(self, a, b):
        x = np.array((*self.nodes[a], *self.nodes[b])).reshape(2, 2)
        return DistanceMetric.get_metric('manhattan').pairwise(x)[0][1]


class GPS(TspExample):
    def distance(self, a, b):
        from math import radians
        # pairwise wants shape (n_samples, 2) lat lon in radians
        x = np.fromiter(map(radians, (*self.nodes[a], *self.nodes[b])), np.float).reshape(2, 2)
        dists = DistanceMetric.get_metric('haversine').pairwise(x)
        return 3959 * dists[0][1]  # multiply distance by earth radius in miles


# Various examples
small = Precomputed(names=["New York", "Los Angeles", "Chicago", "Salt Lake City"],
                    nodes=[
                        [0, 2451, 713, 1018],  # New York
                        [2451, 0, 1745, 1524],  # Los Angeles
                        [713, 1745, 0, 355],  # Chicago
                        [1018, 1524, 355, 0]])  # Salt Lake City)

large = Precomputed(names=["New York", "Los Angeles", "Chicago", "Minneapolis",
                           "Denver", "Dallas", "Seattle", "Boston",
                           "San Francisco", "St. Louis", "Houston",
                           "Phoenix", "Salt Lake City"],
                    nodes=[
                        [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],  # New York
                        [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],  # Los Angeles
                        [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],  # Chicago
                        [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],  # Minneapolis
                        [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],  # Denver
                        [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],  # Dallas
                        [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],  # Seattle
                        [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],  # Boston
                        [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],  # San Francisco
                        [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],  # St. Louis
                        [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],  # Houston
                        [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],  # Phoenix
                        [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0]])  # Salt Lake City

# cheap way to duplicate and extend above example, not exactly elite coding...
large_capa = copy.deepcopy(large)
large_capa.num_vehicles = 4
large_capa.capacities = [15] * large_capa.num_vehicles
large_capa.demands = [5, 6, 4, 2, 2, 1, 2, 1, 2, 4, 4, 1, 3]
large_capa.demand = lambda node, _: int(large_capa.demands[node])

# random values with parameters defined by the Routing exercise
n = 12
random_costs = np.random.randint(1, 1000, (n, n))
nodes = np.triu(random_costs, 1) + np.triu(random_costs, 1).T  # zero out lower half, then mirror upper
randomly = Precomputed(names=range(len(random_costs)), nodes=nodes, num_vehicles=2)

gps = GPS(names=["New York", "Los Angeles", "Chicago", "Minneapolis", "Denver", "Dallas", "Seattle", "Boston",
                 "San Francisco",
                 "St. Louis", "Houston", "Phoenix", "Salt Lake City"],
          nodes=[
              (40.71, -74.01),  # New York
              (34.05, -118.24),  # Los Angeles
              (41.88, -87.63),  # Chicago
              (44.98, -93.27),  # Minneapolis
              (39.74, -104.99),  # Denver
              (32.78, -96.89),  # Dallas
              (47.61, -122.33),  # Seattle
              (42.36, -71.06),  # Boston
              (37.77, -122.42),  # San Francisco
              (38.63, -90.20),  # St.Louis
              (29.76, -95.37),  # Houston
              (33.45, -112.07),  # Phoenix
              (40.76, -111.89)])  # Salt Lak City

drilling = Euclidean(names=range(280),  # the length of the node list
                     nodes=[(288, 149), (288, 129), (270, 133), (256, 141), (256, 157), (246, 157), (236, 169),
                            (228, 169), (228, 161), (220, 169), (212, 169), (204, 169), (196, 169), (188, 169),
                            (196, 161), (188, 145), (172, 145), (164, 145), (156, 145), (148, 145), (140, 145),
                            (148, 169), (164, 169), (172, 169), (156, 169), (140, 169), (132, 169), (124, 169),
                            (116, 161), (104, 153), (104, 161), (104, 169), (90, 165), (80, 157), (64, 157),
                            (64, 165), (56, 169), (56, 161), (56, 153), (56, 145), (56, 137), (56, 129), (56, 121),
                            (40, 121), (40, 129), (40, 137), (40, 145), (40, 153), (40, 161), (40, 169), (32, 169),
                            (32, 161), (32, 153), (32, 145), (32, 137), (32, 129), (32, 121), (32, 113), (40, 113),
                            (56, 113), (56, 105), (48, 99), (40, 99), (32, 97), (32, 89), (24, 89), (16, 97),
                            (16, 109), (8, 109), (8, 97), (8, 89), (8, 81), (8, 73), (8, 65), (8, 57), (16, 57),
                            (8, 49), (8, 41), (24, 45), (32, 41), (32, 49), (32, 57), (32, 65), (32, 73), (32, 81),
                            (40, 83), (40, 73), (40, 63), (40, 51), (44, 43), (44, 35), (44, 27), (32, 25), (24, 25),
                            (16, 25), (16, 17), (24, 17), (32, 17), (44, 11), (56, 9), (56, 17), (56, 25), (56, 33),
                            (56, 41), (64, 41), (72, 41), (72, 49), (56, 49), (48, 51), (56, 57), (56, 65), (48, 63),
                            (48, 73), (56, 73), (56, 81), (48, 83), (56, 89), (56, 97), (104, 97), (104, 105),
                            (104, 113), (104, 121), (104, 129), (104, 137), (104, 145), (116, 145), (124, 145),
                            (132, 145), (132, 137), (140, 137), (148, 137), (156, 137), (164, 137), (172, 125),
                            (172, 117), (172, 109), (172, 101), (172, 93), (172, 85), (180, 85), (180, 77), (180, 69),
                            (180, 61), (180, 53), (172, 53), (172, 61), (172, 69), (172, 77), (164, 81), (148, 85),
                            (124, 85), (124, 93), (124, 109), (124, 125), (124, 117), (124, 101), (104, 89),
                            (104, 81), (104, 73), (104, 65), (104, 49), (104, 41), (104, 33), (104, 25), (104, 17),
                            (92, 9), (80, 9), (72, 9), (64, 21), (72, 25), (80, 25), (80, 25), (80, 41), (88, 49),
                            (104, 57), (124, 69), (124, 77), (132, 81), (140, 65), (132, 61), (124, 61), (124, 53),
                            (124, 45), (124, 37), (124, 29), (132, 21), (124, 21), (120, 9), (128, 9), (136, 9),
                            (148, 9), (162, 9), (156, 25), (172, 21), (180, 21), (180, 29), (172, 29), (172, 37),
                            (172, 45), (180, 45), (180, 37), (188, 41), (196, 49), (204, 57), (212, 65), (220, 73),
                            (228, 69), (228, 77), (236, 77), (236, 69), (236, 61), (228, 61), (228, 53), (236, 53),
                            (236, 45), (228, 45), (228, 37), (236, 37), (236, 29), (228, 29), (228, 21), (236, 21),
                            (252, 21), (260, 29), (260, 37), (260, 45), (260, 53), (260, 61), (260, 69), (260, 77),
                            (276, 77), (276, 69), (276, 61), (276, 53), (284, 53), (284, 61), (284, 69), (284, 77),
                            (284, 85), (284, 93), (284, 101), (288, 109), (280, 109), (276, 101), (276, 93),
                            (276, 85), (268, 97), (260, 109), (252, 101), (260, 93), (260, 85), (236, 85), (228, 85),
                            (228, 93), (236, 93), (236, 101), (228, 101), (228, 109), (228, 117), (228, 125),
                            (220, 125), (212, 117), (204, 109), (196, 101), (188, 93), (180, 93), (180, 101),
                            (180, 109), (180, 117), (180, 125), (196, 145), (204, 145), (212, 145), (220, 145),
                            (228, 145), (236, 145), (246, 141), (252, 125), (260, 129), (280, 133)])

manhattan = Manhattan(names=range(17),  # the length of the node list
                      nodes=[(4, 4), (2, 0), (8, 0), (0, 1), (1, 1), (5, 2), (7, 2), (3, 3), (6, 3),
                             (5, 5), (8, 5), (1, 6), (2, 6), (3, 7), (6, 7), (0, 8), (7, 8)])

manhattan_capa = copy.deepcopy(manhattan)
manhattan_capa.num_vehicles = 4
manhattan_capa.capacities = [15] * manhattan_capa.num_vehicles
manhattan_capa.demands = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
manhattan_capa.demand = lambda node, _: int(manhattan_capa.demands[node])
