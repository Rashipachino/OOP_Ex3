from unittest import TestCase

from src.EdgeData import EdgeData


class TestEdgeData(TestCase):
    global e
    e = EdgeData(2, 1, 1.5)
    def test_set_weight(self):
        e.set_weight(1.7)
        self.assertEquals(e.weight, 1.7)
