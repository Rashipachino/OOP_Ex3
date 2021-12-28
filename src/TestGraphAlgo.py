from unittest import TestCase

from src.GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):
    global g_algo
    g_algo = GraphAlgo()  # init an empty graph - for the GraphAlgo
    file = "../data/A0.json"
    g_algo.load_from_json(file)

    def test_load_from_json(self):
        g_algo = GraphAlgo()  # init an empty graph - for the GraphAlgo
        file = "../data/A0.json"
        g_algo.load_from_json(file)

    def test_save_to_json(self):
        g_algo = GraphAlgo()  # init an empty graph - for the GraphAlgo
        file = "../data/A0.json"
        g_algo.save_to_json(file + '_saved')

    def test_shortest_path(self):
        g_algo.shortest_path(1, 7)

    def test_tsp(self):
        g_algo.TSP([0, 10, 9])

    def test_center_point(self):
        g_algo.centerPoint()
